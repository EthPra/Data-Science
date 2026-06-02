import pandas as pd

ENERGY_MIX_DATA = "data/energy_mix_2024.json"
DEMAND_DATA = "data/energy_demand_2024.csv"

#Update: creates seperate columns to cater to task 1 plotting requirements
def extract_fuel_percentages(energy_mix):
    fuel_dict = {item['fuel']: item['perc'] for item in energy_mix}
    return pd.Series({
        'solar': fuel_dict.get('solar', 0),
        'wind': fuel_dict.get('wind', 0),
        'gas': fuel_dict.get('gas', 0),
        'nuclear': fuel_dict.get('nuclear', 0),
        'imports': fuel_dict.get('imports', 0), 
        'other': (
            fuel_dict.get('biomass', 0) + 
            fuel_dict.get('other', 0) + 
            fuel_dict.get('hydro', 0) + 
            fuel_dict.get('coal', 0)
        )
    })


def load_data() -> pd.DataFrame:
    
    """Read and restructure data from data files."""

    df_demand = pd.read_csv(DEMAND_DATA)

    df_demand = df_demand[['SETTLEMENT_DATE', 'SETTLEMENT_PERIOD', 'ND']].copy()

    df_demand['date'] = pd.to_datetime(df_demand['SETTLEMENT_DATE'], format='%d-%b-%Y')

    df_demand['time_offset'] = pd.to_timedelta((df_demand['SETTLEMENT_PERIOD'] - 1) * 30, unit='minutes')

    df_demand['timestamp'] = df_demand['date'] + df_demand['time_offset']

    df_demand.set_index('timestamp', inplace=True)

    df_demand.rename(columns={'ND': 'demand', 'SETTLEMENT_PERIOD': 'period'}, inplace=True)

    df_demand = df_demand[['period', 'demand']]

    df_mix = pd.read_json(ENERGY_MIX_DATA)

    #Convert to timezone-naive (aids joining with demand data)
    df_mix['timestamp'] = pd.to_datetime(df_mix['from']).dt.tz_localize(None)

    #Filter to only 2024 data (Removes issues with the first data row from 2023)
    df_mix = df_mix[df_mix['timestamp'].dt.year == 2024].copy()

    df_mix.set_index('timestamp', inplace=True)

    df_energy = df_mix['generationmix'].apply(extract_fuel_percentages)

    #Remove duplicates from demand data (Day light saving consideration)
    df_demand = df_demand[~df_demand.index.duplicated(keep='last')]

    df = df_energy.join(df_demand, how='left')

    df['demand'] = df['demand'].fillna(0) 

    #Task 2 additions: absolute power generation in MW
    df['solar_mw'] = (df['solar'] / 100) * df['demand']
    df['wind_mw'] = (df['wind'] / 100) * df['demand']
    df['gas_mw'] = (df['gas'] / 100) * df['demand']
    df['nuclear_mw'] = (df['nuclear'] / 100) * df['demand']
    
    # Extract date components
    df['year'] = df.index.year
    df['month'] = df.index.month
    df['day'] = df.index.day


    df['period'] = ((df.index.hour * 60 + df.index.minute) // 30) + 1
    df.reset_index(drop=True, inplace=True)

    
    
    
    df = df[[
        'solar', 'wind', 'gas', 'nuclear', 'imports', 'other', 
        'solar_mw', 'wind_mw', 'gas_mw', 'nuclear_mw',
        'period', 'demand', 'year', 'month', 'day'
    ]]
    
    return df

def main():
    """Test loading the data."""
    df = load_data()
    print(df.head())
    print(df.describe())


if __name__ == "__main__":
    main()
