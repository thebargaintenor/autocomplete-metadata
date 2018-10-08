from operator import attrgetter

from completion import (
    Completion,
    Repository,
    tokenize_name
)


def starts_with_term(tokens: list, term: str) -> bool:
    return any(t.startswith(term) for t in tokens)


def all_match(terms: set, tokens: list) -> bool:
    return all(starts_with_term(tokens, term) for term in terms)


def match_terms(terms: set, repository: list) -> list:
    return list(course for course in repository if all_match(terms, course.tokens))


def sort_completions(completions) -> list:
    key_function = attrgetter('name')
    return sorted(completions, key=key_function)


def find_completions(query: str, repository: Repository) -> list:
    if query:
        terms = set()
        tokens = tokenize_name(query)
        for t in tokens:
            terms.add(t)

        author_completions = {}  # type: dict
        for match in match_terms(terms, repository.authors):
            if match.id not in author_completions:
                author_completions[match.id] = match

        course_completions = {}  # type: dict
        for match in match_terms(terms, repository.courses):
            if match.id not in course_completions:
                course_completions[match.id] = match

        # Order based on parity with monolith behavior
        completions = []  # type: list
        completions.extend(
            sort_completions(author_completions.values())
        )
        completions.extend(
            sort_completions(course_completions.values())
        )
        return completions
    else:
        return []


def display_completions(completions: list) -> list:
    titles = list(c.name for c in completions)
    return titles
