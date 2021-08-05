import json
from pathlib import Path

import typer
import en_core_web_md

app = typer.Typer()

@app.command()
def create_tests(output_folder: Path, include_lemma: bool) -> None:
    test_folder = Path(__file__, '..', 'book_folder').resolve()
    test_files = [Path(test_folder, 'test_example.json'),
                Path(test_folder, 'test_example_1.json')]
    
    output_folder.mkdir(parents=True, exist_ok=True)
    output_files = [Path(output_folder, 'test_example.tsv'), 
                    Path(output_folder, 'test_example_1.tsv')]

    nlp = en_core_web_md.load()

    for index, test_file in enumerate(test_files):
        output_file = output_files[index]
        with output_file.open('w') as output_fp:
            if include_lemma:
                output_fp.write('token\tlemma\tpos\tner\tpage\n')
            else:
                output_fp.write('token\tpos\tner\tpage\n')
            if index == 0:
                output_fp.write('<quality value="1.0" />\n')
                output_fp.write('<token count="19" />\n')
            elif index == 1:
                output_fp.write('<quality value="0.7143" />\n')
                output_fp.write('<token count="8" />\n')
            output_fp.write('<book identifier="test" />\n')
            with test_file.open('r') as test_fp:
                test_document = json.load(test_fp)
                for page_number, text in test_document:
                    spacy_doc = nlp(text)
                    for spacy_token in spacy_doc:
                        if spacy_token.is_space:
                            continue
                        output_text = f'{spacy_token.text}\t{spacy_token.tag_}\t{spacy_token.ent_type_}\t{page_number}\n'
                        if include_lemma:
                            output_text = f'{spacy_token.text}\t{spacy_token.lemma_}\t{spacy_token.tag_}\t{spacy_token.ent_type_}\t{page_number}\n'
                        output_fp.write(output_text)


if __name__ == "__main__":
    app()
