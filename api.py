import requests
import pandas as pd

# === WHO Athena API Example ===
def fetch_who_disease_data(disease_keyword='malaria'):
    url = f"https://ghoapi.azureedge.net/api/Indicator?$filter=contains(IndicatorName,'Malaria')"
    response = requests.get(url)
    if response.ok:
        indicators = response.json()['value']
        for i, ind in enumerate(indicators[:3]):  # Show top 3 matches
            print(f"{i+1}. {ind['IndicatorCode']}: {ind['IndicatorName']}")
    else:
        print("Failed to fetch WHO data")

# === CDC Socrata API Example ===
def fetch_cdc_notifiable_diseases():
    url = "https://data.cdc.gov/resource/x9gk-5huc.json?$limit=1000"
    response = requests.get(url)
    if response.ok:
        data = pd.DataFrame(response.json())
        print("Top 5 CDC Records:")
        print(data.head())
    else:
        print("Failed to fetch CDC data")

if __name__ == "__main__":
    print("=== WHO Data (Athena API) ===")
    fetch_who_disease_data('malaria')  # or 'malaria', 'tb', etc.

    print("\n=== CDC Notifiable Diseases (Socrata API) ===")
    fetch_cdc_notifiable_diseases()