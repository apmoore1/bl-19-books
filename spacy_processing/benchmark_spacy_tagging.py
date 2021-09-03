import json
import tempfile
from resource import getrusage, RUSAGE_SELF
from pathlib import Path
import time
from typing import Optional, List

import typer

from spacy_tagging import process_text, ComponentNames, text_generator



app = typer.Typer()

@app.command()
def benchmark(components_to_include: Optional[List[ComponentNames]] = typer.Option(None,
                                                                                   "--include",
                                                                                   "-i", 
                                                                                   case_sensitive=False,
                                                                                   help='The NLP components to include from the English Spacy md pipeline.'),):
    '''
    Given the components of the spaCy model to use within an English medium spaCy 
    model, it will output how long and how much memory the spaCy model requires to 
    process 10 pages of a British Library book. This book data can be found in 
    `./test_data/real_book_data` directory. The output will be in JSON format, for
    example:

    {"time": 22.3, "total_memory": 350.36, "compoenets": ["ner"]}
     
    '''
    real_book_data_directory = Path(__file__, '..', 'test_data', 'real_book_data').resolve()

    with tempfile.TemporaryDirectory() as temp_dir:
        tempdir_path = Path(temp_dir)
        t = time.time()
        current_memory = getrusage(RUSAGE_SELF).ru_maxrss
        process_text(real_book_data_directory, tempdir_path, components_to_include)
        total_memory = (getrusage(RUSAGE_SELF).ru_maxrss - current_memory) / 1000
        total_time = time.time() - t

        compoenets = [component.value for component in components_to_include]
        data = {'time': total_time, 'total_memory': total_memory, 
                'compoenets': compoenets}
        typer.echo(f'{json.dumps(data)}')

if __name__ == '__main__':
    app()