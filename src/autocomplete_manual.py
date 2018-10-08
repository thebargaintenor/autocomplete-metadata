#! /usr/bin/env python3

import sys

from autocomplete import (
    find_completions,
    display_completions
)
from completion import load_repository_from_file

repository_file_name = sys.argv[1]
query = sys.argv[2]

repository = load_repository_from_file(repository_file_name)
completions = find_completions(query, repository)

print('\n'.join(display_completions(completions)))
