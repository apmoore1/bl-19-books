import csv
import enum
import json
from typing import List, Dict, Iterable, Tuple
from pathlib import Path

import typer
import en_core_web_md


@enum.unique
class ComponentNames(str, enum.Enum):
    NER = "ner"
    POS = "tagger"
    LEMMA = "lemmatizer"
    #PARSER = "parser" not to be included at the moment

app = typer.Typer()

def text_generator(book_file: Path) -> Iterable[Tuple[str, int]]:
    '''
    :param book_file: File path to a British library book file.
    :returns: Yields the text of a page and it's associated page number for all 
              pages in the given book file. NOTE, if the page contains NO text 
              it will be skipped and therefore not yielded from this function.
    '''
    with book_file.open('r') as fp:
        try:
            data = json.load(fp) # Error can occur here if no data is given 
            for page in data:
                if page[1].strip():
                    yield (page[1], int(page[0]))
        except json.decoder.JSONDecodeError:
            yield ('', 0)

def component_to_attribute_mapper() -> Dict[str, str]:
    return {'token': 'token', 'ner': 'ner', 'tagger': 'pos', 'lemmatizer': 'lemma'}

def attribute_to_spacy_mapper() -> List[str]:
    return {'token' : 'text', 'pos' : 'tag_', 'lemma' : 'lemma_', 'ner' : 'ent_type_'}

def add_metadata(node_name: str, attribute_key: str, attribute_value: str
                 ) -> str:
    return f"<{node_name} {attribute_key}=\"{attribute_value}\" />"
    


@app.command()
def process_text(book_folder: Path = typer.Argument(..., exists=True, dir_okay=True, file_okay=False, help="Book folder"),
                 output_folder: Path = typer.Argument(..., help="Output folder."),
                 components_to_include: List[ComponentNames] = typer.Option(..., "--include", "-i", case_sensitive=False,
                                                                            help='The NLP components to include from the English Spacy pipeline.')
                 ) -> None:
    '''
    Given a folder/directory, `book_folder`, that contains British Library OCR 
    book files, it will run the English Spacy pipeline with the specified included 
    components over all texts in these book files. The tagged result for each 
    file will be saved to a file with the same name **but** with a `.tsv` file 
    extension to the `output_folder`. Each output file can be used as an input 
    file to the LexiDB database.

    `book_folder` we ignore all files in this folder that do not have a `.json`
    extension. Each file has to have the following JSON format: An Array whereby 
    each element in that array is another array of length 2, whereby the first 
    element is the page number and the second element is the text of that page, 
    e.g.:

    [[1, "First page text"], [2, "second page of text"]]

    The texts in these files that are tagged are the texts associated with each 
    page.

    The `.tsv` file format of each output file will be the following:

    token	lemma	pos	ner	page
    <quality value="1.0" />
    <token count="19" />
    <book identifier="test" />
    This	this	DT		1
    is	be	VBZ		1
    some	some	DT		1
    text	text	NN		1
    to	to	TO		1
    test	test	VB		1
    if	if	IN		1
    the	the	DT		1
    system	system	NN		1
    works	work	VBZ		1
    correctly	correctly	RB		1
    .	.	.		1
    Here	here	RB		2
    is	be	VBZ		2
    an	an	DT		2
    extra	extra	JJ		2
    test	test	NN		2
    London	London	NNP	GPE	2
    .	.	.		2

    As we can see this is not strict TSV file format as we have some XML under 
    the headers. However these files are the correct input for the LexiDB 
    database, whereby these XML tags/nodes are used as meta data for the file. 
    Also we can see that we keep the page numbers that the tokens came from.

    **NOTE** That tokenisation always occurs, does not need to be included in the 
    `components_to_include`
    '''
    expanded_components_to_exclude = [value.value for value in ComponentNames]
    expanded_components_to_exclude.append('attribute_ruler')
    expanded_components_to_exclude.append('parser')
    components_to_include_values = [component.value for component in components_to_include]
    for component in components_to_include_values:
        if component == 'lemmatizer':
            expanded_components_to_exclude.remove('lemmatizer')
            expanded_components_to_exclude.remove('attribute_ruler')
            if 'tagger' in expanded_components_to_exclude:
                expanded_components_to_exclude.remove('tagger')
        else:
            if component in expanded_components_to_exclude:
                expanded_components_to_exclude.remove(component)

    
    component_default_order = ['token', 'lemmatizer', 'tagger', 'ner']
    component_order = [component for component in component_default_order 
                       if component in components_to_include_values]
    if 'token' not in component_order:
        component_order.insert(0, 'token')
    
    component_to_attribute = component_to_attribute_mapper()
    attribute_order = [component_to_attribute[component] 
                       for component in component_order]
    attributes_to_spacy_tags = attribute_to_spacy_mapper() 

    nlp = en_core_web_md.load(exclude=expanded_components_to_exclude)
    # If you do not create a copy, vocab.strings will update with new words 
    # each time you run the model.
    vocab_strings = list(nlp.vocab.strings)

    # Create the output folder in case it does not exist.
    output_folder.mkdir(parents=True, exist_ok=True)

    for book_file in book_folder.iterdir():
        if book_file.suffix != '.json':
            continue
        
        # Collecting token level data including the page number the tokens came 
        # from.
        import tempfile
        number_tokens = 0
        number_tokens_excluding_punctuation = 0
        number_tokens_found_in_dictionary = 0
        with tempfile.NamedTemporaryFile('w+', newline='') as temp_file:
            temp_tsv_writer = csv.writer(temp_file, delimiter='\t')
            for spacy_doc, page_number in nlp.pipe(text_generator(book_file), 
                                                as_tuples=True, batch_size=1):
                
                for spacy_token in spacy_doc:
                    if spacy_token.is_space:
                            continue
                    if not spacy_token.is_punct:
                        number_tokens_excluding_punctuation += 1
                        if spacy_token.text.lower() in vocab_strings:
                            number_tokens_found_in_dictionary += 1
                    
                    number_tokens += 1
                    token_values = []
                    for attribute in attribute_order:
                        spacy_attribute = attributes_to_spacy_tags[attribute]
                        token_values.append(getattr(spacy_token, spacy_attribute))
                    token_values.append(str(page_number))
                    temp_tsv_writer.writerow(token_values)
                
            
            # Getting the identifier of the book
            book_file_name = book_file.stem
            book_identifier = book_file_name.split('_')[0]

            # Get the OCR noise level of the book, higher the quality the better.
            ocr_quality = 0
            if number_tokens_excluding_punctuation != 0:
                ocr_quality = round(number_tokens_found_in_dictionary / number_tokens_excluding_punctuation, 4)
            ocr_quality_error = ("OCR Quality should never be above 1.0, currently"
                                f" {ocr_quality}, book file: {book_file}")
            assert ocr_quality <= 1, ocr_quality_error
            
            output_file = Path(output_folder, f'{book_file_name}.tsv')
            with output_file.open('w', newline='') as output_fp:
                tsv_writer = csv.writer(output_fp, delimiter='\t')
                headers = attribute_order + ['page']
                tsv_writer.writerow(headers)
                output_fp.write(add_metadata("quality", "value", str(ocr_quality)))
                output_fp.write('\n')
                output_fp.write(add_metadata("token", "count", str(number_tokens)))
                output_fp.write('\n')
                output_fp.write(add_metadata("book", "identifier", str(book_identifier)))
                output_fp.write('\n')
                temp_file.seek(0)
                for line in temp_file:
                    output_fp.write(line)
            

if __name__ == "__main__":
    app()



