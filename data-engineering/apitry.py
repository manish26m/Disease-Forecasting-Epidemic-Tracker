import requests
import xml.etree.ElementTree as ET

# WHO Athena API URL for Tuberculosis data
url = "http://apps.who.int/gho/athena/api/GHO/ENVCAUSE003"

try:
    # Fetch data from WHO API
    response = requests.get(url)
    response.raise_for_status()

    # Parse XML content
    root = ET.fromstring(response.content)

    # Loop through each 'Fact' entry
    for fact in root.findall(".//Fact"):
        country = fact.find(".//Dim[@category='COUNTRY']")
        year = fact.find(".//Dim[@category='YEAR']")
        sex = fact.find(".//Dim[@category='SEX']")
        value = fact.find(".//Value")

        print("-----------")
        print("Country:", country.text if country is not None else "N/A")
        print("Year:", year.text if year is not None else "N/A")
        print("Sex:", sex.text if sex is not None else "N/A")
        print("Value:", value.attrib['numeric'] if value is not None else "N/A")

except requests.exceptions.RequestException as e:
    print("HTTP Request failed:", e)
except Exception as e:
    print("Error parsing response:", e)
