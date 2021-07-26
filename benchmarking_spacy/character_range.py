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
def character_count(top_level_book_directory: Path, results_file: Path, 
                    log_file: Path) -> None:
    
    # logs to stdout
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



