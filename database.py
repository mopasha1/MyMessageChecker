
import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payload TEXT,
            hash TEXT,
            visited BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    conn.close()
def save_payload(payload, unique_hash):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Save payload with unique hash
    cursor.execute('INSERT INTO payloads (payload, hash) VALUES (?, ?)', (payload, unique_hash))
    
    conn.commit()
    conn.close()

def fetch_payload(hash):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT payload FROM payloads WHERE hash = ?', (hash,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

init_db()
