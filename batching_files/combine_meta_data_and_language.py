import json
from pathlib import Path
from typing import List, Dict

import typer

app = typer.Typer()

@app.command()
def combine(meta_data_file: Path = typer.Argument(..., exists=True, dir_okay=False, file_okay=True, help="File that contains meta data"),
            language_meta_data_file: Path = typer.Argument(..., exists=True, dir_okay=False, file_okay=True, help="File that cotain language meta data"),
            output_file: Path = typer.Argument(..., help="File that will contain a JSON Array, where each element in the Array is an Object with three keys: 1. identifier, 2. date, and 3. language. Each Object element represents one book from the `meta_data_file`")) -> None:
    # These ID's relate to books that have more than one volume, of which at least 
    # two volumes in each books has a different language associated with it.
    _ids_to_ignore = ["000228355", "000459957", "000624024", "001671636", 
                      "001691448", "002654658", "002722435", "003376382"]
    
    meta_data: Dict[str, Dict[str, str]] = {}
    with language_meta_data_file.open('r') as language_meta_fp:
        for line in language_meta_fp:
            line = line.strip()
            if line:
                data = json.loads(line)
                _id = data['filename'].split('_')[0]
                if _id in _ids_to_ignore:
                    continue
                language = data['language']
                meta_data[_id] = {'language': language}
                
    with meta_data_file.open('r') as meta_data_fp:
        for data in json.load(meta_data_fp): 
            _id = data['identifier']
            if _id in meta_data:
                meta_data[_id]['date'] = data['date']
    
    array_meta_data = [{'identifier': key, 'date': value['date'], 'language': value['language']} 
                       for key, value in meta_data.items()]
    
    with output_file.open('w') as output_fp:
        json.dump(array_meta_data, output_fp)


if __name__ == "__main__":
    app()