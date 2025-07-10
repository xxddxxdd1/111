import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "analyses.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            units TEXT,
            norms TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_analysis(name, category, units, norms, description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analyses (name, category, units, norms, description)
        VALUES (?, ?, ?, ?, ?)
    """, (name, category, units, norms, description))
    conn.commit()
    conn.close()

def find_analysis_by_name(keyword: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, category, units, norms, description
        FROM analyses
        WHERE lower(name) LIKE ?
        LIMIT 1
    """, (f"%{keyword.lower()}%",))
    result = cursor.fetchone()
    conn.close()
    return result

def list_analyses(offset=0, limit=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM analyses LIMIT ? OFFSET ?", (limit, offset))
    results = cursor.fetchall()
    conn.close()
    return results

def delete_analysis(analysis_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
    conn.commit()
    conn.close()
