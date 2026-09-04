from fastapi import FastAPI
from backend.data_processing import solar_df

app = FastAPI()


@app.get("/solar/stats")
async def show_data(limit: int = 100):
    return solar_df.head(20).to_dict(orient="records")


@app.get("/solar/type-counts")
async def eclipse_type_counts():
    counts = solar_df["Eclipse Type"].value_counts()

    return counts.to_dict()


# förklara arkitekturen, förklara vad som lever i de olika resurserna, hur requesterna är kopplade till varandra.
