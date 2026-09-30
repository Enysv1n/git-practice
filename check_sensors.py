import json
import pandas as pd
import yaml
#––––––––––––––––––––––––––––––––––––––––

# 1. Les innstillinger fra config.yml
with open("config.yml") as f:
    config = yaml.safe_load(f)

max_days = config["max_days_since_calibration"]
output_file = config["output_file"]

# 2. Les Excel-filen (lab/eier) og CSV-filen (kalibreringsstatus)
sensors = pd.read_excel("sensors.xlsx")
calibrations = pd.read_csv("calibrations.csv")

# 3. Koble tabellene sammen på sensor_id
merged = sensors.merge(calibrations, on="sensor_id", how="inner")

# 4. Behold bare sensorene som er over grensen
overdue = merged[merged["days_since_calibration"] > max_days]

# 5. Skriv resultatet til JSON (liste med én dict per sensor)
records = overdue.to_dict(orient="records")
with open(output_file, "w") as f:
    json.dump(records, f, indent=2)

print(f"{len(records)} sensor(er) over {max_days} dager. Lagret i {output_file}")
