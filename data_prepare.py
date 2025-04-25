import subprocess
import os
import re
import shutil
from tqdm import tqdm

import numpy as np
import pandas as pd

def corpus2df(name, lang=None):
    df = pd.read_table(name, on_bad_lines='skip', header=None, names=['text'])
    df['lang'] = lang
    df = df[['lang', 'text']]
    return df

def clean(f):
    """clean text, remove html tags, and return new file name"""
    in_text = open(f, 'rb').read().decode('utf-8', errors='ignore')
    cleaned = re.sub(r'<.*?>', '', in_text).lower().strip()
    outfile = f.replace('.txt', '-cleaned.txt')
    open(outfile, 'w').write(cleaned)
    os.remove(f)
    return outfile


def preprocess():
    
    # Download the data
    print('Downloading the data and creting txt files, takes long ~20 min .. ')
    subprocess.run(['./download.sh'])

    # Convert the data to csv, and clean the text
    # remove html tags, remove empty lines
    corpora = [c for c in os.listdir('txt/') if c.endswith('.txt')]
    for corpus in corpora:
        lang = corpus.replace('.txt', '')
        corpus = 'txt/' + corpus
        print('{} .. cleaning and converting to a csv .. '.format(corpus), end='\t')
        if 'cleaned' in corpus:
            print('already cleaned.')
            continue
        f = clean(corpus)
        df = corpus2df(f, lang)
        df.to_csv(corpus.replace('.txt', '.csv'), index=False, header=False)
        print('finished.')
    
    # move the csv files to a seaparate folder and delete the text folder to free space
    os.makedirs('data/csv', exist_ok=True)
    csvs = [c for c in os.listdir('txt/') if c.endswith('.csv')]
    for csv in csvs:
        shutil.move('txt/' + csv, 'data/csv/' + csv)
        res = pd.read_csv('data/csv/' + csv, header=None)
        print('csv {} has {} rows.'.format(csv, len(res)))	
    
    # remove the txt folder
    shutil.rmtree('txt/')

    # create a single csv file and add 40,000 samples from each language 
    
    csv_dir = "data/csv/"
    output_file = "data/europarl.csv"

    # Open the output file in write mode
    with open(output_file, "w") as outfile:
        # Iterate over all files in the CSV directory
        for csv_file in os.listdir(csv_dir):
            if csv_file.endswith(".csv"):
                csv_path = os.path.join(csv_dir, csv_file)
                # Read the first 40,000 lines of the CSV file
                df = pd.read_csv(csv_path, header=None, nrows=40000)
                # Write the content to the output file
                df.to_csv(outfile, index=False, header=False, mode="a")
    
    print("Combined CSV file created at:", output_file)
    print('Total samples:', len(pd.read_csv(output_file, header=None)))

    # remove the csv folder
    shutil.rmtree(csv_dir)

    return None

# as per fasttext input format
def normalize_text(row):
    
    label = '__label__' + str(row['lang'])
    txt = str(row['text'])
    
    return ' '.join(( label + ' , ' + txt ).split())

def main():
    if not os.path.exists('data/europarl.csv'):
        preprocess()
    
    # split the data into train, test set 
    df = pd.read_csv('data/europarl.csv', names=['lang', 'text'])
    df = df.reindex(np.random.permutation(df.index)).reset_index(drop=True)
    df['normalized'] = df.apply( lambda row: normalize_text(row), axis=1 )

    SPLIT = 630000  # 75% train, 25% test
    train = df['normalized'][:SPLIT].copy()
    test = df['normalized'][SPLIT:].copy()

    np.savetxt('data/europarl.train', train.values, fmt="%s")
    np.savetxt('data/europarl.eval', test.values, fmt="%s")
    print('Train and test files saved at data/europarl.train and data/europarl.eval')
    print('Train samples:', len(train))
    print('Test samples:', len(test))

if __name__ == '__main__':
    main()
