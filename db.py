import sqlite3
from datetime import datetime


def update_db(language_name, base, voc_p, con_p, new_vowels, new_consonants, txt_o, txt_r):
    conn = sqlite3.connect('inventedLanguages.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS languages (
    language_name text,
    base_language text,
    vocal_permutations text,
    consonant_permutations text,
    new_vowels text,
    new_consonants text,
    text_origin text,
    text_result text,
    date text
    )
    ''')
    c.execute('INSERT INTO languages VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (str(language_name), str(base), str(voc_p), str(con_p), str(new_vowels), str(new_consonants), str(txt_o), str(txt_r), str(datetime.now())))
    conn.commit()
    conn.close()


def query_table(language=None):
    conn = sqlite3.connect('inventedLanguages.db')
    c = conn.cursor()
    if language is None:
        c.execute('''SELECT * from languages''')
    else:
        c.execute(f'''
SELECT * from languages 
WHERE language_name='{language}';''')
    result = c.fetchall()
    return result
