from fastapi import FastAPI

app = FastAPI(
    title="ARQUI1_2S2026G6 Backend",
    description="Backend para Raspberry Pi, MQTT, MongoDB y Dashboard",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "proyecto": "ARQUI1_2S2026G6",
        "mensaje": "Backend funcionando correctamente"
    }