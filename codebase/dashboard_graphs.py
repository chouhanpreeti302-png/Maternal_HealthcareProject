import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import requests

class ANCDashboard:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        # Fetch and clean the data immediately
        self.anc_data = self._fetch_and_clean_data()

    def _fetch_and_clean_data(self):
        """Fetches data from the API and performs initial cleaning."""
        try:
            response = requests.get(self.api_endpoint)
            if response.status_code == 200:
                df = pd.read_csv(StringIO(response.text))
                # Filter out the summary 'All India' row to only show individual states/UTs
                df = df[df['State/UT'] != 'All India'].copy()
                return df
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Error during API request: {e}")
            return None
        except Exception as e:
            st.error(f"An error occurred while processing the data: {e}")
            return None

    def create_anc_performance_barchart(self, year='2019-20'):
        """Creates a bar chart showing the percentage of women with 4+ ANC check-ups."""
        if self.anc_data is None:
            return

        st.header(f'Performance: % of Women with 4+ ANC Check-ups ({year})')
        st.markdown("This chart ranks states by the percentage of registered pregnant women who received four or more Ante Natal Care check-ups.")

        # Define the exact column names from your new dataset
        performance_col = 'Percentage of women with 4 or more ANC check-ups'
        year_col = 'Year'
        state_col = 'State/UT'
        
        # Filter data for the selected year
        df_year = self.anc_data[self.anc_data[year_col] == year].copy()
        
        # Convert performance column to numbers, handling any errors
        df_year[performance_col] = pd.to_numeric(df_year[performance_col], errors='coerce')
        df_year = df_year.dropna(subset=[performance_col])
        
        # Sort data for better visualization
        df_sorted = df_year.sort_values(by=performance_col, ascending=False)

        fig = px.bar(
            df_sorted,
            x=state_col,
            y=performance_col,
            title=f'ANC Check-up Performance by State/UT for {year}',
            labels={performance_col: '% of Women with 4+ ANC Check-ups', state_col: 'State / Union Territory'},
            color=performance_col,
            color_continuous_scale=px.colors.sequential.Viridis
        )
        fig.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig, use_container_width=True)

    def create_registration_trend_chart(self):
        """Creates a grouped bar chart comparing total ANC registrations over two years."""
        if self.anc_data is None:
            return

        st.header('Trend: Total ANC Registrations (2018-19 vs 2019-20)')
        st.markdown("This chart compares the total number of Ante Natal Care registrations for each state across two consecutive years.")

        # Define the exact column names from your new dataset
        registration_col = 'Total number of pregnant women registered for ANC'
        year_col = 'Year'
        state_col = 'State/UT'

        # Convert registration column to numbers
        df_copy = self.anc_data.copy()
        df_copy[registration_col] = pd.to_numeric(df_copy[registration_col], errors='coerce')
        df_copy = df_copy.dropna(subset=[registration_col])

        fig = px.bar(
            df_copy,
            x=state_col,
            y=registration_col,
            color=year_col, # This creates the grouping
            barmode='group', # This places bars side-by-side
            title='ANC Registrations: 2018-19 vs 2019-20',
            labels={registration_col: 'Total ANC Registrations', state_col: 'State / Union Territory'}
        )
        st.plotly_chart(fig, use_container_width=True)

# This part is for testing the script directly.
# You will call these functions from your main.py file.
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Maternal Health Dashboard (ANC Data)")

    # Your new API Key and Endpoint
    API_KEY = "579b464db66ec23bdd000001841e8421dcf54a8b43cdb5add832a844"
    API_ENDPOINT = f"https://api.data.gov.in/resource/5ae2dbe0-849d-4e20-91ff-1e2905934d7e?api-key={API_KEY}&format=csv"

    dashboard = ANCDashboard(API_ENDPOINT)

    if dashboard.anc_data is not None:
        dashboard.create_anc_performance_barchart(year='2019-20')
        st.divider()
        dashboard.create_registration_trend_chart()