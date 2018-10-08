from flask import (
    Flask,
    request
)
import json
import sys

from autocomplete import (
    display_completions,
    find_completions
)
from completion import load_repository_from_file

repository_path = sys.argv[1]
print('Attempting to load {}...'.format(repository_path))

print('Loading repository...')
repository = load_repository_from_file(repository_path)
print('Repository loaded!')

app = Flask(__name__)


@app.route('/complete', methods=['GET'])
def complete():
    query = request.args.get('query', '')
    if query:
        completions = display_completions(find_completions(query, repository))
        body = {
            'completions': completions
        }
        response = app.response_class(
            response=json.dumps(body),
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(status=400)
    return response

if __name__ == '__main__':
    app.run(debug=True)