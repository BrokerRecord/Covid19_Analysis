import pandas as pd
import numpy as np
import requests
import os
from datetime import datetime, timedelta


class CovidDataLoader:
    def __init__(self):
        self.base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"

    def download_data(self, data_dir="../data/raw/"):
        """Download COVID-19 data from Johns Hopkins University repository"""
        os.makedirs(data_dir, exist_ok=True)

        files = {
            "confirmed": "time_series_covid19_confirmed_global.csv",
            "deaths": "time_series_covid19_deaths_global.csv",
            "recovered": "time_series_covid19_recovered_global.csv",
        }

        for data_type, filename in files.items():
            url = self.base_url + filename
            response = requests.get(url)

            if response.status_code == 200:
                filepath = os.path.join(data_dir, f"{data_type}_{filename}")
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {data_type} data")
            else:
                print(f"Failed to download {data_type} data")

    def load_data(self, data_dir="../data/raw/"):
        """Load COVID-19 data into pandas DataFrames"""
        data = {}

        for data_type in ["confirmed", "deaths", "recovered"]:
            file_pattern = f"{data_type}_time_series_covid19_*_global.csv"
            files = [
                f
                for f in os.listdir(data_dir)
                if f.startswith(f"{data_type}_time_series")
            ]

            if files:
                filepath = os.path.join(data_dir, files[0])
                df = pd.read_csv(filepath)
                data[data_type] = df
            else:
                print(f"No file found for {data_type}")

        return data

    def preprocess_data(self, data, save_processed=True):
        """Preprocess and clean the COVID-19 data"""
        processed_data = {}

        for data_type, df in data.items():
            # Melt the dataframe to convert date columns to rows
            id_vars = ["Province/State", "Country/Region", "Lat", "Long"]
            melted_df = df.melt(id_vars=id_vars, var_name="Date", value_name="Cases")

            # Convert date column to datetime
            melted_df["Date"] = pd.to_datetime(melted_df["Date"])

            # Group by country and date
            country_data = (
                melted_df.groupby(["Country/Region", "Date"])
                .agg({"Cases": "sum", "Lat": "first", "Long": "first"})
                .reset_index()
            )

            processed_data[data_type] = country_data

            # Save processed data
            if save_processed:
                os.makedirs("../data/processed/", exist_ok=True)
                country_data.to_csv(
                    f"../data/processed/{data_type}_processed.csv", index=False
                )

        return processed_data

    def get_merged_data(self, processed_data):
        """Merge confirmed, deaths, and recovered data"""
        confirmed = processed_data["confirmed"].rename(columns={"Cases": "Confirmed"})
        deaths = processed_data["deaths"].rename(columns={"Cases": "Deaths"})
        recovered = processed_data["recovered"].rename(columns={"Cases": "Recovered"})

        # Merge datasets
        merged = confirmed.merge(
            deaths[["Country/Region", "Date", "Deaths"]],
            on=["Country/Region", "Date"],
            how="left",
        ).merge(
            recovered[["Country/Region", "Date", "Recovered"]],
            on=["Country/Region", "Date"],
            how="left",
        )

        # Calculate active cases
        merged["Active"] = merged["Confirmed"] - merged["Deaths"] - merged["Recovered"]
        merged["Death_Rate"] = (merged["Deaths"] / merged["Confirmed"] * 100).round(2)
        merged["Recovery_Rate"] = (
            merged["Recovered"] / merged["Confirmed"] * 100
        ).round(2)

        # Fill NaN values
        merged.fillna(0, inplace=True)

        merged.to_csv("../data/processed/merged_covid_data.csv", index=False)
        return merged
