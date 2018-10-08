import attr
import json
import re
import sys
from typing import Optional


@attr.s()
class Completion():
    id = attr.ib(type=str)
    name = attr.ib(type=str)
    tokens = attr.ib(type=list)


@attr.s()
class Repository():
    authors = attr.ib(type=list)
    courses = attr.ib(type=list)


def tokenize_name(name: str) -> list:
    return name.lower().split() if name else []


def tokenize_tag(tag: str) -> list:
    return re.split('[ -]', tag.lower()) if tag else []


def tokenize_names(names: list) -> list:
    tokens = []
    for name in names:
        tokens.extend(tokenize_name(name))
    return tokens


def parse_course_record(record: dict) -> Optional[Completion]:
    try:
        tokens = tokenize_name(record['title'])
        if record['authors']:
            tokens.extend(tokenize_names(record['authors']))

        return Completion(
            id=record['id'],
            name=record['title'],
            tokens=tokens
        )
    except:
        return None


def get_courses(course_records: list) -> list:
    return list(
        filter(None,
            (parse_course_record(c) for c in course_records)
        )
    )


def get_courses_from_json(repo_blob: dict) -> list:
    return get_courses(repo_blob['courses']) if 'courses' in repo_blob else []


def parse_author_record(record: dict) -> Optional[Completion]:
    try:
        return Completion(
            id=record['id'],
            name=record['name'],
            tokens=tokenize_name(record['name'])
        )
    except:
        return None


def get_authors(author_records: list) -> list:
    return list(
        filter(None,
            (parse_author_record(c) for c in author_records)
        )
    )


def get_authors_from_json(repo_blob: dict) -> list:
    return get_authors(repo_blob['authors']) if 'authors' in repo_blob else []


def load_repository_from_file(file_name: str) -> Repository:
    with open(file_name, 'r') as course_file:
        repo_blob = json.load(course_file)
        return Repository(
            courses=get_courses_from_json(repo_blob),
            authors=get_authors_from_json(repo_blob)
        )


def main():
    file_name = sys.argv[1]
    courses = load_repository_from_file(file_name)
    print('{} courses found.'.format(len(courses)))

if __name__ == '__main__':
    main()
