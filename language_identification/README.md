# Language Identification

We explain here how we identify the language of a British Library book based on the [FastText language identification models](https://fasttext.cc/docs/en/language-identification.html). THer language is identified through the [./language_id.py script](./language_id.py) which is explained best below: (below is a better formatted version of the help from the script generated through `python language_id.py --help`):

``` bash
Usage: language_id.py [OPTIONS] MODEL_PATH FILE_TO_PROCESS OUTPUT_FILE
                      EXCLUDE_FILENAME

Arguments:
  MODEL_PATH        File path to either the large or small FastText language
                    identification model.  [required]

  FILE_TO_PROCESS   File path to a British Library book file.  [required]
  OUTPUT_FILE       File to store the JSON output, file is opened in append
                    mode.  [required]

  EXCLUDE_FILENAME  If True then the `filename` key will not be in the output
                    file  [required]

Given a FastText language ID model and a British Library book file. 
It will write the following JSON to the `output_file`:
    
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
```

## Example

Assuming that we have downloaded the [FastText large language identification model](https://fasttext.cc/docs/en/language-identification.html) to [./large_model.bin](./large_model.bin) (if you are running linux this can be downloaded for you be running: `bash get_model.sh ./large_model.bin`) we can identify the language of the [./test_data/test1.json file](./test_data/test1.json) like so:

``` bash
python language_id.py ./large_model.bin ./test_data/test1.json ./output.json False
```

The output of the language identification can be found in the `./output.json` file:

``` json
{"filename": "test1", "language": "Spanish", "language_extras": {"Spanish": {"BCP 47 code": "es", "count": 2, "proportion": 0.6666666666666666}, "English": {"BCP 47 code": "en", "count": 1, "proportion": 0.3333333333333333}}}
```

**NOTE** that if we ran this script again and use a different input file e.g. [./test_data/test2.json file](./test_data/test2.json), **but** use the same output file e.g. `./output.json` the results will **append**:

``` bash
python language_id.py ./large_model.bin ./test_data/test2.json ./output.json False
```

`./output.json`:

```json
{"filename": "test1", "language": "Spanish", "language_extras": {"Spanish": {"BCP 47 code": "es", "count": 2, "proportion": 0.6666666666666666}, "English": {"BCP 47 code": "en", "count": 1, "proportion": 0.3333333333333333}}}
{"filename": "test2", "language": "English", "language_extras": {"English": {"BCP 47 code": "en", "count": 3, "proportion": 1.0}}}
```

As we can see the output from `test2.json` has been appended to `./output.json`.


## Testing

The [./language_id.py script](./language_id.py) has been fully tested. To run the tests:

``` bash
python -m pytest
```