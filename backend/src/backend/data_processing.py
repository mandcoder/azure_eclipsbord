import pandas as pd
from backend.constants import DATA_PATH

solar_df = pd.read_csv(DATA_PATH / "solar.csv")

solar_df.columns = solar_df.columns.str.strip()

solar_df["Path Width (km)"] = solar_df["Path Width (km)"].fillna("missing")

solar_df["Central Duration"] = solar_df["Central Duration"].fillna("missing")
