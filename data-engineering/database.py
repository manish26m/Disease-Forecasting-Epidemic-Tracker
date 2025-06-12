import psycopg2
import csv

def safe_int(val):
    try:
        return int(val)
    except:
        return None

def safe_float(val):
    try:
        return float(val)
    except:
        return None

conn = psycopg2.connect(
    host='localhost',
    database='Infectious_Diseases',
    user='postgres',
    password='password',
    port='5432'
)

cur = conn.cursor()

with open(r"D:\Projects\SUMMER_2025(DIDDY_PARTY)\Disease-Forecasting-Epidemic-Tracker\data-engineering\Infectious_Diseases.csv", "r", encoding="utf-8", newline='') as file:
    data_reader = csv.reader(file)
    next(data_reader)  # Skip header row

    for row in data_reader:
        if len(row) < 12:
            print(f"Skipping incomplete row: {row}")
            continue

        # Safely convert
        count = safe_int(row[4])
        population = safe_int(row[5])
        rate = safe_float(row[6])
        ci_lower = safe_float(row[7])
        ci_upper = safe_float(row[8])
        disease_label = safe_int(row[9])
        country_label = safe_int(row[10])
        sex_label = safe_int(row[11])

        # If any critical value is None, skip the row
        if None in [count, population, rate, ci_lower, ci_upper, disease_label, country_label, sex_label]:
            print(f"Skipping bad data row: {row}")
            continue

        try:
            cur.execute("""
                INSERT INTO DiseaseStats (
                    Disease, Country, Year, Sex, Count, Population, Rate,
                    CI_Lower, CI_Upper, Disease_label, Country_label, Sex_label
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row[0],                  # Disease
                row[1],                  # Country
                row[2] + '-01-01',       # Year as date
                row[3],                  # Sex
                count,
                population,
                rate,
                ci_lower,
                ci_upper,
                disease_label,
                country_label,
                sex_label
            ))
        except Exception as e:
            print(f"Skipping row due to error: {e} → {row}")

conn.commit()
cur.close()
conn.close()