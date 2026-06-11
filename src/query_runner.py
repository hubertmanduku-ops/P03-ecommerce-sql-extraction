# ================================================================
# src/query_runner.py
# ================================================================
# CONTEXT:
#   We wrote SQL in .sql files. Now we need to EXECUTE those queries
#   from Python and get back pandas DataFrames we can work with.
#
# THE ANALOGY:
#   Think of SQLQueryRunner as a translator.
#   You hand it a SQL query (a string).
#   It sends that query to PostgreSQL.
#   PostgreSQL sends back rows of data.
#   SQLQueryRunner catches those rows and packages them as a DataFrame.
#
# KEY pandas FUNCTION: pd.read_sql()
#   pd.read_sql(sql_string, engine) executes SQL and returns a DataFrame.
#   This is what powers every Python + database workflow.
#
# WHY A CLASS AND NOT JUST pd.read_sql() DIRECTLY?
#   The class adds:
#     - Error handling (what if the query fails?)
#     - Logging (track what ran and when)
#     - Timing (how long did each query take?)
#     - Query loading from .sql files
#   These extras make it production-grade rather than just a script.
# ================================================================

import sys, pathlib, time

_root = pathlib.Path(__file__).resolve().parent
while not (_root / "config.py").exists() and _root != _root.parent:
    _root = _root.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import pandas as pd
from config import engine, DB_AVAILABLE, SQL_DIR, INDUSTRY, logger


class SQLQueryRunner:
    """
    Executes SQL queries against the Supabase PostgreSQL database.
    Returns results as pandas DataFrames.

    Attributes
    ──────────
    industry   str           the configured industry schema
    history    list[dict]    log of every query run (for auditing)
    """

    def __init__(self):
        self.industry = INDUSTRY
        self.history  = []   # audit log: each entry records a query run
        logger.info(f"SQLQueryRunner ready — db_available: {DB_AVAILABLE}")

    def run(self, sql: str, params: dict = None) -> pd.DataFrame:
        """
        Execute a SQL query and return results as a DataFrame.

        Args:
            sql     the SQL query string to execute
            params  optional dict of parameters for parameterised queries
                    e.g. params={"dept": "Engineering"}
                    used as WHERE department = :dept in the SQL

        Returns:
            pd.DataFrame with query results (empty DataFrame if query fails)
        """
        if not DB_AVAILABLE or engine is None:
            logger.warning("[SQL] Database not available. Returning empty DataFrame.")
            return pd.DataFrame()

        # Replace {industry} placeholder with the actual schema name
        # This makes SQL files reusable across different industries
        sql = sql.replace("{industry}", self.industry)

        start_time = time.time()   # record start time for performance logging

        try:
            # pd.read_sql() executes SQL and returns a DataFrame
            # params → passed as bind parameters to prevent SQL injection
            df = pd.read_sql(sql, engine, params=params)

            duration_ms = round((time.time() - start_time) * 1000, 1)

            # Record this query in the history log
            self.history.append({
                "sql_preview": sql[:80].strip(),   # first 80 chars for the log
                "rows":        len(df),
                "cols":        len(df.columns),
                "duration_ms": duration_ms,
                "status":      "success",
            })

            logger.info(
                f"[SQL] Query complete — "
                f"{len(df):,} rows × {len(df.columns)} cols | "
                f"{duration_ms}ms"
            )

            return df

        except Exception as e:
            self.history.append({
                "sql_preview": sql[:80].strip(),
                "rows":        0,
                "cols":        0,
                "duration_ms": round((time.time() - start_time) * 1000, 1),
                "status":      f"error: {str(e)[:100]}",
            })
            logger.error(f"[SQL] Query failed: {e}")
            return pd.DataFrame()   # return empty DataFrame so callers do not crash

    def run_file(self, filename: str) -> pd.DataFrame:
        """
        Load a .sql file and execute it.

        Args:
            filename   name of the SQL file in the sql/ directory
                       e.g. "01_basics.sql" or "05_extract_raw_data.sql"

        Returns:
            pd.DataFrame with results of the LAST query in the file.
        """
        sql_path = SQL_DIR / filename

        if not sql_path.exists():
            logger.error(f"[SQL] File not found: {sql_path}")
            return pd.DataFrame()

        logger.info(f"[SQL] Loading: {filename}")

        # Read the .sql file as a Python string
        sql_text = sql_path.read_text(encoding="utf-8")

        # Run the SQL (may contain multiple statements separated by semicolons)
        # We run the whole file and return the result of the last statement
        return self.run(sql_text)

    def demo_basics(self) -> None:
        """
        Run selected demonstration queries from 01_basics.sql.
        Used during the teaching session to show SQL concepts live.
        """
        demos = [
            ("DISTINCT categorys of products",
             f"SELECT DISTINCT category FROM {self.industry}.products ORDER BY category"),
           
			("High value orders above 500",
             f"SELECT order_id, customer_id, total_amount, status, order_date FROM {self.industry}.orders WHERE total_amount > 500 ORDER BY total_amount DESC LIMIT 10"),	          
    		  
            ("Top performing sellers",
     		 f"SELECT store_name, owner_name, country, total_sales, rating FROM {self.industry}.sellers WHERE is_verified = TRUE ORDER BY total_sales DESC LIMIT 10"),
       ]
        

        for title, sql in demos:
            print(f"\n── {title}:")
            df = self.run(sql)
            if not df.empty:
                print(df.to_string(index=False))

    def demo_aggregation(self) -> None:
        """Demo groupby queries from 02_aggregation.sql."""
        
        sql = f"""
            SELECT
                country AS seller_region,
                COUNT(*) AS total_sellers,
                ROUND(AVG(total_sales)::NUMERIC, 2) AS avg_sales,
                ROUND(MAX(rating)::NUMERIC, 2) AS top_rating
            FROM {self.industry}.sellers
            WHERE is_verified = TRUE
            GROUP BY country
            ORDER BY avg_sales DESC
        """
        print("\n── Seller Performance Summary:")
        df = self.run(sql)
        if not df.empty:
            print(df.to_string(index=False))

    def demo_joins(self) -> None:
        """Demo join query from 03_joins.sql."""
            
        sql = f"""
            SELECT
                p.product_name, p.category,
                COUNT(o.order_id) AS number_of_orders,
                SUM(o.quantity) AS total_units_sold,
                ROUND(COALESCE(SUM(o.total_amount), 0)::NUMERIC, 2) AS total_revenue
            FROM {self.industry}.products AS p
            LEFT JOIN {self.industry}.orders AS o ON p.product_id = o.product_id
            WHERE p.is_active = TRUE
            GROUP BY p.product_id, p.product_name, p.category
            ORDER BY total_revenue DESC
            LIMIT 10
        """
        print("\n── Product sales performance (products ↔ orders):")
        df = self.run(sql)
        if not df.empty:
            print(df.to_string(index=False))

    def __str__(self) -> str:
        return (f"SQLQueryRunner(industry={self.industry!r}, "
                f"queries_run={len(self.history)})")

    def __repr__(self) -> str:
        return f"SQLQueryRunner(industry={self.industry!r})"
