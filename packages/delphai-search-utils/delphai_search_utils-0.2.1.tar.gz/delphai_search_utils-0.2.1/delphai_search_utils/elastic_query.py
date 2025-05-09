from delphai_search_utils.text_query import TextQuery
from delphai_utils.config import get_config
from delphai_utils.formatting import clean_url
from collections import defaultdict


def get_field_weights():
    weights_cfg = get_config('elastic_ranking.query_weights')
    labels_cfg = get_config('label_layers_searched')
    for label, incl in labels_cfg.items():
        label = f'{label}_labels'
        if label in weights_cfg and not incl:
            weights_cfg.pop(label)
        if label not in weights_cfg and incl:
            weights_cfg[label] = 1
    return weights_cfg


def build_query_clause(term, weight_factor=1, with_quotes=True, incl_names=False):
    """ simply builds a query clause and adjusts the weights"""
    weights_cfg = get_field_weights()
    incl_text = not get_config('elastic_ranking.disable_webpage_search')
    fields = [
        f'{name}^{weight / weight_factor:.3f}'
        for name, weight in weights_cfg.items()
        if (incl_names or name not in ['name', 'url', 'name.keyword', 'url.keyword']) and
            (incl_text or name not in ['text', 'pages.text'])]
    if with_quotes:
        unquoted_term = term.strip('" ')
        term = f'"{unquoted_term}"'
    # build elastic clause
    clause = {
        "query_string": {
            "query": term,
            "fields": fields,
            "type": 'best_fields',  # default
        }
    }
    if get_config('elastic_ranking.sum_field_scores', False):
        # alternative scoring which sums score of each field for a term,
        # instead of taking the maximum score
        clause['query_string']['type'] = 'cross_fields'
        clause['query_string']['tie_breaker'] = 1.0
    return clause


def create_elastic_query(query_parsed, related_terms_map):
    query_expanded = TextQuery.from_str(query_parsed)
    query_expanded.add_related_terms_from_map(related_terms_map)
    query_expanded_str = query_expanded.to_str()
    query_dictionary = {
        "must": [],
        "should": [],
        "string": query_expanded_str,
    }
    top_query = {
        "bool": {
            "minimum_should_match": 1,
            "should": [
                # query part with whole query string
                build_query_clause(query_expanded_str, with_quotes=False, incl_names=True),
                # exact match for name
                {
                    "term": {
                        "name_keyword": {
                            "term": query_parsed.strip('"'),
                            "boost": 2
                        }
                    }
                },
                # exact match for url
                {
                    "term": {
                        "url.keyword": {
                            "term": clean_url(query_parsed),
                            "boost": 3
                        }
                    }
                }
            ]
        }
    }
    if 'project_annotations' in get_config('elastic_ranking.query_weights'):
        weight = get_config('elastic_ranking.query_weights.project_annotations')
        anno_match_clause = {
            "term": {
                "project_annotations": {
                    "value": query_parsed,
                    "boost": weight * 2,
                }
            }
        }
        top_query['bool']['should'].append(anno_match_clause)
    query_dictionary['must'] = top_query

    # add single terms as additional boosts 
    # (with weights proportional to their position in the query)
    term_nbr = len(query_expanded.get_terms())
    # The factors are inversely proportional to term weights
    factors = []
    if term_nbr < 2:
        # If only one term is present, it's factor is set to 2
        factors = [2 for i in range(term_nbr)]
    else:
        # Otherwise, the factors range from 1.3 to 3.9
        factors = [1.3 + 2.6/(term_nbr - 1)*i for i in range(term_nbr)]
    for factor, query_term in list(zip(factors, query_expanded.get_terms())):
        if not query_term.negated:
            # add query boosting query clause for this similar term;
            # we don't need quotes here because they are already added in the term's
            # __str__() function itself; for complex queries this leads to errors, e.g.
            # '"("EVs" OR "electric vehicles")"', so that the brackets are enclosed in quotes
            term_clause = build_query_clause(str(query_term), factor, with_quotes=False, incl_names=False)
            query_dictionary['should'].append(term_clause)

    # add related similar terms as additional boosts
    # (with weights proportional to the position of the original term in the query)
    # (max N per query term)
    max_term_count = get_config('elastic_ranking.similar_keywords.count')
    per_term_counts = defaultdict(int)
    # If a related term is not matched with any original terms, it's factor is set to 4
    factors.append(4)
    for similar_term in related_terms_map['similar_terms']:
        if per_term_counts[similar_term['original']] < max_term_count:
            ind = 0
            for query_term in query_expanded.get_terms():
                # Checking which query term corresponds to this similar term
                if query_term.str == similar_term['original']:
                    break
                ind += 1
            factor = factors[ind]
            term_clause = build_query_clause(similar_term['term'], factor, with_quotes=True, incl_names=False)
            query_dictionary['should'].append(term_clause)
            per_term_counts[similar_term['original']] += 1

    query_dictionary['_source'] = {
        'include': [
            'see_also_ids',
            'company_id',
            'name',
            'url',
            'href',
            'organisation_type',
            'founded',
            'headquarters',
            'relevance_score',
            'description',
            'funding',
            'n_investors',
            'added'
        ]
    }
    return query_dictionary
