import json
from pathlib import Path
from typing import List, Dict

import typer

app = typer.Typer()

@app.command()
def extract_id_date_from_meta_data(meta_data_file: Path = typer.Argument(...,
                                                                         exists=True,
                                                                         dir_okay=False,
                                                                         file_okay=True,  
                                                                         help="The file path to the British Library 19th Century book META data."),
                                   output_file: Path = typer.Argument(...,
                                                                      help="File that will contain a JSON Array, where each element in the Array is an Object with two keys: 1. identifier and 2. date. Each Object element represents one book from the `meta_data_file`")
                                                                         ) -> None:
    with meta_data_file.open('r') as meta_fp:
        book_data = json.load(meta_fp)
        id_date: List[Dict[str, str]] = []
        for book in book_data:
            if 'date' in book:
                _id = book['identifier']
                date = book['date']
                id_date.append({'identifier': _id, 'date': date})
        with output_file.open('w') as output_fp:
            json.dump(id_date, output_fp)


if __name__ == "__main__":
    app()