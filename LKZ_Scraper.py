#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import sqlite3
from sys import exit

class WordDB:

    # By default use in memory database
    def __init__(self, path=":memory:"):
        self.conn = sqlite3.connect(path)
        c = self.conn.cursor()
        # setting UNIQUE on word column deduplicates words
        c.execute('''
            CREATE TABLE IF NOT EXISTS "words" (
	            "id"	INTEGER,
	            "word"	TEXT NOT NULL UNIQUE COLLATE NOCASE,
	            "length"	INTEGER NOT NULL,
	            PRIMARY KEY("id" AUTOINCREMENT)
            );
        ''')
        self.conn.commit()

    def insert(self, words):
        # One liner to create bulk insert query 
        values = ', '.join([f'(\'{word}\', length(\'{word}\'))' for word in words])
        query = f'INSERT INTO words (word, length) VALUES {values} ON CONFLICT ( word ) DO NOTHING;'
        self.conn.execute(query)
        self.conn.commit()

    def get_words(self, order_col='word', order='ASC', limit=''):
        query = f'SELECT word, length FROM words ORDER BY {order_col} {order}'
        if limit != '': query += f' LIMIT {limit}' # if limit is not an empty string set LIMIT
        c = self.conn.cursor()
        c.execute(query)
        return c.fetchall()

    def dump_to_file(self, path, end='\n'):
        word_list = self.get_words()
        with open(path, 'w', encoding='utf-8') as fout:
            for word in word_list:
                fout.write(word[0] + end)

# alphbet for search queries 
alphabet = ['A', 'Ą', 'B', 'C', 'Č', 'D', 'E', 'Ę', 'Ė', 'F', 'G', 'H', 'I', 'Į', 'Y', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'Š', 'T', 'U', 'Ų', 'Ū', 'V', 'Z', 'Ž']


def get_n_scrape(url):
    words = list()
    response = requests.get(url)
    if response.status_code == 200:
        dom = BeautifulSoup(response.content, 'html.parser')
        res = dom.find_all('a', 'abold')
        for result in res:
            words.append(result.string)
        return words
    else:
        raise Exception(f'HTTP Error {response.status_code}')

if '__main__' == __name__:
    db = WordDB()

    for letter in alphabet:
        url = f"http://158.129.192.222/LKZ_2021/Zodziai.asp?txtZodis={letter.casefold()}&nrLn=-1&nrLe=-1&zdId=-1&tstMode=0"
        print(f'Querying letter "{letter}"...')
        try:
            words = get_n_scrape(url)
        except Exception as e:
            print(str(e))
            exit('Exiting...')
        print('Got %d words.' % len(words))
        db.insert(words)

    # print(db.get_words(limit=10))
    print('Saving words to file...')
    db.dump_to_file('lkz_words.txt')
    print('Done!')
