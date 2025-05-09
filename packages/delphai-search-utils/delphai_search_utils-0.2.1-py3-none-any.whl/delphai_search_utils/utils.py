from sacremoses import MosesTruecaser
from os.path import join
from nltk.stem.snowball import SnowballStemmer
import logging
import nltk
from copy import deepcopy
from itertools import groupby
import json
import requests
import bson
from typing import Tuple, List, Generator
# get data path in a reproducible way
import os
this_dir, this_filename = os.path.split(__file__)
data_path = os.path.join(this_dir, "data")

mtr = MosesTruecaser(join(data_path, 'demonyms.truecasemodel'))

special_stopwords = ['compani', 'found',]
stemmer = SnowballStemmer(language='english')


def mask_conjunction(query_str: str) -> str:
    """ Removes conjunctions at the end of the query which are very likely
    not related to the actual query terms but just left overs from filters etc."""
    if len(query_str.strip()) == 0:
        return query_str
    pos_tags = nltk.pos_tag(nltk.word_tokenize(query_str))
    if not pos_tags:
        return query_str
    # iterate through pos tags and keep absolute string positions in mind
    for i, ((tok, pos), (_, pos_tag)) in enumerate(zip(split_with_indices(query_str), pos_tags)):
        if i == len(pos_tags) - 1 or is_masked(pos_tags[i + 1][0]):
            if pos_tag in ['CC', 'IN']:
                query_str = mask_substr(query_str, pos, pos + len(tok))
    return query_str


def mask_stopwords(query_str: str) -> str:
    # remove special_stopwords
    query_stops = [word for word in query_str.split() if stemmer.stem(word) in special_stopwords]
    for stop_word in query_stops:
        stop_index = query_str.index(stop_word)
        if stop_index >= 0:
            query_str = mask_substr(query_str, stop_index, stop_index + len(stop_word))
    return query_str


def is_masked(substring: str) -> bool:
    return (all(char == '_' for char in substring))


def remove_mask(query_str: str) -> str:
    """" Remove masked words;
    Doesn't guarantee that character indices stay the same afterwards,
    e.g. if masked words are removed in the middle of the query.
    We also don't want to remove underscores from inside names for example;
    e.g. 'xyz_robotics' should search for 'xyz_robotics' and not 'xyz robotics' """
    tokens = query_str.split()
    non_mask_tokens = [token for token in tokens if not all(char == '_' for char in token)]
    return ' '.join(non_mask_tokens)


def mask_substr(query_str: str, start_index: int, end_index: int) -> str:
    """ replaces the element between the given indices with underscores so that
    it is ignored for the subsequent filter detection; they are removed afterwards
    but kept for now to keep the correct character indices afterwards.
    This is not an ideal solution, so replacing it e.g. with a custom class which has
    a 'hide'-flag for each token would seem more resilient. (spaCy could do that..?)"""
    return query_str[:start_index] + '_' * (end_index - start_index) + query_str[end_index:]


def mask_elements_from_text(query_str: str, labels: List, remove_conjunctions=False) -> str:
    """ Removes the given labels from the query string and potentially also
    conjunctions; returns a cleaned query string."""
    for label in labels:
        query_str = mask_substr(query_str, label['start_index'], label['end_index'])
        if remove_conjunctions:
            query_str = mask_conjunction(query_str)
            query_str = mask_conjunction(query_str)
    return query_str


# https://stackoverflow.com/a/13734815
def split_with_indices(query: str, sep: str = ' ')\
        -> Generator[Tuple[str, int], None, None]:
    """ Splits the string by the given separator and returns all tokens
    together with their character start indices."""
    p = 0
    for k, g in groupby(query, lambda x: x == sep):
        q = p + sum(1 for i in g)
        if not k:
            yield query[p:q], p
        p = q


def query_contained_in_query(query: str, reference_query: str):
    """ Check if query is contained in reference_query."""
    # check if each character from elastic_query appears in textquery, in same order.
    ref_index = 0
    for c in query:
        try:
            while c != reference_query[ref_index]:
                ref_index += 1
            if c == reference_query[ref_index]:
                ref_index += 1
            else:
                return False
        except IndexError:
            return False
    return True
