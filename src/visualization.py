import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os


class CovidVisualizer:
    def __init__(self, style=None):
        try:
            if style and style in plt.style.available:
                plt.style.use(style)
            else:
                plt.style.use("default")  # Use default style
        except:
            plt.style.use("default")  # Fallback to default

        self.colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

    def set_plot_style(self):
        """Set consistent plot style"""
        plt.rcParams["figure.figsize"] = [12, 8]
        plt.rcParams["font.size"] = 12
        plt.rcParams["axes.grid"] = True
        plt.rcParams["grid.alpha"] = 0.3

    def plot_top_countries(
        self, top_countries, metric="Confirmed", title_suffix="Confirmed Cases"
    ):
        """Plot bar chart of top countries by metric"""
        fig, ax = plt.subplots(figsize=(12, 8))

        # Handle both Series and DataFrame inputs
        if isinstance(top_countries, pd.Series):
            countries = top_countries.index
            values = top_countries.values
        else:
            countries = top_countries["Country/Region"]
            values = top_countries[metric]

        bars = ax.barh(countries, values, color=self.colors[0])

        ax.set_xlabel(f"Total {title_suffix}")
        ax.set_title(f"Top {len(countries)} Countries by {title_suffix}")
        ax.invert_yaxis()

        # Add value labels on bars
        for bar in bars:
            width = bar.get_width()
            label_format = (
                f"{width:,.0f}" if metric != "Death_Rate" else f"{width:.2f}%"
            )
            ax.text(
                width,
                bar.get_y() + bar.get_height() / 2,
                label_format,
                ha="left",
                va="center",
                fontweight="bold",
            )

        plt.tight_layout()
        return fig

    def plot_country_time_series(self, country_data, country_name):
        """Plot time series for a specific country"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Total cases
        ax1.plot(
            country_data["Date"],
            country_data["Confirmed"],
            label="Confirmed",
            color=self.colors[0],
            linewidth=2,
        )
        ax1.plot(
            country_data["Date"],
            country_data["Deaths"],
            label="Deaths",
            color=self.colors[3],
            linewidth=2,
        )
        ax1.plot(
            country_data["Date"],
            country_data["Recovered"],
            label="Recovered",
            color=self.colors[2],
            linewidth=2,
        )
        ax1.set_title(f"COVID-19 Cases in {country_name}")
        ax1.legend()
        ax1.tick_params(axis="x", rotation=45)
        ax1.set_ylabel("Number of Cases")

        # Daily new cases (if available)
        if "Daily_Confirmed" in country_data.columns:
            ax2.plot(
                country_data["Date"],
                country_data["Daily_Confirmed"],
                label="Daily Confirmed",
                alpha=0.7,
                color=self.colors[0],
            )
            if "Confirmed_MA_7" in country_data.columns:
                ax2.plot(
                    country_data["Date"],
                    country_data["Confirmed_MA_7"],
                    label="7-day MA",
                    color="red",
                    linewidth=2,
                )
            ax2.set_title(f"Daily New Cases in {country_name}")
            ax2.legend()
            ax2.tick_params(axis="x", rotation=45)
            ax2.set_ylabel("Daily Cases")

        # Growth rates (if available)
        if "Confirmed_Growth_Rate" in country_data.columns:
            ax3.plot(
                country_data["Date"],
                country_data["Confirmed_Growth_Rate"],
                label="Case Growth Rate",
                color=self.colors[0],
            )
            if "Death_Growth_Rate" in country_data.columns:
                ax3.plot(
                    country_data["Date"],
                    country_data["Death_Growth_Rate"],
                    label="Death Growth Rate",
                    color=self.colors[3],
                )
            ax3.set_title(f"Growth Rates in {country_name}")
            ax3.legend()
            ax3.tick_params(axis="x", rotation=45)
            ax3.set_ylabel("Growth Rate (%)")

        # Death rate over time
        ax4.plot(
            country_data["Date"],
            country_data["Death_Rate"],
            color=self.colors[3],
            linewidth=2,
        )
        ax4.set_title(f"Death Rate Over Time in {country_name}")
        ax4.set_ylabel("Death Rate (%)")
        ax4.tick_params(axis="x", rotation=45)

        plt.tight_layout()
        return fig

    def create_heatmap_data(self, data, countries, start_date=None, end_date=None):
        """Prepare data for heatmap visualization"""
        if start_date is None:
            start_date = data["Date"].max() - pd.Timedelta(days=30)
        if end_date is None:
            end_date = data["Date"].max()

        # Filter data for selected countries and date range
        filtered_data = data[
            (data["Country/Region"].isin(countries))
            & (data["Date"] >= start_date)
            & (data["Date"] <= end_date)
        ].copy()

        # Ensure we have data for the heatmap
        if filtered_data.empty:
            print("No data available for the selected countries and date range.")
            return None

        # Pivot for heatmap
        try:
            heatmap_data = filtered_data.pivot_table(
                index="Country/Region",
                columns="Date",
                values="Confirmed",
                aggfunc="sum",
            )
            return heatmap_data
        except Exception as e:
            print(f"Error creating heatmap data: {e}")
            return None

    def plot_heatmap(self, heatmap_data, title="COVID-19 Cases Heatmap"):
        """Plot heatmap of cases by country and date"""
        if heatmap_data is None or heatmap_data.empty:
            print("No data available for heatmap.")
            return None

        fig, ax = plt.subplots(figsize=(15, 8))

        try:
            # Normalize data for better visualization (row-wise normalization)
            normalized_data = heatmap_data.apply(
                lambda x: (
                    (x - x.min()) / (x.max() - x.min()) if x.max() > x.min() else x
                ),
                axis=1,
            )

            sns.heatmap(
                normalized_data,
                ax=ax,
                cmap="YlOrRd",
                cbar_kws={"label": "Normalized Cases"},
            )
            ax.set_title(title)
            ax.set_xlabel("Date")
            ax.set_ylabel("Country")

            plt.tight_layout()
            return fig
        except Exception as e:
            print(f"Error plotting heatmap: {e}")
            return None

    def plot_interactive_global_map(self, data, date=None):
        """Create interactive global map using plotly"""
        if date is None:
            date = data["Date"].max()

        map_data = data[data["Date"] == date].copy()

        # Remove rows with missing coordinates
        map_data = map_data.dropna(subset=["Lat", "Long"])

        if map_data.empty:
            print("No data available for the map.")
            return None

        try:
            fig = px.scatter_geo(
                map_data,
                lat="Lat",
                lon="Long",
                size="Confirmed",
                color="Death_Rate",
                hover_name="Country/Region",
                hover_data={
                    "Confirmed": True,
                    "Deaths": True,
                    "Death_Rate": True,
                    "Lat": False,
                    "Long": False,
                },
                title=f"Global COVID-19 Distribution on {date.strftime('%Y-%m-%d')}",
                color_continuous_scale="Viridis",
                size_max=50,
            )

            fig.update_layout(geo=dict(showframe=False, showcoastlines=True))
            return fig
        except Exception as e:
            print(f"Error creating interactive map: {e}")
            return None

    def plot_multiple_countries_comparison(self, data, countries, metric="Confirmed"):
        """Plot comparison of multiple countries"""
        fig, ax = plt.subplots(figsize=(14, 8))

        for i, country in enumerate(countries):
            country_data = data[data["Country/Region"] == country].sort_values("Date")
            if not country_data.empty:
                ax.plot(
                    country_data["Date"],
                    country_data[metric],
                    label=country,
                    color=self.colors[i % len(self.colors)],
                    linewidth=2,
                )

        ax.set_title(f"COVID-19 {metric} Cases Comparison")
        ax.set_ylabel(f"Number of {metric} Cases")
        ax.legend()
        ax.tick_params(axis="x", rotation=45)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig
