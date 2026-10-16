DATA_PATH = "data/raw"

import sys
import duckdb
from loguru import logger

logger.add(sys.stderr, level="INFO")


def main():
    try:
        con = duckdb.connect("weather_data.duckdb")
        logger.debug("Conntected to DuckDB")
        con.execute("CREATE SCHEMA IF NOT EXISTS prod")

        con.execute(f"""
            SELECT * FROM read_parquet('{DATA_PATH}/*.parquet')
        """)

    except Exception as e:
        logger.debug(f"Error: {e}")


if __name__ == "__main__":
    main()
