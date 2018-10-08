from autocomplete import (
    display_completions,
    find_completions
)
from completion import (
    Completion,
    Repository
)

repository = Repository(
    authors=[
        Completion(
            id='4',
            name='Jared Gilbert',
            tokens=['jared', 'gilbert']
        )
    ],
    courses=[
        Completion(
            id='1',
            name='Fundamentals of Angular 4',
            tokens=['fundamentals', 'of', 'angular', '4', 'ha', 'phan']
        ),
        Completion(
            id='2',
            name='Angular Components and Stuff',
            tokens=['angular', 'components', 'and', 'stuff', 'ha', 'phan']
        ),
        Completion(
            id='3',
            name='React for Lazy People',
            tokens=['react', 'for', 'lazy', 'people']
        )
    ]
)


def test_no_query_yields_empty_list():
    got = find_completions(None, repository)
    want = []
    assert got == want


def test_no_matches_yields_empty_list():
    got = find_completions('java', repository)
    want = []
    assert got == want


def test_angular_matches_two_courses():
    got = len(find_completions('angular', repository))
    want = 2
    assert got == want


def test_angular_fundamentals_matches_one_course():
    got = len(find_completions('angular fundamentals', repository))
    want = 1
    assert got == want


def test_fundamental_angular_matches_one_course():
    got = len(find_completions('fundamental angular', repository))
    want = 1
    assert got == want


def test_ha_phan_matches_two_courses():
    got = len(find_completions('Ha Phan', repository))
    want = 2
    assert got == want


def test_jared_matches_one_author():
    got = len(find_completions('jared', repository))
    want = 1
    assert got == want


def test_display_results_are_sorted():
    got = display_completions(find_completions('angular', repository))
    want = ['Angular Components and Stuff', 'Fundamentals of Angular 4']
    assert got == want
