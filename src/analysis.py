import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class CovidAnalysis:
    def __init__(self, data):
        self.data = data

    def get_top_countries_by_cases(self, n=10, latest_date=None):
        """Get top N countries by confirmed cases"""
        if latest_date is None:
            latest_date = self.data["Date"].max()

        latest_data = self.data[self.data["Date"] == latest_date]
        top_countries = latest_data.nlargest(n, "Confirmed")[
            ["Country/Region", "Confirmed", "Deaths", "Recovered", "Death_Rate"]
        ]

        return top_countries

    def get_top_countries_by_death_rate(self, n=10, min_cases=1000, latest_date=None):
        """Get top N countries by death rate (with minimum cases filter)"""
        if latest_date is None:
            latest_date = self.data["Date"].max()

        latest_data = self.data[self.data["Date"] == latest_date]
        # Filter countries with minimum cases to avoid skewed rates
        filtered_data = latest_data[latest_data["Confirmed"] >= min_cases]
        top_death_rates = filtered_data.nlargest(n, "Death_Rate")[
            ["Country/Region", "Confirmed", "Deaths", "Death_Rate"]
        ]

        return top_death_rates

    def get_country_time_series(self, country_name):
        """Get time series data for a specific country"""
        country_data = self.data[
            self.data["Country/Region"] == country_name
        ].sort_values("Date")
        return country_data

    def calculate_growth_rates(self, country_data):
        """Calculate daily and weekly growth rates"""
        country_data = country_data.sort_values("Date")

        # Daily growth
        country_data["Daily_Confirmed"] = country_data["Confirmed"].diff()
        country_data["Daily_Deaths"] = country_data["Deaths"].diff()

        # Growth rates
        country_data["Confirmed_Growth_Rate"] = (
            country_data["Confirmed"].pct_change() * 100
        ).round(2)
        country_data["Death_Growth_Rate"] = (
            country_data["Deaths"].pct_change() * 100
        ).round(2)

        # 7-day moving averages
        country_data["Confirmed_MA_7"] = (
            country_data["Daily_Confirmed"].rolling(window=7).mean()
        )
        country_data["Deaths_MA_7"] = (
            country_data["Daily_Deaths"].rolling(window=7).mean()
        )

        return country_data

    def get_global_summary(self, date=None):
        """Get global summary statistics"""
        if date is None:
            date = self.data["Date"].max()

        global_data = self.data[self.data["Date"] == date]

        summary = {
            "Total_Confirmed": global_data["Confirmed"].sum(),
            "Total_Deaths": global_data["Deaths"].sum(),
            "Total_Recovered": global_data["Recovered"].sum(),
            "Total_Active": global_data["Active"].sum(),
            "Global_Death_Rate": (
                global_data["Deaths"].sum() / global_data["Confirmed"].sum() * 100
            ).round(2),
            "Number_of_Countries": global_data["Country/Region"].nunique(),
        }

        return summary
