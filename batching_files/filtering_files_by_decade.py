import json
from pathlib import Path

import typer

app = typer.Typer()

@app.command()
def filter_by_decade(deacde: int = typer.Argument(..., help="Decade the book was published e.g. 1890 or 1880 to filter books by."), 
                     meta_data_file: Path = typer.Argument(...,
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
                                                        help="The file that will contain the relative file paths of all books that are in the given decade. The file paths will be relative to the `input_folder`. e.g. `0118/011833856_01_text.json`")
                     ) -> None:
    '''
    Given a deacde e.g. 1890 it will find all books published in that decade, 
    through the meta data, and copy the relative file path of that book from 
    the `input_folder` and write it on a new line in the `output_file`.
    '''

    with meta_data_file.open('r') as meta_fp:
        book_data = json.load(meta_fp)
        with output_file.open('w') as output_fp:
            for book in book_data:
                if not book['date']:
                    continue
                date = int(book['date'])
                book_decade = (date // 10) * 10
                if book_decade != deacde:
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