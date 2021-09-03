# Spacy Processing of 1890 books

## Installation and Setup

We assume that all of the 1890 British Library books are stored in the following folder on the HEC: `$global_storage/1890_english_books` and have been created through the batching script explained in the `batching files README`, whereby all of these books have been identified as written in English. This directory should have 39 sub-folders each with at most 300 book files.

Before running any script we will need to crate a custom Conda environment so that we have a Python environment that has all of the relevant requirements, this Conda environment will be saved at `$global_storage/conda_environments/py3.8-bl-spacy-processing` on the HEC. Lastly we will create another directory at `$global_storage/1890_english_books_spacy_output`, which will contain all of the results will from running the [./spacy_tagging.py script](./spacy_tagging.py script). All of this is done when you run the following command on the HEC:

``` bash
qsub install.com
```

## Running the Spacy Tagging script

The [./spacy_tagging.py script](./spacy_tagging.py script) is the same script as [../../../spacy_processing/spacy_tagging.py](../../../spacy_processing/spacy_tagging.py), which has been fully tested. The reason for duplicating the script within this directory is so that we can easily copy this directory to the HEC and run the script without having to copy files from different directories.

To run the [./spacy_tagging.py script](./spacy_tagging.py) over all files in all batches within `$global_storage/1890_english_books` run the following command on the HEC:

``` bash
qsub spacy_tagging.com
```

This will result in all of the tagged files being stored in `.tsv` format, for LexiDB, in the directory `$global_storage/1890_english_books_spacy_output`.


### Time taken to run the job on the HEC

This job took around 48 hours to run, whereby we had *39* nodes running at once. Therefore it took each node around 48 hours to process one batch of 300 books. **However** some of the files failed to process due to some of the books containing no JSON data and erroring and running out of memory due to us storing all of the spacy tokens in a list in RAM. These problems are now over come by catching JSON decoding errors and writing all of the spacy tokens to disk rather than saving them in a list in RAM and then at the end of the book writing them to disk. In total though we only processed 9,214 files out of the 11,419 files.