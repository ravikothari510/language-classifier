### Objective 
This repo utilizes [fastText](https://github.com/facebookresearch/fastText) library to efficiently classify (21) languages which are based on the [European Parliament Proceedings Parallel Corpus](http://www.statmt.org/europarl/).

This is toy problem which is used to demonstrate the fastText library functions and textual dataset prepartaion and cleanup.fastText is a library for efficient learning of word representations and sentence classification. It is written in C++ and has bindings for Python, Node.js, and Java.


There are several ways to learn word embeddings, [word2vec](https://code.google.com/archive/p/word2vec/) is a popular example.<br>
fastText is another way, which even extends word2vec functionality to include supervised sentence classification.
Where sentence classification training takes place during the learning of word represenations.

### Environment Setup
```bash
conda create -n fasttext python=3.8
conda activate fasttext
pip install -r requirements.txt

!git clone https://github.com/facebookresearch/fastText.git
cd fastText/
make
```

### Dataset Preparation
Download, unzip and collate dataset by running the `data_prepare.py` script.

### language labels:

| language   | label |
|------------|-------|
| Bulgarian  | bg    |
| Czech      | cs    |
| Danish     | da    |
| German     | de    |
| Greek      | el    |
| English    | en    |
| Spanish    | es    |
| Estonian   | et    |
| Finnish    | fi    |
| French     | fr    |
| Hungarian  | hu    |
| Italian    | it    |
| Lithuanian | lt    |
| Latvian    | lv    |
| Dutch      | nl    |
| Polish     | pl    |
| Portuguese | pt    |
| Romanian   | ro    |
| Slovak     | sk    |
| Slovene    | sl    |
| Swedish    | sv    |

### Traing and Validation
```bash
mkdir -p model

TRAIN=data/europarl.train
RESULT=model/europarl

./fastText/fasttext supervised -input $TRAIN -output $RESULT
```
That will generate two files: 
- `europarl.bin`: (787 Mb) this is the learned model which contains the optimized parameters for predicting the language label from a given text.
- `europarl.vec`: (1.9 Gb) a text file that contains the learned vocabulary (around 1.8million) and their embeddings.

For evautaion 
```bash
MODEL=model/europarl.bin
TEST=data/europarl.eval

./fastText/fasttext test $MODEL $TEST
```

Save the prediction 
```bash
mkdir -p prediction

MODEL=model/europarl.bin
TEST=data/europarl.eval
OUTPUT=prediction/europarl.eval.predict

./fastText/fasttext predict $MODEL $TEST > $OUTPUT
```
### Inference
```bash
MODEL=model/europarl.bin
TEST=sample-sentences.txt

./fastText/fasttext predict $MODEL $TEST
```

## TODO
- compare with https://huggingface.co/papluca/xlm-roberta-base-language-detection



