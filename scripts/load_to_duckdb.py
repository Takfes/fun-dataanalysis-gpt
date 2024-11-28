import argparse
from pathlib import Path

import duckdb
import pandas as pd

# Define the schemas
schemas = {
    "amazon": """
        CREATE TABLE IF NOT EXISTS amazon (
            order_id STRING,
            agent_age INTEGER,
            agent_rating FLOAT,
            store_latitude FLOAT,
            store_longitude FLOAT,
            drop_latitude FLOAT,
            drop_longitude FLOAT,
            order_date DATE,
            order_time TIME,
            pickup_time TIME,
            weather STRING,
            traffic STRING,
            vehicle STRING,
            area STRING,
            delivery_time INTEGER,
            category STRING
        )
        """,
    "zomato": """
        CREATE TABLE IF NOT EXISTS zomato (
            id STRING,
            delivery_person_id STRING,
            delivery_person_age FLOAT,
            delivery_person_ratings FLOAT,
            restaurant_latitude FLOAT,
            restaurant_longitude FLOAT,
            delivery_location_latitude FLOAT,
            delivery_location_longitude FLOAT,
            order_date DATE,
            time_ordered TIME,
            time_order_picked TIME,
            weather_conditions STRING,
            road_traffic_density STRING,
            vehicle_condition STRING,
            type_of_order STRING,
            type_of_vehicle STRING,
            multiple_deliveries FLOAT,
            festival BOOLEAN,
            city STRING,
            time_taken INTEGER
        )
        """,
}


def parse_user_args():
    parser = argparse.ArgumentParser(description="Load CSV data into DuckDB")
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="The dataset to load into DuckDB (amazon or zomato)",
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

    # Connect to DuckDB (creates or opens the database file)
    con = duckdb.connect("data/myduckdb.db")

    # Execute the schema creation
    con.execute(schemas[dataset])

    # Insert the DataFrame into the DuckDB table
    con.execute(f"INSERT INTO {dataset} SELECT * FROM df")

    # # Print the first 5 rows of the table
    # print(con.execute(f"SELECT * FROM {dataset} LIMIT 5").fetchdf())
