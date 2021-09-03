# Spacy Processing

We explain here how we use Spacy as our main NLP processing pipeline on the British Library books. All of the British Library books are going to be indexed through [LexiDB database](https://github.com/UCREL/lexidb), therefore the [./spacy_tagging.py script](./spacy_tagging.py) that runs Spacy will create an output file, within a specified output folder, that is specific to inserting into the LexiDB database. Below we describe this process in more detail (the description below has been mainly taken from the help command of the [./spacy_tagging.py script](./spacy_tagging.py) e.g. `python spacy_tagging.py --help`, just formatted better for the README):


``` bash
Usage: spacy_tagging.py [OPTIONS] BOOK_FOLDER OUTPUT_FOLDER

Arguments:
  BOOK_FOLDER    Book folder  [required]
  OUTPUT_FOLDER  Output folder.  [required]

Options:
  -i, --include [ner|tagger|lemmatizer]
                                  The NLP components to include from the
                                  English Spacy pipeline.  [required]

Given a folder/directory, `book_folder`, that contains British Library OCR
book files, it will run the English Spacy pipeline with the specified
included components over all texts in these book files. The tagged result
for each file will be saved to a file with the same name **but** with a
`.tsv` file  extension to the `output_folder`. Each output file can be
used as an input  file to the LexiDB database.

`book_folder` we ignore all files in this folder that do not have a
`.json` extension. Each file has to have the following JSON format: An
Array whereby  each element in that array is another array of length 2,
whereby the first  element is the page number and the second element is
the text of that page,  e.g.:
```

```json
[[1, "First page text"], [2, "second page of text"]]
```

```bash
The texts in these files that are tagged are the texts associated with
each page.

The `.tsv` file format of each output file will be the following:

```

```tsv
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
```
``` bash
As we can see this is not strict TSV file format as we have some XML under
the headers. However these files are the correct input for the LexiDB
database, whereby these XML tags/nodes are used as meta data for the file. Also we can see that we keep the page numbers that the tokens came from.

**NOTE** That tokenisation always occurs, does not need to be included in
the  `components_to_include`
```

## Example

We shall use one of the tests case as an example. Running the following:

``` bash
python spacy_tagging.py ./test_data/book_folder/ ./test_data/expected_output/ -i ner -i tagger -i lemmatizer
```

Will produce the output found in [./test_data/expected_output/](./test_data/expected_output/) from the files within [./test_data/book_folder/](./test_data/book_folder/).

## More Real World Benchmarking

Even though we have benchmarked the various Spacy models and components within [../benchmarking_spacy](../benchmarking_spacy), this benchmark is a more realistic guesstimate of how long the task may take in time. However the benchmarks within [../benchmarking_spacy](../benchmarking_spacy) are still relevant as they test the spacy models when given the largest text input which is a good estimate on the maximum amount of memory (RAM) required to process the British Library Book corpus.

To run the benchmarking (**NOTE** this does not need re-running) and process the results:

``` bash
python benchmark_spacy_runner.py
python analyse_results.py
```

The results are shown below, note that the spaCy model used is the medium model. Units are seconds for time, MB for memory, and hours for whole corpus processing time. The time predict to run on the whole corpus is based on the average book/volume containing 325 pages and the book corpus containing 63,984 volumes, as shown in this [analysis](../HEC_Processing/language_identification/language_analysis.ipynb):

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Whole Corpus Processing Time (Hours)</th>
      <th>time (S)</th>
      <th>total memory (MB)</th>
    </tr>
    <tr>
      <th>components</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>tagger</th>
      <td>14928.132</td>
      <td>25.844</td>
      <td>314.212</td>
    </tr>
    <tr>
      <th>lemmatizer</th>
      <td>15174.949</td>
      <td>26.271</td>
      <td>322.904</td>
    </tr>
    <tr>
      <th>ner</th>
      <td>15115.637</td>
      <td>26.168</td>
      <td>312.004</td>
    </tr>
    <tr>
      <th>tagger,lemmatizer</th>
      <td>15005.113</td>
      <td>25.977</td>
      <td>322.896</td>
    </tr>
    <tr>
      <th>ner,tagger</th>
      <td>15034.287</td>
      <td>26.027</td>
      <td>312.064</td>
    </tr>
    <tr>
      <th>ner,lemmatizer</th>
      <td>14980.288</td>
      <td>25.934</td>
      <td>319.148</td>
    </tr>
    <tr>
      <th>ner,tagger,lemmatizer</th>
      <td>15219.833</td>
      <td>26.349</td>
      <td>319.016</td>
    </tr>
  </tbody>
</table>

## Testing

The [./spacy_tagging.py script](./spacy_tagging.py) has been fully tested, to run the tests:

``` bash
python -m pytest
```