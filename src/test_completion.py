from uuid import uuid4

from completion import (
    Completion,
    parse_author_record,
    parse_course_record,
    tokenize_name,
    tokenize_tag
)


def test_name_tokenizes_as_lowercase_list():
    name = 'This is a Title'
    got = tokenize_name(name)
    want = ['this', 'is', 'a', 'title']
    assert got == want


def test_no_name_tokenizes_as_empty_list():
    got = tokenize_name(None)
    want = []
    assert got == want


def test_tag_tokenizes_as_lowercase_list():
    tag = '3d-rendering'
    got = tokenize_tag(tag)
    want = ['3d', 'rendering']
    assert got == want


def test_tag_name_tokenizes_as_empty_list():
    got = tokenize_tag(None)
    want = []
    assert got == want


def test_valid_course_record_parses_as_completion_object():
    id = str(uuid4())
    valid_record = {
        'id': id,
        'title': 'This is a Title',
        'authors': ['Some Dude'],
        'tags': []
    }

    course_tokens = ['this', 'is', 'a', 'title', 'some', 'dude']

    got = parse_course_record(valid_record)
    want = Completion(id=id, name='This is a Title', tokens=course_tokens)
    assert got == want


def test_invalid_course_record_parses_as_none():
    invalid_record = {
        'id': None,
        'authors': [],
        'tags': []
    }

    got = parse_course_record(invalid_record)
    want = None
    assert got == want


def test_valid_author_record_parses_as_completion_object():
    id = str(uuid4())
    valid_record = {
        'id': id,
        'name': 'Some Dude',
        'tags': []
    }

    author_tokens = ['some', 'dude']

    got = parse_author_record(valid_record)
    want = Completion(id=id, name='Some Dude', tokens=author_tokens)
    assert got == want


def test_invalid_author_record_parses_as_none():
    invalid_record = {
        'id': None,
        'tags': []
    }

    got = parse_author_record(invalid_record)
    want = None
    assert got == want

