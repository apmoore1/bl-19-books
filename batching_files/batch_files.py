from typing import List
from pathlib import Path
import shutil

import typer

app = typer.Typer()

@app.command()
def batch(batch_size: int = typer.Argument(..., help="Maximum number of files per batch folder."),
          book_folder: Path = typer.Argument(..., 
                                             exists=True,
                                             dir_okay=True,
                                             file_okay=False,
                                             help="The top level directory the books were downloaded to e.g. /home/json. In the root directory of this repositories README this is called the `DIRECTORY_TO_BOOKS`"), 
          extracted_file_names_file: Path = typer.Argument(...,
                                                           exists=True,
                                                           dir_okay=False,
                                                           file_okay=True,
                                                           help="The file that contains the relative file paths of all books that are to be batched. The file paths will be relative to the `book_folder`. e.g. `0118/011833856_01_text.json`"),
          batch_folder: Path = typer.Argument(..., exists=False, help="Folder that will contain all of the batch folders.")
    ) -> None:
    '''
    Given a batch size, *N*, it will copy *N* files from the book folder to a 
    new sub folder within `batch_folder`, these *N* files will have come from 
    the list of `extracted_file_names_file`. This will be repeated until all 
    file names from the `extracted_file_names_file` have been copied to a sub folder 
    within `batch_folder`. Each batch of *N* files will be saved to a separate 
    sub folder within `batch_folder` whereby the first batch will be saved to 
    sub folder `0` and the last to sub folder *M* if there are *M* batches of 
    *N* files in the `extracted_file_names_file`.
    '''

    def copy_files_to_folder(files_to_copy: List[Path], folder_to_copy_too: Path
                             ) -> None:
        '''
        Given a list of files to copy, it will copy these files to the folder, 
        whereby it will be saved in that folder as same file name.
        '''
        for file_to_copy in files_to_copy:
            copy_file_path = Path(folder_to_copy_too, file_to_copy.name)
            shutil.copyfile(file_to_copy, copy_file_path)

    batch_number = 0
    
    with extracted_file_names_file.open('r') as extracted_fp:
        file_paths: List[Path] = []
        for index, line in enumerate(extracted_fp):
            # If the count starts at 0, 0 modules (%) anything is 0
            count = index + 1
            line = line.strip()
            if not line:
                continue
            
            file_path = Path(book_folder, *line.split('/'))
            file_paths.append(file_path)
            if (count % batch_size) == 0:
                sub_batch_folder = Path(batch_folder, str(batch_number))
                sub_batch_folder.mkdir(parents=True)
                copy_files_to_folder(file_paths, sub_batch_folder)
                batch_number += 1
                file_paths = []
        if file_paths:
            sub_batch_folder = Path(batch_folder, str(batch_number))
            sub_batch_folder.mkdir(parents=True)
            copy_files_to_folder(file_paths, sub_batch_folder)
            file_paths = []

if __name__ == "__main__":
    app()