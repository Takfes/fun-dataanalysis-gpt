import argparse
import sqlite3
from pathlib import Path

import pandas as pd

# Define the schemas
schemas = {
    "amazon": """
        CREATE TABLE IF NOT EXISTS amazon (
            order_id TEXT,
            agent_age INTEGER,
            agent_rating REAL,
            store_latitude REAL,
            store_longitude REAL,
            drop_latitude REAL,
            drop_longitude REAL,
            order_date DATE,
            order_time TIME,
            pickup_time TIME,
            weather TEXT,
            traffic TEXT,
            vehicle TEXT,
            area TEXT,
            delivery_time INTEGER,
            category TEXT
        )
        """,
    "zomato": """
        CREATE TABLE IF NOT EXISTS zomato (
            id TEXT,
            delivery_person_id TEXT,
            delivery_person_age REAL,
            delivery_person_ratings REAL,
            restaurant_latitude REAL,
            restaurant_longitude REAL,
            delivery_location_latitude REAL,
            delivery_location_longitude REAL,
            order_date DATE,
            time_ordered TIME,
            time_order_picked TIME,
            weather_conditions TEXT,
            road_traffic_density TEXT,
            vehicle_condition TEXT,
            type_of_order TEXT,
            type_of_vehicle TEXT,
            multiple_deliveries REAL,
            festival INTEGER,
            city TEXT,
            time_taken INTEGER
        )
        """,
}


def parse_user_args():
    parser = argparse.ArgumentParser(description="Load CSV data into SQLite")
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="The dataset to load into SQLite (amazon or zomato)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    # Define the table name
    dataset = parse_user_args().dataset

    # Dynamically determine the path relative to the script's location
    script_dir = Path(__file__).parent  # Directory where the script resides
    data_dir = script_dir.parent / "data" / dataset  # ../data/dataset relative to the script
    csv_path = data_dir / f"{dataset}.csv"

    # Load the CSV files into DataFrames
    df = pd.read_csv(csv_path).dropna()

    # Preprocess the data
    if dataset == "zomato":
        df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%d-%m-%Y").dt.strftime("%Y-%m-%d")
        df = df[
            (df["Time_Orderd"].str.contains(":"))
            & (df["Time_Orderd"].str.len() == 5)
            & (df["Time_Order_picked"].str.contains(":"))
            & (df["Time_Order_picked"].str.len() == 5)
        ].copy()

    # Connect to SQLite (creates or opens the database file)
    db_path = Path("data/mysqlite.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db_path))

    # Execute the schema creation
    con.execute(schemas[dataset])

    # Insert the DataFrame into the SQLite table
    df.to_sql(dataset, con, if_exists="replace", index=False)

    # Commit the changes and close the connection
    con.commit()
    con.close()
