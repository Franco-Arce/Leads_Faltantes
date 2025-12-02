import pandas as pd
import psycopg2
import streamlit as st
import toml

# Load secrets directly since we are running this as a standalone script for analysis
# We need to manually read the secrets file because st.secrets works only in streamlit apps
secrets = toml.load(".streamlit/secrets.toml")

def get_db_connection(config):
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            database=config["dbname"],
            user=config["user"],
            password=config["password"],
            connect_timeout=5
        )
        return conn
    except Exception as e:
        print(f"Error connecting: {e}")
        return None

def analyze_university(uni_name, config):
    print(f"--- Analyzing {uni_name} ---")
    conn = get_db_connection(config)
    if not conn:
        return

    # Filtrar solo leads de la semana actual (desde el lunes hasta hoy)
    query = """
        SELECT * FROM faltantes_neotel
    """
    try:
        df = pd.read_sql_query(query, conn)
        print(f"Total Rows: {len(df)}")
        
        if df.empty:
            print("Table is empty.")
            return

        print("\nColumns:", df.columns.tolist())
        
        # Check for duplicates
        if 'id' in df.columns:
            duplicates = df.duplicated(subset=['id']).sum()
            print(f"Duplicate IDs: {duplicates}")
        else:
            # Check for full row duplicates
            duplicates = df.duplicated().sum()
            print(f"Full Row Duplicates: {duplicates}")

        # Check Date Range
        if 'fecha' in df.columns:
            print("\nDate Analysis:")
            try:
                # Try converting to datetime to see range
                dates = pd.to_datetime(df['fecha'], errors='coerce')
                print(f"Min Date: {dates.min()}")
                print(f"Max Date: {dates.max()}")
                print(f"Null Dates: {dates.isnull().sum()}")
                
                # Show distribution
                print("\nRecords per Month:")
                print(dates.dt.to_period('M').value_counts().sort_index())
            except Exception as e:
                print(f"Could not analyze dates: {e}")

        # Show sample data
        print("\nSample Data (First 5 rows):")
        print(df.head().to_string())

    except Exception as e:
        print(f"Error querying table: {e}")
    finally:
        conn.close()

# Analyze CREXE as it had the most leads
if "connections" in secrets and "CREXE" in secrets["connections"]:
    analyze_university("CREXE", secrets["connections"]["CREXE"])
else:
    print("CREXE configuration not found.")
