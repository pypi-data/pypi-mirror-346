"""
NOTE that this file is currently not used.
It has some structures that seem promising going forward but it is incomplete
and would need more implementations for various use cases etc.
It would help a lot with the situation in query-companies, however.
""" 
from typing import Dict, List
from dataclasses import dataclass
from delphai_search_utils.text_query import TextQuery


def _single_match(field: str, value, vals_added: set) -> dict:
    if isinstance(value, (int, float, bool)):
        if value not in vals_added:
            vals_added.add(value)
            return {'match': {field: value}}
    if isinstance(value, str):
        value = value.strip().lower()
        if value and value not in vals_added:
            vals_added.add(value)
            return {'match': {field: {'query': value, 'operator': 'and'}}}
    return None


@dataclass
class Filter:
    """ Contains a single filter element regarding
    a specific field, a clause, and whether it should be
    fulfilled or negated (i.e., does it belong to a
    'must' or a 'must_not' query?)"""
    filter_type: str
    filter_clause: Dict
    do_negate: bool

    @classmethod
    def from_time_range(cls, value_from, value_to):
        range_criteria = {}
        if value_from and value_from.is_numeric():
            range_criteria['gte'] = int(value_from)
        if value_to and value_to.is_numeric():
            range_criteria['lte'] = int(value_to)
        if range_criteria:
            filter_clause = {'range': {'founded': range_criteria}}
            return cls('time', filter_clause, False)
        return None

    @classmethod
    def from_time_values(cls, year_values):
        years_list = [year for year in year_values if year.is_numeric()]
        if years_list:
            filter_clause = {'terms': {'founded': years_list}}
            return cls('time', filter_clause, False)
        return None

    @classmethod
    def from_location(self, location_field, value):
        pass

    @classmethod
    def from_company_type(self, value):
        pass


@dataclass
class Aggregation:
    """ Contains a single aggregation clause."""
    aggregation_name: str
    aggregation_query: Dict


class Query:
    """ Comprises all components of a query:
    - TextQuery for the actual content
    - A list of Filters
    - A list of Aggregations
    This makes the process of processing queries and user inputs
    extremely modular and simplifies how to manipulate queries.
    This class can be treated as an interface between logical query
    components and the query representation for Elasticsearch."""

    def __init__(self, text_query: TextQuery):
        self.text_query = text_query
        self.filters = []
        self.aggregations = []

    def add_filter(self, query_filter: Filter):
        self.filters.append(query_filter)

    def add_aggregation(self, query_aggregation: Aggregation):
        self.aggregations.append(query_aggregation)

    def get_elastic_query(
            self,
            exclude_filter_types: List[str] = None,
            without_aggregations: bool = False
            ) -> Dict:
        """ Produces a query representation to query Elasticsearch, including
        the actual text content, all filters and aggregations."""
        return {}
