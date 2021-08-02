import json
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer()

@app.command()
def filter_files(meta_data_file: Path = typer.Argument(...,
                                                       exists=True,
                                                       dir_okay=False,
                                                       file_okay=True, 
                                                       help="The file path to the British Library 19th Century book META data. Instead of the whole meta data file you can also use the `id_date_meta_data.json` file that is whithin this repository."), 
                 input_folder: Path = typer.Argument(..., 
                                                     exists=True,
                                                     dir_okay=True,
                                                     file_okay=False,
                                                     help="The top level directory the books were downloaded to e.g. /home/json. In the root directory of this repositories README this is called the `DIRECTORY_TO_BOOKS`"), 
                 output_file: Path = typer.Argument(...,
                                                    help="The file that will contain the relative file paths of all books that are in the given decade. The file paths will be relative to the `input_folder`. e.g. `0118/011833856_01_text.json`"),
                 language: Optional[str] = typer.Option(None, help="(NOTE this is case in-sensitive) Filter by the language of that the book was written in e.g. english. The language name comes from the description tag of the BCP: 47 registry which can be found here: https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry"),
                 decade: Optional[int] = typer.Option(None, help="Filter by the decade the book was published e.g. 1890 or 1880.")
                 ) -> None:
    '''
    Given a filter(s) such as decade and/or language it will find all books 
    that match the filtered criteria through the meta data, and copy the relative
    file path of that book from the `input_folder` and write it on a new line 
    in the `output_file`.
    '''
    if isinstance(language, str):
        language = language.lower()

    with meta_data_file.open('r') as meta_fp:
        book_data = json.load(meta_fp)
        with output_file.open('w') as output_fp:
            for book in book_data:
                # Filter by decade
                if isinstance(decade, int):
                    if 'date' not in book:
                        continue
                    date = int(book['date'])
                    book_decade = (date // 10) * 10
                    if book_decade != decade:
                        continue
                # Filter by language
                if isinstance(language, str):
                    if 'language' not in book:
                        continue
                    book_language = book['language'].lower()
                    if book_language != language:
                        continue
                
                _id = book['identifier']
                sub_folder_name = _id[:4]
                sub_folder = Path(input_folder, sub_folder_name)
                if not sub_folder.exists():
                    continue
                # Some books have multiple volumes, therefore have multiple book files
                for file_name in sub_folder.iterdir():
                    if _id in file_name.stem:
                        output_fp.write(f'{sub_folder_name}/{file_name.name}\n') 

if __name__ == "__main__":
    app()