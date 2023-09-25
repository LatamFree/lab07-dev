from fastapi import FastAPI, Depends
from .log import init_logger
from .config import get_settings
from .services.countries import Countries

app = FastAPI()
settings = get_settings()
logger = init_logger(settings)

@app.get("/all")
def get_all(
    countries_service: Countries = Depends(),
):
    logger.warning({ "message": 'INFO LOG', "data": 'data for this '})
    results = countries_service.get_south_america()

    return results

@app.get("/countries/{country_code}")
def get_country(
    country_code,
    countries_service: Countries = Depends()
):
    results = countries_service.get_capital_weather(
        country_code
    )

    return results
