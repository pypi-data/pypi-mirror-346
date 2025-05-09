"""
Note that one drawback from this test suite is that we cannot really test
the correctness of Elasticsearch queries here. There are different ways to
dreach the same results/behavior and we can only test for one version here;
for example "NOT (A OR B)" is the same as "NOT A AND NOT B".
"""
from delphai_search_utils.text_query import TextQuery, SYNONYM_TERMS_TYPE
from delphai_search_utils.text_query import TextQueryOp, TextQueryTerm
from delphai_search_utils.utils import query_contained_in_query
import pytest
import os
from typing import List, Dict, Callable
os.environ['DELPHAI_ENVIRONMENT'] = 'development'


@pytest.mark.parametrize("query,terms", [
  ('Mobility', ['"Mobility"']),
  ('mobility and (scooters or bikes)', ['"mobility"', '"scooters"', '"bikes"']),
  ('autonomous robots and ppe', ['"autonomous robots"', '"ppe"']),
  ('ML applications and not statistics', ['"ML applications"', 'NOT "statistics"']),
  ('Process mining Or Bitcoins', ['"Process mining"', '"Bitcoins"']),
])
def test_query_term_parsing(query: str, terms: List[str]):
  textquery = TextQuery.from_str(query)
  query_terms = [str(term) for term in textquery.get_terms()]
  assert all(term in query_terms for term in terms)
  assert all(term in terms for term in query_terms)
  

@pytest.mark.parametrize("query,elastic_query", [
  ('mobility', '"mobility"'),
  ('robots and cats', '"robots" AND "cats"'),
  ('ppe and (covid or corona)', '"ppe" AND ("covid" OR "corona")'),
  ('process mining and NOT bitcoin and NOT dogecoin',
    '"process mining" AND NOT "bitcoin" AND NOT "dogecoin"'),
  ('xyz_robotics', '"xyz_robotics"'),
])
def test_query_to_string(query: str, elastic_query: str):
  """ We only check for rough matches because there are additional brackets
  in the TextQuery output (which are not necessary but also not harmful)."""
  textquery = TextQuery.from_str(query).to_str()
  assert query_contained_in_query(elastic_query, textquery)


@pytest.mark.parametrize("query_parts,query", [
  ([TextQueryTerm('mobility'), TextQueryOp('AND'), 
    TextQueryTerm('robots')], '"mobility" AND "robots"'),
  ([TextQueryTerm('mobility'), TextQueryOp('AND'), TextQuery.from_str('robots OR cats')],
    '"mobility" AND ("robots" OR "cats")'),
  ([TextQuery.from_str('dogs and bikes'), TextQueryOp('OR'), TextQuery.from_str('robots and cats')],
    '("dogs" AND "bikes") OR ("robots" AND "cats")'),
])
def test_query_list_parsing(query_parts: List, query: str):
  generated_query = TextQuery.from_list(query_parts).to_str()
  assert query_contained_in_query(query, generated_query)


@pytest.mark.parametrize("query,output", [
  ('urban mobility', 'NOT "urban mobility"'),
  ('cats and dogs', 'NOT "cats" OR NOT "dogs"'),
  ('robots and (bikes or scooters)', 'NOT "robots" OR (NOT "bikes" AND NOT "scooters")'),
])
def test_negation(query: str, output: str):
  textquery = TextQuery.from_str(query)
  textquery.negate()
  negated_query = textquery.to_str()
  assert query_contained_in_query(output, negated_query)


@pytest.mark.parametrize("query,output", [
  ('NOT (cats and dogs)', '(NOT "cats" OR NOT "dogs")'),
  ('NOT (cats or dogs)', '(NOT "cats" AND NOT "dogs")'),
])
def test_negation_substitutions(query: str, output: str):
  textquery = TextQuery.from_str(query)
  textquery.substitute_negations()
  substituted_query = textquery.to_str()
  assert query_contained_in_query(output, substituted_query)


@pytest.mark.parametrize("query,syns_fct,output", [
  ('mobility', lambda x: ['scooters'] if x == 'mobility' else [], 'mobility OR scooters'),
  ('cars AND bikes', lambda x: [f'many {x}'], 
    '("cars" OR "many cars") AND ("bikes" OR "many bikes")'),
])
def test_syns_fct_expansion(query: str, syns_fct: Callable, output: str):
  textquery = TextQuery.from_str(query)
  textquery.expand_with_syns_fct(syns_fct)
  expanded_query = textquery.to_str()
  assert query_contained_in_query(output, expanded_query)


@pytest.mark.parametrize("query,syns_map,output", [
  ('mobility', 
    {SYNONYM_TERMS_TYPE: [
      {'original': 'mobility', 'term': 'much mobility', 'source': 'arbitrary'}
    ]},
    '"mobility" OR "much mobility"'),
  ('cars AND vehicles AND bikes', 
    {SYNONYM_TERMS_TYPE: [
      {'original': 'cars', 'term': 'car', 'source': 'lemmatizer'},
      {'original': 'vehicles', 'term': 'vehicle', 'source': 'lemmatizer'},
    ]},
    '("cars" OR "car") AND ("vehicles" OR "vehicle")'),
])
def test_syns_map_expansion(query: str, syns_map: Dict, output: str):
  textquery = TextQuery.from_str(query)
  textquery.add_related_terms_from_map(syns_map)
  expanded_query = textquery.to_str()
  assert query_contained_in_query(output, expanded_query)
