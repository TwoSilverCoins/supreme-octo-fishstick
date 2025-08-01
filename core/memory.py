import sqlite3
from datetime import datetime
from rapidfuzz import process

DB_PATH = "database/tm.sqlite"

def connect_db():
    return sqlite3.connect(DB_PATH)

def insert_tm_entry(source, target, lang_pair, context=None):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO translation_memory (source, target, lang_pair, context, usage_count, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (source, target, lang_pair, context, 1, datetime.utcnow()))
    conn.commit()
    conn.close()

def update_usage_count(source, lang_pair):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE translation_memory
        SET usage_count = usage_count + 1
        WHERE source = ? AND lang_pair = ?
    """, (source, lang_pair))
    conn.commit()
    conn.close()

def get_fuzzy_match(query, lang_pair, threshold=85):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT source, target FROM translation_memory WHERE lang_pair = ?
    """, (lang_pair,))
    entries = cursor.fetchall()
    conn.close()

    sources = [row[0] for row in entries]
    match, score, idx = process.extractOne(query, sources)
    if score >= threshold:
        update_usage_count(sources[idx], lang_pair)
        return entries[idx][1]
    return None
