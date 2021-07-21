import json
from pathlib import Path
from typing import List

import typer

def main(identifier: str = typer.Argument(..., help='9 digit string that uniquely identifies a book e.g. `000741339`', 
                                          metavar='Identifier'),
         book_fp: Path = typer.Argument(Path('.','book_data.json'), 
                                        help='The file path to the British Library 19th Century book META data.',
                                        metavar='Book_Meta_File_Path', exists=True,
                                        file_okay=True, dir_okay=False, writable=False,
                                        readable=True, resolve_path=True),
        fields_to_remove: List[str] = typer.Option(['imgs', 'datefield', 'shelfmarks', 'edition', 'issuance', 'corporate'], '--remove', '-rm', 
                                                   help='Field/Key not to print')):
    '''
    Given the file path to the British Library 19th Century book Meta data and 
    the unique identifier of a book it will return that books meta data in 
    a pretty print format.
    '''
    with book_fp.open('r') as book_json:
        book_data = json.load(book_json)
        for book in book_data:
            _id = book['identifier']
            if _id == identifier:
                for key, value in book.items():
                    if key in fields_to_remove:
                        continue
                    else:
                        key_print = typer.style(f'{key}', fg='bright_blue', bg='black')
                        break_print = typer.style(' : ', fg='white', bg='black')
                        value_print = typer.style(f'{value}', fg='yellow', bg='black')
                        typer.echo(key_print + break_print + value_print)

if __name__ == '__main__':
    typer.run(main)