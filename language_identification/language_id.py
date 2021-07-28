from collections import Counter
import json
from pathlib import Path
from typing import Iterable, Tuple, Optional

import fasttext
from langcodes import Language, standardize_tag
import typer

app = typer.Typer()

def text_generator(book_file: Path) -> Iterable[Tuple[int, str]]:
    '''
    :param book_file: File path to a British library book file.
    :returns: Yields the page number and text of that page for all pages in the 
              given book file. NOTE, if the page contains NO text it will be 
              skipped and therefore not yielded from this function.
    '''
    with book_file.open('r') as fp:
        data = json.load(fp)
        for page in data:
            if page[1].strip():
                yield (page[0], page[1])

@app.command()
def process_file(model_path: Path = typer.Argument(...,
                                                   exists=True,
                                                   dir_okay=False,
                                                   file_okay=True,
                                                   resolve_path=True,
                                                   help="File path to either the large or small FastText language identification model."),
                 file_to_process: Path = typer.Argument(..., exists=True,
                                                        dir_okay=False,
                                                        file_okay=True,
                                                        resolve_path=True,
                                                        help="File path to a British Library book file."),
                 output_file: Path = typer.Argument(..., help="File to store the JSON output, file is opened in append mode."),
                 exclude_filename: bool = typer.Argument(..., help="If True then the `filename` key will not be in the output file"),
                 model_threshold: Optional[float] = typer.Option(None, "--threshold", "-t", help="Probability threshold for the model to output a label e.g. `0.9` would mean the model has to be 90% confident that the language label is correct.")
                 ) -> None:
    '''
    Given a FastText language ID model and a British Library book file. It will 
    write the following JSON to the `output_file`:
    
    {
        "filename": "file_name",
        "language": "Main language name", 
        "language_extras": 
        {
            "Main language name": 
            {
                "BCP 47 code": "language code", 
                "count": 4, 
                "proportion": 0.8
            },
            "Minor language name":
            {
                "BCP 47 code": "language code", 
                "count": 1, 
                "proportion": 0.2
            }
        }
    }

    Whereby the Main language name could be English and the Minor language name 
    could be Spanish for example. The count is based on the number of pages in 
    the book that have been identified as that language. The proportion is the 
    count of that language divided total number of pages with text e.g. 4/5 = 0.8.
    The filename is the name of the `file_to_process` e.g. if the `file_to_process` is
    /home/user/bl_book.json then the filename is `bl_book`.

    If the program cannot identify any language in the book file, for example if
    the book file is empty then the JSON output will be:

    {
        "filename": "file_name",
        "language": null
    } 

    null will be equal to None in Python.
    '''
    model = fasttext.load_model(str(model_path))
    language_counts = Counter()
    for page_number, page in text_generator(file_to_process):
        language_probability = ()
        if not isinstance(model_threshold, float):
            language_probability = model.predict(page, k=1)
        else:
            language_probability = model.predict(page, k=1, threshold=model_threshold)
        # Checks that a language probability exists
        if language_probability[0]:
            language_label = language_probability[0][0]
            language_counts.update([language_label])
    
    total_count = sum(language_counts.values())
    # Add detailed language data
    language_specific_data = {}
    for language, count in language_counts.items():
        language = language.replace('__label__', '', 1)
        language_code = standardize_tag(language)
        language_name = Language.get(language).describe('en')['language']
        language_specific_data[language_name] = {'BCP 47 code': language_code,
                                                 'count': count,
                                                 'proportion': count / total_count}
    
    most_common_language = language_counts.most_common(1)
    output_data = {}
    if not exclude_filename:
        output_data["filename"] = file_to_process.stem
    
    if most_common_language:
        most_common_language = most_common_language[0][0]
        most_common_language = most_common_language.replace('__label__', '', 1)
        most_common_language = Language.get(most_common_language).describe('en')['language']
        output_data["language"] = most_common_language
        output_data["language_extras"] = language_specific_data
    else:
        output_data["language"] = None

    with output_file.open('a') as output_fp:
        json.dump(output_data, output_fp)
        output_fp.write("\n")


if __name__ == "__main__":
    app()
