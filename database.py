import sqlite3
import os
import pandas as pd

DB_FILE = "trades.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    return conn

def initialize_database():
    """
    Initializes the database and creates the necessary tables
    if they don't exist.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create trades table with a column for product_code
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY,
        product_code TEXT NOT NULL,
        exec_date TEXT NOT NULL,
        price REAL NOT NULL,
        size REAL NOT NULL,
        side TEXT NOT NULL,
        UNIQUE(id, product_code)
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def get_latest_trade_id(product_code: str) -> int | None:
    """
    Gets the ID of the most recent trade stored for a given product code.

    :param product_code: The product code (e.g., 'BTC_JPY').
    :return: The latest trade ID, or None if the table is empty for that product.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(id) FROM trades WHERE product_code = ?", (product_code,))
    latest_id = cursor.fetchone()[0]

    conn.close()
    return latest_id

def save_trades(trades: list[dict], product_code: str):
    """
    Saves a list of new trades to the database.

    :param trades: A list of trade dictionaries from the API.
    :param product_code: The product code for these trades.
    """
    if not trades:
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    trades_to_insert = [
        (t['id'], product_code, t['exec_date'], t['price'], t['size'], t['side'])
        for t in trades
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO trades (id, product_code, exec_date, price, size, side) VALUES (?, ?, ?, ?, ?, ?)",
        trades_to_insert
    )

    conn.commit()
    conn.close()
    print(f"Attempted to save {len(trades_to_insert)} new trades for {product_code} to the database.")

def load_all_trades_as_df(product_code: str) -> pd.DataFrame:
    """
    Loads all trades for a given product code from the database into a DataFrame.

    :param product_code: The product code (e.g., 'BTC_JPY').
    :return: A pandas DataFrame with all trades for that product.
    """
    conn = get_db_connection()

    df = pd.read_sql_query(
        "SELECT exec_date, price FROM trades WHERE product_code = ? ORDER BY exec_date ASC",
        conn,
        params=(product_code,)
    )

    conn.close()

    # Convert exec_date to datetime objects after loading
    if not df.empty:
        df['exec_date'] = pd.to_datetime(df['exec_date'], format='ISO8601')

    return df
