""" semantic processing of the query to generate better results."""

from __future__ import annotations
from collections import namedtuple, defaultdict
import logging
from typing import List, Callable, Dict
from delphai_search_utils.utils import split_with_indices

logger = logging.getLogger(__name__)

# which keywords to replace with AND?
AND_KEYWORDS = ["and", "for"]
OR_KEYWORDS = ["or"]
NOT_KEYWORDS = ["not"]

SYNONYM_TERMS_TYPE = "synonyms"
SIMILAR_TERMS_TYPE = "similars"

# This represents a related term, e.g. a synonym or an alternative spelling,
# but it can also be a boolean query. The .query field is saved as a TextQuery,
# so it will be transformed to a string again afterwards.
RelatedQueryTerm = namedtuple('RelatedQueryTerm', ['query', 'source'])


class TextQueryOp:

    def __init__(self, op):
        if op not in ['OR', 'AND', 'NOT']:
            logger.error(f'TextQueryOp has been called with an invalid argument: {op}')
        self.op = op

    def negate(self):
        if self.op == 'OR':
            self.op = 'AND'
        elif self.op == 'AND':
            self.op = 'OR'
        elif self.op == 'NOT':
            # This case happens in the current logic but it's not resolved
            # here so it can be just ignored.
            pass


class TextQueryTerm:

    def __init__(
            self,
            term: str,    # actual term string
            start_pos: int = None,    # character position
            negated: bool = False,    # whether the term is negated
            quoted: bool = False,    # whether the term is quoted
            related_query_terms: Dict[int, List[RelatedQueryTerm]] = None,    # list of related terms
    ):
        self.str = term
        self.start_pos = start_pos
        self.negated = negated
        self.quoted = term.startswith('"') and term.endswith('"')
        self.related_query_terms = defaultdict(list)
        if related_query_terms is not None:
            self.related_query_terms = related_query_terms

    def expand_with_fct(
            self,
            similars_fct: Callable,
            terms_type: int = SYNONYM_TERMS_TYPE,    # or SIMILAR_TERMS_TYPE
            apply_on_synonyms: bool = True,
    ):
        """ Adds related terms to this term, depending on the function that
        is passed.
        'apply_on_synonyms' determines if we also apply the function on the
        synonyms that were already found or only on the term itself."""
        if self.quoted:
            return
        apply_on = [self.str]
        if apply_on_synonyms:
            # collect related query terms that only have a single term
            # (so they are e.g. not queries with boolean operators).
            terms_collection = [
                query_term.query.get_terms()
                for query_term in self.related_query_terms[SYNONYM_TERMS_TYPE]]
            apply_on += [
                terms[0].str for terms in terms_collection
                if len(terms) == 1 and not terms[0].quoted]
        for term in apply_on:
            similars_result = similars_fct(term)
            for result in similars_result:
                self.add_related(terms_type, result, similars_fct.__name__)

    def add_related(self, term_type: str, related_query_term: str, source: str):
        query_object = TextQuery.from_str(related_query_term)
        related_object = RelatedQueryTerm(query_object, source)
        self.related_query_terms[term_type].append(related_object)

    def negate(self):
        self.negated = not self.negated

    def __str__(self):
        # 'add_quotes_to_unquoted_terms' is a parameter to influence the Elasticsearch behavior;
        # if we change this to False the term will not be treated as a single phrase but
        # implicitly combined with an AND, so there will be a lot more (irrelevant) results.
        add_quotes_to_unquoted_terms = True
        self_term = self.str
        if not self.quoted and add_quotes_to_unquoted_terms:
            self_term = f'"{self.str}"'
        terms = [self_term] + \
            [term.query.to_str() for term in self.related_query_terms[SYNONYM_TERMS_TYPE]]
        terms_str = ' OR '.join(terms)
        if len(terms) >= 2:
            terms_str = f'({terms_str})'
        if self.negated:
            terms_str = f'NOT {terms_str}'
        return terms_str

    def __repr__(self):
        return self.__str__()


class TextQuery:
    """ helper class to help with query expansion etc.
    a TextQuery consists of terms, operators, and subqueries (of type TextQuery).
    currently supports AND, OR and NOT."""

    def __init__(self, subqueries, prune=False):
        self.subqueries = subqueries
        if prune:
            self.substitute_negations()
            self.collapse()

    def to_str(self):
        """ returns a readable query string representation which
        can be used in Elasticsearch."""
        query_parts = []
        for i, subq in enumerate(self.subqueries):
            if type(subq) == TextQuery:
                if len(subq.subqueries) == 1:
                    query_parts.append(subq.to_str())
                else:
                    query_parts += ['(', subq.to_str(), ')']
            elif type(subq) == TextQueryTerm:
                query_parts.append(str(subq))
            elif type(subq) == TextQueryOp:
                query_parts.append(subq.op)
        query_str = " ".join(query_parts)
        if len(self.subqueries) >= 2:
            query_str = f'({query_str})'
        return query_str

    @classmethod
    def from_str(cls, query_str):
        """ query parser that identifies brackets, AND and OR.
        handles an arbitrary number of nested brackets but won't produce
        reasonable results for a wrong query syntax."""
        query_layers = defaultdict(list)
        current_layer = 0
        # create a stack and process tokens from front to back
        query_stack = list(split_with_indices(query_str))[::-1]
        open_quotes = False
        while len(query_stack) >= 1:
            tok, start_idx = query_stack.pop()
            # preprocess token
            # tok = tok.lower()
            tok_lower = tok.lower()
            if tok == '"':
                open_quotes = not open_quotes
            if len(tok) == 0:
                continue
            # handle quotes
            if '"' in tok and not tok == '"':
                # split by quotes
                quote_idx = tok.index('"')
                if quote_idx + 1 < len(tok):
                    query_stack.append((tok[quote_idx + 1:], start_idx + quote_idx + 1))
                query_stack.append(('"', start_idx + quote_idx))
                if quote_idx > 0:
                    query_stack.append((tok[:quote_idx], start_idx))
            # handle brackets
            elif tok.startswith("(") and not open_quotes:
                current_layer += 1
                remaining = tok[1:]
                query_stack.append((remaining, start_idx + 1))
            elif tok.endswith(")") and not tok == ')' and not open_quotes:
                query_stack.append((')', start_idx + len(tok) - 1))
                query_stack.append((tok[:-1], start_idx))
            elif tok == ')' and not open_quotes:
                nested_query = TextQuery.from_list(query_layers[current_layer])
                query_layers[current_layer - 1].append(nested_query)
                query_layers[current_layer] = []
                current_layer -= 1
            # handle actual terms
            else:
                # keywords
                if tok_lower in AND_KEYWORDS and not open_quotes:
                    query_layers[current_layer].append(TextQueryOp('AND'))
                elif tok_lower in OR_KEYWORDS and not open_quotes:
                    query_layers[current_layer].append(TextQueryOp('OR'))
                elif tok_lower in NOT_KEYWORDS and not open_quotes:
                    query_layers[current_layer].append(TextQueryOp('NOT'))
                # query terms
                elif len(query_layers[current_layer]) == 0:
                    query_layers[current_layer].append(TextQueryTerm(tok, start_idx))
                elif type(query_layers[current_layer][-1]) in (TextQueryOp, TextQuery):
                    # new term
                    query_layers[current_layer].append(TextQueryTerm(tok, start_idx))
                elif type(query_layers[current_layer][-1]) == TextQueryTerm:
                    # append to current term
                    term = query_layers[current_layer][-1]
                    end_pos = start_idx + len(tok)
                    # print(f'appending {tok} to {term}')
                    new_term = query_str[term.start_pos:end_pos]
                    query_layers[current_layer][-1] = TextQueryTerm(new_term, term.start_pos)
        return cls(query_layers[0], prune=True)

    @classmethod
    def from_list(cls, query_parts):
        """ create query from list or tuple of query parts."""
        subquery_list = list(query_parts)
        return cls(subquery_list)

    def get_terms(self) -> List[TextQueryTerm]:
        """ returns only the actual terms included in this query without
        any operators; is used for resolving keywords."""
        terms = []
        for subq in self.subqueries:
            if type(subq) == TextQueryTerm:
                terms.append(subq)
            elif type(subq) == TextQuery:
                terms += subq.get_terms()
        return terms

    def reduce(self):
        """ reduces this query if it has only a single subquery"""
        if len(self.subqueries) == 1:
            subq = self.subqueries[0]
            if type(subq) == TextQuery:
                return subq.reduce()
            else:
                return [subq]
        else:
            return self.subqueries

    def collapse(self):
        """ optimize the query: if it has only one TextQuery as subquery
        then one layer can be removed."""
        collapsed_qs = []
        subs = self.reduce()
        for i, subq in enumerate(subs):
            if type(subq) == TextQuery:
                if not subq.is_empty():
                    # collapse subquery and append
                    subq.collapse()
                    collapsed_qs.append(subq)
            elif type(subq) in [TextQueryTerm, TextQueryOp]:
                # regular term
                collapsed_qs.append(subq)
        self.subqueries = collapsed_qs

    def negate(self):
        for subquery in self.subqueries:
            subquery.negate()

    def substitute_negations(self):
        """ Substitute the query so that negations are passed on to
        the single query terms; e.g.
        'NOT (A AND B)' becomes '(NOT A OR NOT B)'.
        see also https://en.wikipedia.org/wiki/De_Morgan%27s_laws
        """
        # Identify all query parts that need to be negated in the right order.
        # We want to substitute nested negations first because that makes
        # it very straight forward. E.g.
        # 'NOT (A AND NOT (B OR C))'
        # will be 'NOT (A AND (NOT B AND NOT C))'
        # and then '(NOT A OR (B OR C))'
        def build_stack(query, stack):
            for i, subquery in enumerate(query.subqueries):
                if type(subquery) == TextQueryOp and subquery.op == 'NOT':
                    # next term should be negated
                    try:
                        stack.append(query.subqueries[i + 1])
                    except IndexError:
                        logger.error(f'Invalid query: Found NOT at the end of a query: {query.to_str()}')
                elif type(subquery) == TextQuery:
                    build_stack(subquery, stack)

        negate_stack = []
        build_stack(self, negate_stack)
        # Do the actual substitutions
        for subquery in negate_stack[::-1]:
            subquery.negate()
        # Remove all 'NOT's because they have been applied but still exist.
        # (They are now encoded in TextQueryTerm.negated.)
        query_list = [self]
        while len(query_list) >= 1:
            query = query_list.pop()
            query.subqueries = [
                subquery for subquery in query.subqueries
                if not (type(subquery) == TextQueryOp and subquery.op == 'NOT')
            ]
            query_list += [
                subquery for subquery in query.subqueries
                if type(subquery) == TextQuery
            ]

    def is_empty(self):
        """ returns true if it doesn't contain relevant query information"""
        if len(self.subqueries) == 0:
            return True
        else:
            for subq in self.subqueries:
                if type(subq) == TextQueryTerm or    \
                        (type(subq) == TextQuery and not subq.is_empty()):
                    return False
            return True

    def expand_with_syns_fct(
            self,
            similars_fct: Callable,
            terms_type: int = SYNONYM_TERMS_TYPE,    # or SIMILAR_TERMS_TYPE
            apply_on_synonyms: bool = True):
        for query_term in self.get_terms():
            query_term.expand_with_fct(similars_fct, terms_type, apply_on_synonyms)

    def get_related_terms_map(self) -> Dict[str, List[Dict[str, str]]]:
        """ Create a map of related terms by collecting them for each unique term."""
        related_terms_map = defaultdict(list)
        processed_terms = set()
        for query_term in self.get_terms():
            if query_term.str in processed_terms:
                # avoid duplicates in the map;
                # equal terms will have equal related terms.
                continue
            processed_terms.add(query_term.str)
            for related_type, terms in query_term.related_query_terms.items():
                for related_term in terms:
                    related_terms_map[related_type].append({
                        'original': query_term.str,
                        'term': related_term.query.to_str(),
                        'source': related_term.source,
                    })
        return related_terms_map

    def add_related_terms_from_map(self, related_terms_map: Dict[str, List[Dict[str, str]]]):
        """ Takes a map of related terms as created by get_related_terms_map()
        and adds them to the terms of this query."""
        for query_term in self.get_terms():
            for related_type, terms_list in related_terms_map.items():
                for related_term in terms_list:
                    if related_term['original'] == query_term.str:
                        related_term_str = str(related_term['term'])
                        source = related_term.get('source', '')
                        query_term.add_related(
                            related_type,
                            related_term_str,
                            source)
                        if related_type == 'synonyms':
                            print(f'added {related_term_str=} to {query_term=}')

    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.__str__()
