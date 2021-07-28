
# Benchmarking English spacy models

In this readme we show how fast and memory efficient the [4 main English spacy models](https://spacy.io/models/en): 1. Small, 2. Medium, 3. Large, and 4. Transformer. This is done so we know the trade offs between the models and more importantly estimate the time and memory each model will require to process a text. Knowing the memory requirement is important as Lancaster's High End Computing (HEC) cluster requires us to state up front before submitting a script to run how much memory is required to run the script. Knowing how long it will take (time) will allow us to determine roughly how long it will take to process all of the texts.

To further better scope out the memory requirements we also run a script over all of the British Library books to estimate the maximum page size for each book, in tokens based off character counts. Pages are used as the smallest unit of text as all book are split up into pages of text.


## High level overview

The small spacy model is the quickest and most memory efficient and in comparison to the other non-transformer models it's accuracy is only marginally worse ([see metrics section](#metrics)). The transformer model on the other hand is a lot better than all other models with respect to accuracy and in comparison to the large spacy model is better on the memory efficiency. However the transformer model is a lot slower (almost 30 times slower). **For all models** it is best to use a batch size of `>1` but less than `<100`, whereby a single batch contains around `100 tokens` thus a batch size of `100` would be processing `10,000` tokens.

As the page with the largest number of characters in the whole book corpus is roughly `11,891` tokens long ([see largest page size section](#largest-page-size)), processing a page at a time can easily be done using any of the models with less than `1.5GB` of RAM and if we use either the small or medium model can be achieved with less than `0.5GB` of RAM. 

**Note on the transformer model**, as can be seen from the [total memory](#total-memory-used) used metric, the transformer model does not use anymore memory with larger batch sizes compared to the other models. This I thought was unusual as you expect the larger batch sizes to use more memory, like the other models show. For the transformers models this can be explained by this [blog post](https://explosion.ai/blog/spacy-transformers#batching), whereby they state that they split the input into sentences and batch by a set number of tokens each time, and if the sentence is longer than the transformers maximum sentence length (I think for [RoBERTa this 512, section 2.4 of the paper](https://arxiv.org/pdf/1907.11692.pdf), RoBERTa default model used in spacy) then the sentence gets truncated to the first 512 tokens. 

## Downloading spacy models

Before being able to run either the [./benchmark_spacy.py](./benchmark_spacy.py), or [./benchmark_spacy_runner.py](./benchmark_spacy_runner.py) scripts you will need to download the [4 English spacy models](https://spacy.io/models/en). If you run a linux machine this can be done using the [./download_all_english_models.sh script](./download_all_english_models.sh) like so:

``` bash
bash download_all_english_models.sh
```

Otherwise you can copy the commands within that [script](./download_all_english_models.sh) and run them in your own operating system terminal.

## Metrics

In this section we list the following:

1. [Metric scores](#metic-scores) -- how accurate the models are.
2. [Memory required to load each spacy model](#memory-required-to-load-each-spacy-model) -- this is before processing any text.
3. [Total memory used](#total-memory-used) -- this is the load memory requirement **plus** the memory requirement for processing the given number of tokens.
4. [Time](#time-to-process-texts) -- time taken to process `100,000` tokens, in `N` batch sizes.

In all tables the models are called:

1. Small = **sm**
2. Medium = **md**
3. Large = **lg**
4. Transformer = **trf**

NLP components:

1. Tagger = Part Of Speech (POS) tagger.
2. NER = Named Entity Recogniser.
3. Parser - Dependency Parser.

All of the tables below have been genertated using the [./benchmarking_spacy_runner.py script](./benchmarking_spacy_runner.py), which outputs the results in JSON to the following [./results.json file](./results.json), and using the [./analyse_results.py script](./analyse_results.py) it creates the following tables in the sub-sections below.

``` bash
python benchmarking_spacy_runner.py
python analyse_results.py
```

### Metic scores

These scores for each model and NLP component have been taken from the [main spacy website.](https://spacy.io/usage/facts-figures#benchmarks)

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Model</th>
      <th>NER (F-Score)</th>
      <th>Parser (LAS)</th>
      <th>Tagger (ACC)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
        <th>sm</th>
        <td>84</td>
        <td>90</td>
        <td>97</td>
      </tr>
      <tr>
        <th>md</th>
        <td>85</td>
        <td>90</td>
        <td>97</td>
      </tr>
      <tr>
        <th>lg</th>
        <td>85</td>
        <td>90</td>
        <td>97</td>
      </tr>
      <tr>
        <th>trf</th>
        <td>90</td>
        <td>94</td>
        <td>98</td>
      </tr>
  </tbody>
</table>

### Memory required to load each spacy model

(Unit is MB)

Memory required to load each spacy model with it's given NLP components.

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>included</th>
      <th>lemmatizer</th>
      <th>ner</th>
      <th>parser</th>
      <th>tagger</th>
    </tr>
    <tr>
      <th>model</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>sm</th>
      <td>97.2</td>
      <td>96.6</td>
      <td>89.9</td>
      <td>89.4</td>
    </tr>
    <tr>
      <th>md</th>
      <td>320.8</td>
      <td>313.8</td>
      <td>313.4</td>
      <td>313.0</td>
    </tr>
    <tr>
      <th>lg</th>
      <td>1139.3</td>
      <td>1139.6</td>
      <td>1139.4</td>
      <td>1139.3</td>
    </tr>
    <tr>
      <th>trf</th>
      <td>1062.2</td>
      <td>1061.9</td>
      <td>1061.4</td>
      <td>1061.7</td>
    </tr>
  </tbody>
</table>


### Total memory used

(Unit is MB)

Memory required by each spacy model with it's given NLP components to process `X` tokens (number tokens determined by `batch_size`, whereby a single batch is equal to `100 tokens` so a batch size of `100` is processing `10,000 tokens`). The memory required to process the tokens only you need to subtract the load memory requirements from the [last section](#memory-required-to-load-each-spacy-model):

<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>included</th>
      <th colspan="4" halign="left">lemmatizer</th>
      <th colspan="4" halign="left">ner</th>
      <th colspan="4" halign="left">parser</th>
      <th colspan="4" halign="left">tagger</th>
    </tr>
    <tr>
      <th>batch_size</th>
      <th>1</th>
      <th>100</th>
      <th>200</th>
      <th>300</th>
      <th>1</th>
      <th>100</th>
      <th>200</th>
      <th>300</th>
      <th>1</th>
      <th>100</th>
      <th>200</th>
      <th>300</th>
      <th>1</th>
      <th>100</th>
      <th>200</th>
      <th>300</th>
    </tr>
    <tr>
      <th>model</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>sm</th>
      <td>97.8</td>
      <td>268.5</td>
      <td>439.1</td>
      <td>602.1</td>
      <td>99.0</td>
      <td>264.1</td>
      <td>439.8</td>
      <td>587.5</td>
      <td>90.0</td>
      <td>257.1</td>
      <td>431.7</td>
      <td>592.3</td>
      <td>89.9</td>
      <td>256.5</td>
      <td>431.1</td>
      <td>592.3</td>
    </tr>
    <tr>
      <th>md</th>
      <td>321.1</td>
      <td>476.5</td>
      <td>656.4</td>
      <td>836.2</td>
      <td>318.5</td>
      <td>480.9</td>
      <td>672.6</td>
      <td>816.5</td>
      <td>313.9</td>
      <td>472.4</td>
      <td>648.9</td>
      <td>828.7</td>
      <td>313.6</td>
      <td>470.6</td>
      <td>648.6</td>
      <td>828.5</td>
    </tr>
    <tr>
      <th>lg</th>
      <td>1139.3</td>
      <td>1260.5</td>
      <td>1435.4</td>
      <td>1615.5</td>
      <td>1139.7</td>
      <td>1260.2</td>
      <td>1451.5</td>
      <td>1595.6</td>
      <td>1139.2</td>
      <td>1252.5</td>
      <td>1428.0</td>
      <td>1608.0</td>
      <td>1139.5</td>
      <td>1249.0</td>
      <td>1427.7</td>
      <td>1607.7</td>
    </tr>
    <tr>
      <th>trf</th>
      <td>1062.5</td>
      <td>1061.9</td>
      <td>1069.0</td>
      <td>1236.5</td>
      <td>1070.8</td>
      <td>1060.7</td>
      <td>1062.3</td>
      <td>1156.5</td>
      <td>1068.2</td>
      <td>1062.1</td>
      <td>1092.7</td>
      <td>1125.7</td>
      <td>1069.4</td>
      <td>1061.8</td>
      <td>1061.8</td>
      <td>1180.3</td>
    </tr>
  </tbody>
</table>

### Time to process texts

(Unit is seconds)

Time taken by each spacy model with it's given NLP components to process `100,000` tokens, in `N` batch sizes:

<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>included</th>
      <th colspan="4" halign="left">lemmatizer</th>
      <th colspan="4" halign="left">ner</th>
      <th colspan="4" halign="left">parser</th>
      <th colspan="4" halign="left">tagger</th>
    </tr>
    <tr>
      <th>batch_size</th>
      <th>1</th>
      <th>100</th>
      <th>200</th>
      <th>300</th>
      <th>1</th>
      <th>100</th>
      <th>200</th>
      <th>300</th>
      <th>1</th>
      <th>100</th>
      <th>200</th>
      <th>300</th>
      <th>1</th>
      <th>100</th>
      <th>200</th>
      <th>300</th>
    </tr>
    <tr>
      <th>model</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>sm</th>
      <td>5.477</td>
      <td>4.616</td>
      <td>4.714</td>
      <td>4.674</td>
      <td>8.698</td>
      <td>6.090</td>
      <td>6.374</td>
      <td>6.753</td>
      <td>6.219</td>
      <td>4.098</td>
      <td>4.121</td>
      <td>4.114</td>
      <td>3.927</td>
      <td>3.221</td>
      <td>3.294</td>
      <td>3.366</td>
    </tr>
    <tr>
      <th>md</th>
      <td>5.925</td>
      <td>5.050</td>
      <td>5.069</td>
      <td>5.087</td>
      <td>9.946</td>
      <td>7.276</td>
      <td>7.539</td>
      <td>7.602</td>
      <td>7.027</td>
      <td>4.559</td>
      <td>4.704</td>
      <td>4.571</td>
      <td>4.487</td>
      <td>3.797</td>
      <td>4.006</td>
      <td>3.964</td>
    </tr>
    <tr>
      <th>lg</th>
      <td>6.092</td>
      <td>5.273</td>
      <td>5.620</td>
      <td>5.967</td>
      <td>9.656</td>
      <td>7.283</td>
      <td>7.873</td>
      <td>8.797</td>
      <td>6.730</td>
      <td>4.580</td>
      <td>4.747</td>
      <td>5.463</td>
      <td>4.538</td>
      <td>3.994</td>
      <td>4.174</td>
      <td>4.546</td>
    </tr>
    <tr>
      <th>trf</th>
      <td>259.856</td>
      <td>184.014</td>
      <td>183.423</td>
      <td>191.894</td>
      <td>234.467</td>
      <td>166.725</td>
      <td>173.791</td>
      <td>173.512</td>
      <td>248.417</td>
      <td>174.658</td>
      <td>178.233</td>
      <td>184.548</td>
      <td>251.903</td>
      <td>170.369</td>
      <td>191.918</td>
      <td>185.511</td>
    </tr>
  </tbody>
</table>

## Largest page size

To determine the largest page size we need to find the largest page length per book, to do this run the following [script](./character_range.py) like so:

``` bash
python character_range.py DIRECTORY_TO_BOOKS ./character_count_results.json ./character_log.txt
```

For more details on this script run: 

``` bash
python character_range.py --help
```

Given the result/output and assuming there are 4 characters per word on average in English the longest page from all of the books is 11,891 words long and contains 47,567 characters. This was calculated using this script:

``` bash
python analyse_max_page_character_counts.py ./character_count_results.json 4
```

For more information on this script run:

``` bash
python analyse_max_page_character_counts.py --help
```



