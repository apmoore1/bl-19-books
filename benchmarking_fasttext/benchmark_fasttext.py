import enum
import json
from pathlib import Path
import timeit
from resource import getrusage, RUSAGE_SELF
from timeit import repeat

import fasttext
import typer

@enum.unique
class ModelNames(str, enum.Enum):
    LARGE = "large"
    SMALL = "small"

app = typer.Typer()

@app.command()
def process_text(model_path: Path = typer.Argument(...,
                                                   exists=True,
                                                   dir_okay=False,
                                                   file_okay=True,
                                                   resolve_path=True,
                                                   help="File path to either the large or small FastText language identification model."),
                model_name: ModelNames = typer.Argument(..., case_sensitive=False, help="Name of the model e.g. large or small"),
                to_json: bool = typer.Option(False, "--json", "-j", help="Output in JSON")) -> None:
    '''
    Given a FastText model it will output how long and hom much memory it took 
    that model to process a text that is 11,000 tokens long. The time of processing 
    is the best mean time over 5 repeats of running the model 100 times on 11,000 tokens.
    The reason for doing so many repeats is to better capture the speed of the models, 
    as they are very quick, roughly 11,000 tokens is around 0.002 seconds.

    The output can be in JSON format whereby the JSON will have the following 
    structure: 
    
    {"model": "small", "text_size": 11000, 
     "time": "0.00228", "model_load_memory": "3.658", "total_memory": "4.07"}

    In this the units of time and memory are seconds and MB respectively.
    '''
    current_memory = getrusage(RUSAGE_SELF).ru_maxrss

    model = fasttext.load_model(str(model_path))
    loading_model_memory = (getrusage(RUSAGE_SELF).ru_maxrss - current_memory) / 1000
    
    text = "this is very much pas Bonjour comment another bit of data" * 1000
    total_time = min(timeit.repeat('model.predict(text, k=1)', number=100, repeat=5, globals=locals()))    
    total_time = total_time / 100
    a = model.predict(text)
    total_memory = (getrusage(RUSAGE_SELF).ru_maxrss - current_memory) / 1000
    

    if to_json:
        json_data = {"model": model_name,
                     "text_size": 110000,
                     "time": total_time,
                     "model_load_memory": loading_model_memory,
                     "total_memory": total_memory}
        typer.echo(json.dumps(json_data))
    else:
        typer.echo(f'Time taken to process text: {total_time}\n'
                   f'Using: {model_name}')
        typer.echo(f'Memory used to load model: {loading_model_memory} MB')
        typer.echo(f'Total Memory used: {total_memory} MB')

if __name__ == "__main__":
    app()