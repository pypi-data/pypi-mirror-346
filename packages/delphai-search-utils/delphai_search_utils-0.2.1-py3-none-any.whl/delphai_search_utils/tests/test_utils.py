from delphai_search_utils.utils import mask_conjunction, mask_stopwords
from delphai_search_utils.utils import is_masked, remove_mask, mask_elements_from_text
from delphai_search_utils.utils import split_with_indices
import pytest
import os
from typing import List, Dict, Tuple
os.environ['DELPHAI_ENVIRONMENT'] = 'development'


@pytest.mark.parametrize("query,output", [
  ("urban mobility in", "urban mobility __"),
  ("robots and cars after", "robots and cars _____"),
  ("robots and cars in germany", "robots and cars in germany")
])
def test_conjunction_masking(query: str, output: str):
  assert mask_conjunction(query) == output
  

@pytest.mark.parametrize("query,output", [
  ("urban mobility companies", "urban mobility _________"),
  ("urban mobility companies in Prague", "urban mobility _________ in Prague"),
  ("urban mobility founded after 2020", "urban mobility _______ after 2020"),
])
def test_mask_stopwords(query: str, output: str):
  assert mask_stopwords(query) == output


@pytest.mark.parametrize("query,output", [
  ('xyz_robotics company', 'xyz_robotics'),
])
def test_unmasking(query: str, output: str):
  masked_query = mask_stopwords(query)
  unmasked_query = remove_mask(masked_query)
  assert unmasked_query == output


@pytest.mark.parametrize("query,output", [
  ("____", True),
  ("urban", False),
  ("__ban", False),
])
def test_is_masked(query: str, output: bool):
  assert is_masked(query) == output


@pytest.mark.parametrize("query,output", [
  ("urban mobility ________", "urban mobility"),
  ("mobility ________ _____ after 2020", "mobility after 2020"),
  ("urban mobility", "urban mobility")
])
def test_remove_mask(query: str, output: str):
  assert remove_mask(query) == output


@pytest.mark.parametrize("query,labels,output", [
  ('urban mobility in germany', [{'start_index': 18, 'end_index': 25}], 'urban mobility __ _______'),
  ('german cars', [{'start_index': 0, 'end_index': 6}], '______ cars'),
])
def test_mask_elements(query: str, labels: List[Dict], output: str):
  assert mask_elements_from_text(query, labels, remove_conjunctions=True) == output


@pytest.mark.parametrize("query,output", [
  ('urban mobility in germany', [('urban', 0), ('mobility', 6), ('in', 15), ('germany', 18)]),
  ('electric vehicles', [('electric', 0), ('vehicles', 9)]),
  ('robots and cats', [('robots', 0), ('and', 7), ('cats', 11)]),
])
def test_index_splitting(query: str, output: List[Tuple[int, int]]):
  tokens = list(split_with_indices(query))
  assert len(tokens) == len(query.split())
  assert all(token in query for token, _ in tokens)
  assert all(' ' not in token for token, _ in tokens)
  assert all(query[start_index:].startswith(token) for token, start_index in tokens)
