from collections import defaultdict
import json
import logging
from pathlib import Path
from typing import Iterable

import typer

app = typer.Typer()

def yield_book_directories(top_level_directory: Path) -> Iterable[Path]:
    for book_directory in top_level_directory.iterdir():
        if book_directory.is_dir():
            yield book_directory

def yield_book_files(book_directory: Path) -> Iterable[Path]:
    for book_file in book_directory.iterdir():
        if book_file.suffix == '.json':
            yield book_file

def page_generator(book_file: Path) -> Iterable[str]:
    with book_file.open('r') as fp:
        data = json.load(fp)
        for page in data:
            if page[1].strip():
                yield page[1]

@app.command()
def character_count(top_level_book_directory: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True,
                                                                    help="The directory that contains the book corpus (OCR text), after downloading it and un-compressing it, should be called `json` "), 
                    results_file: Path = typer.Argument(..., help="File to store the output of this script in JSON format."), 
                    log_file: Path = typer.Argument(..., help="Log file which will generate on each new line the number of directories within `top_level_book_directory` that have been processed, a directory is processed if all files within that direcotry have been processed.")) -> None:
    '''
    This script will find the maximum size length page per book, for each book 
    in the `top_level_book_directory`. The `result_file` will contain that 
    following JSON data:

    The file contains one JSON object which has 4 keys, of which each value in 
    all 4 keys is a JSON array of the same length, whereby the index of each array 
    link to each e.g. the value at index 1 of "book_name" is the book name of 
    the "max_page_characters" value at index 1:

    1. "book_directory" -- The name of the parent directory that book file came 
    from e.g. `0007`.
    
    2. "book_name" -- The file name of the book, from the book name you 
    can get the books volume in this case it is `01`, each volume links to the 
    same meta data identifier, in this case `000741339` 
    e.g. `000741339_01_text`
    
    3. "meta_data_identifier" -- The unique identifier that links the book file 
    to the book record in the meta data. In the meta data this is called the 
    `identifier` e.g. `000741339`
    
    4. "max_page_characters" -- The number of characters in the longest page.

    A note, the `log_file` is created for debugging purposes, once the script 
    has successfully completed this `log_file` can be deleted.
    '''
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    results = defaultdict(list)
    for index, book_directory in enumerate(yield_book_directories(top_level_book_directory)):
        book_directory_name = book_directory.stem
        for book_file in yield_book_files(book_directory):
            max_number_characters = 0
            for page in page_generator(book_file):
                number_characters = len(page)
                if number_characters > max_number_characters:
                    max_number_characters = number_characters
            results["book_directory"].append(book_directory_name)
            book_file_name = book_file.stem
            results["book_name"].append(book_file_name)
            results["meta_data_identifier"].append(book_file_name.split('_')[0])
            results["max_page_characters"].append(max_number_characters)

        logger.info(f'Book directory index: {index} processed.')
    results = dict(results)
    with results_file.open('w') as results_fp:
        json.dump(results, results_fp)

        


if __name__ == "__main__":
    app()



