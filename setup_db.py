import sqlite3
from datetime import datetime

DB_NAME = "episteme.db"


def create_tables(conn):
    cursor = conn.cursor()

    # Create tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        notes TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create concepts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS concepts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        status TEXT CHECK( status IN ('unknown','in-progress','known') ) DEFAULT 'unknown',
        explanation TEXT,
        added_by TEXT CHECK( added_by IN ('user','llm') ) DEFAULT 'user'
    );
    """)

    # Create task-concept mapping table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_concept_map (
        task_id INTEGER,
        concept_id INTEGER,
        reason TEXT,
        PRIMARY KEY (task_id, concept_id),
        FOREIGN KEY (task_id) REFERENCES tasks(id),
        FOREIGN KEY (concept_id) REFERENCES concepts(id)
    );
    """)

    # Create reflection logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        concept_id INTEGER,
        date DATETIME DEFAULT CURRENT_TIMESTAMP,
        notes TEXT,
        FOREIGN KEY (concept_id) REFERENCES concepts(id)
    );
    """)

    conn.commit()


def main():
    conn = sqlite3.connect(DB_NAME)
    create_tables(conn)
    conn.close()
    print(f"[✓] Initialized database: {DB_NAME}")


if __name__ == "__main__":
    main()
