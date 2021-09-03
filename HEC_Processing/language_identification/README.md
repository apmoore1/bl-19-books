# Language Identification of all the British Library books

## Installation and Setup

We assume that all of the British Library books are stored in the following folder on the HEC: `$global_scratch/all_books` and have been created through the batching script explained in the `batching files README`. This directory should have 214 sub-folders each with at most 300 book files.

Before running any script we will need to crate a custom Conda environment so that we have a Python environment that has all of the relevant requirements, this Conda environment will be saved at `$global_storage/conda_environments/py3.8-bl-language-id` on the HEC. Additionally we need to download the [large FastText language id model](https://fasttext.cc/docs/en/language-identification.html), this model will be saved at `$global_storage/bl-books-models/large-language-id.bin` on the HEC whereby the directory it is saved too `$global_storage/bl-books-models` will be created with this installation script. Lastly we will create another directory at `$global_scratch/all_books_language_id_results`, which will contain all of the results will from running the [./language_id.py script](./language_id.py). All of this is done when you run the following command on the HEC:

``` bash
qsub install.com
```

## Running the language ID script

The [./language_id.py script](./language_id.py) is the same script as [../../../language_identification/language_id.py](../../../language_identification/language_id.py), which has been fully tested. The reason for duplicating the script within this directory is so that we can easily copy this directory to the HEC and run the script without having to copy files from different directories.

To run the [./language_id.py script](./language_id.py) over all files in all batches within `$global_scratch/all_books` run the following command on the HEC:

``` bash
qsub language_id.com
```

This will then create 214 result files in `$global_scratch/all_books_language_id_results`, whereby the name of the file will relate to the batch number the results are associated with, e.g. result file `0.json` will be the results for batch number `0`.


### Time taken to run the job on the HEC

This job took around 5-7 minutes to run, whereby we had *214* nodes running at once. Therefore it took each node around 5-7 minutes to process one batch of 300 books.

## Language ID results

### Combining results together

**NOTE** this has already been done and is here to note how this process was performed.

As each batch will have it's own results file we need to combine all of the results files into one. To do this run the following script, whereby `/language_id_results` is the directory all of the results were stored in, in our example this would be `$global_scratch/all_books_language_id_results`, and [./language_results.json](./language_results.json) is the to be created combined results file:

``` bash
python combine_language_id_results.py ./language_id_results ./language_results.json
```

### Analysis of the combined results

The analysis can be see in the [./language_analysis.ipynb notebook](./language_analysis.ipynb).

Main takeaways from the analysis:

1. 76.53% of books/volumes are English, 8.20% is French, and 6.68% is German. Total number of books/volumes: 63,984 (whereby a book here can be a volume)
2. 69 books which have more than one volume have 2/3 different languages identified in different volumes of the same book.
3. Out of 63,984 volumes only 3 of them have no text, as they contains either maps only or the text is so poor in them that the OCR could not pick it up.
