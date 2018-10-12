# autocomplete-metadata
Search-as-you-type experiment as a web service

## Development
Well, I suppose you need to make your database in the exact manner as the models exist?  Or, you know, have the correct ones already.  This was more for my own curiosity and amusement.  Everything else you need is in the Pipfile.

Anyway, here's Pipenv.

```sh
cd autocomplete-metadata
pipenv install
pipenv shell
```

You'll want to duplicate `config.example.py` as `config.py` and add the appropriate DB credentials for exporting data that this service can use.  To export that data to a JSON file:

```sh
python utilities/create_metadata_json.py OUTPUT_FILE_LOCATION
```

Then to run the server, pass the location of the file you just created to the server:

```sh
python server.py OUTPUT_FILE_LOCATION
```

This will start the server on flask's default port.