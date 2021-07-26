from enum import Enum
import enum
import json
from typing import Iterable
import time
from resource import getrusage, RUSAGE_SELF
from typing import Optional, List

import spacy
import typer

app = typer.Typer()

@enum.unique
class SpacyVersion(str, Enum):
    SM = "sm"
    MD = "md"
    LG = "lg"
    TRF = "trf"

@enum.unique
class ComponentNames(str, Enum):
    NER = "ner"
    POS = "tagger"
    PARSER = "parser"
    LEMMA = "lemmatizer"

THE_TEXT = 'Hello how are you, I am well thank you, this is an example of a short text.' * 5

def text_generation(number_texts: int = 200) -> Iterable[str]:
    '''
    :param number_text: The number of times the text is repeated. This 
                        will determine the length of the returned iterable. The text
                        that is repeated is the following: 

                        `Hello how are you, I am well thank you, this is an example of a short text.`

    :returns: An iterable of identical Strings whereby the number of items in this list 
              is determined by the `number_text` argument.
    '''

    for _ in range(number_texts):
        yield THE_TEXT

@app.command()
def process_text(spacy_version: SpacyVersion = typer.Argument(SpacyVersion.SM, 
                                                     help='Name of the English spacy model to use',
                                                     case_sensitive=False),
                 components_to_include: Optional[List[ComponentNames]] = typer.Option(None,
                                                                                    "--include",
                                                                                    "-i", 
                                                                                    case_sensitive=False,
                                                                                    help='The NLP components to include from the English Spacy pipeline.'),
                 text_size: int = typer.Option(100, "--text-size", "-t", help='Number of texts to process, each text contains ~100 tokens.'),
                 batch_size: int = typer.Option(50, "--batch-size", "-b", help='Number of texts to process at once.'),
                 to_json: bool = typer.Option(False, "--json", "-j", help="Output in JSON")) -> None:
    """
    Given a spacy model version it will output how long and how much memory it took 
    that model to process the given texts. The output can be in JSON format 
    whereby the JSON will have the following structure: 
    
    {"model": "sm", "included": ["ner", "lemmatizer"], "text_size": 100, "batch_size": "50", 
     "time": "100", "model_load_memory": "120.2", "total_memory": "1200.1"}
    
    In this the units of time and memory are seconds and MB respectively.

    If the text-size is greater than batch-size then the spacy model will only 
    process batch-size number of texts at one time, and will carry on processing 
    that number of texts until all texts have been processed.
    """
    expanded_components_to_exclude = [value.value for value in ComponentNames]
    expanded_components_to_exclude.append('attribute_ruler')
    for component in components_to_include:
        if component.name == 'LEMMA':
            expanded_components_to_exclude.remove('lemmatizer')
            expanded_components_to_exclude.remove('attribute_ruler')
            expanded_components_to_exclude.remove('tagger')
        else:
            if component.value in expanded_components_to_exclude:
                expanded_components_to_exclude.remove(component.value)
    
    current_memory = getrusage(RUSAGE_SELF).ru_maxrss
    nlp = spacy.load(f"en_core_web_{spacy_version.value}", 
                     exclude=expanded_components_to_exclude)
    loading_model_memory = (getrusage(RUSAGE_SELF).ru_maxrss - current_memory) / 1000

    
    t = time.time()
    
    
    for doc in nlp.pipe(text_generation(text_size), batch_size=batch_size):
        load_doc = doc.text

    total_memory = (getrusage(RUSAGE_SELF).ru_maxrss - current_memory) / 1000
    total_time = time.time() - t
    if to_json:
        json_data = {"model": spacy_version.value,
                     "included": [component.value for component in components_to_include],
                     "text_size": text_size,
                     "batch_size": batch_size,
                     "time": total_time,
                     "model_load_memory": loading_model_memory,
                     "total_memory": total_memory}
        typer.echo(json.dumps(json_data))
    else:
        typer.echo(f'Time taken to process text: {total_time}\n'
                f'Using Spacy en_core_web_{spacy_version} model')
        typer.echo(f'Memory used to load model: {loading_model_memory} MB')
        typer.echo(f'Total Memory used: {total_memory} MB')

if __name__ == '__main__':
    app()