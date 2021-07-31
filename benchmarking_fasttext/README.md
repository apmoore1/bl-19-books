# Benchmarking FastText Language Identification Models

In this README we are going to benchmark the [large and small FastText Language identification models.](https://fasttext.cc/docs/en/language-identification.html) This will be similar to how we benchmark the Spacy models in [../benchmarking_spacy](../benchmarking_spacy). As we know from benchmarking Spacy the maximum page length is around 11,000 tokens therefore we are going to test how quick the two models can process 11,000 tokens and how much RAM/memory is used.

## High level overview

The small and large models are just as quick as each other, the large model is slightly more accurate. Even though the large model uses 35 times more memory, the memory requirements are very low, around 140MB (small model uses around 4MB).

## Language Identification Details

Both FastText models can recognise 176 languages. The language codes returned are based on [ISO 639](https://en.wikipedia.org/wiki/ISO_639), **but** some of the language codes are ISO 639-1 and some are ISO 639-2. Therefore to know the language returned we are going to use the [langcodes python library.](https://github.com/rspeer/langcodes) An example of how we are going to use the library is shown below:

``` python
from langcodes import Language, standardize_tag

example_lang_codes = "af als am an ar"
lang_codes = lang_codes.split(' ')
for code in lang_codes:
    print(f"Language Name: {Language.get(code).describe('en')['language']}")
    print(f"BCP 47 code: {standardize_tag(code)}")
```

This example will output the following, whereby the [BCP 47](http://tools.ietf.org/html/bcp47) is a more up to date standard for language codes.

``` python
Language Name: Afrikaans
BCP 47 code: af
Language Name: Tosk Albanian
BCP 47 code: als
Language Name: Amharic
BCP 47 code: am
Language Name: Aragonese
BCP 47 code: an
Language Name: Arabic
BCP 47 code: ar
```

## Downloading the models

We need to first download the two models we are testing, the large and small model. We are going to assume that both models are stored in [./fasttext_models](./fasttext_models) directory under the names `large_model.bin` and `small_model.ftz` for the large and small model respectively. If you are running a Linux machine you can download the models using the following script (large model is 126MB and small is 917kB):

``` bash
bash get_models.sh ./fasttext_models/large_model.bin ./fasttext_models/small_model.ftz
```

Else if you are using another Operating System you can download them and change their names, the models can be found at: [https://fasttext.cc/docs/en/language-identification.html](https://fasttext.cc/docs/en/language-identification.html).

## Metrics

To test how quick the large and small model can process 11,000 tokens, we run the [./benchmark_fasttext.py script](./benchmark_fasttext.py) with both the large and small model inputs like so:

``` bash
python benchmark_fasttext.py fasttext_models/large_model.bin large
python benchmark_fasttext.py fasttext_models/small_model.ftz small
```

Of which this tells us the following:

| Model | Time (S)     | Memory used to load model (MB) | Total memory used (MB) |
|-------|--------------|--------------------------------|------------------------|
| Small | 0.002099     | 3.472                          | 3.976                  |
| Large | 0.002025     | 137.388                        | 138.948                |

As we can see the main difference is the memory to load the model in, the large model is about 134MB larger. The time difference is small. These metrics are similar to those given in the [FastText blog post](https://fasttext.cc/blog/2017/10/02/blog-post.html) when they benchmarked these models, however our results tend to show a smaller speed difference between the two models. Based on that blog post they reported the accuracy of the two models which is repeated below:

| Model | Wikipedia | TCL  | EuroGov |
|-------|-----------|------|---------|
| Small | 92.7      | 94.6 | 98.9    |
| Large | 93.1      | 95.1 | 98.9    |

As we can see the large model is slightly more accurate.
