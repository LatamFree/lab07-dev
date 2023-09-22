import requests

from fastapi import Depends
from src.config import Settings, get_settings

class Countries():
    def __init__(self, settings: Settings = Depends(get_settings)):
        self.app_settings = settings

    def get_south_america(self):
        results = []
        subregion = "South America"
        countries_api_url = f"https://restcountries.com/v3.1/subregion/{subregion}?fields=name,capital,currencies,flags,cca2,cca3"

        try: 
            response_countries = requests.get(countries_api_url)
            countries = response_countries.json()

            if response_countries.status_code != requests.codes.ok:
                raise Exception(response_countries.error)

            for country in countries:
                country_name = country["name"]["common"]
                currency_codes = list(country['currencies'].keys())
                capital_names = country["capital"]
                flag_url = country["flags"]["png"]

                info={
                    "name": country_name,
                    "cca2": country["cca2"],
                    "cca3": country["cca3"],
                    "currency": currency_codes[0],
                    "capital": capital_names[0],
                    "flag_url": flag_url
                }
                results.append(info)
            return results
        except Exception as error:
            return {
                "message": "API not available"
            }

    def get_capital_weather(self, country_code):
        countries_api_url = f"{self.app_settings.REST_COUNTRIES_BASE_URL}/alpha/{country_code}?fields=name,capital,currencies,flags,cca2,cca3"

        try: 
            response_countries = requests.get(countries_api_url)
            country = response_countries.json()
            
            if response_countries.status_code != requests.codes.ok:
                raise Exception(response_countries.error)

            country_name = country["name"]["common"]
            currency_codes = list(country['currencies'].keys())
            capital_names = country["capital"]
            flag_url = country["flags"]["png"]

            info={
                "name": country_name,
                "cca2": country["cca2"],
                "cca3": country["cca3"],
                "currency": currency_codes[0],
                "capital": capital_names[0],
                "flag_url": flag_url
            }

            weatherapi_base_url = f"{self.app_settings.WEATHER_BASE_URL}/forecast.json?key={self.app_settings.WEATHERAPI_KEY}&q={capital_names[0]}&days=3"
            
            response_weather = requests.get(weatherapi_base_url)
            weather = response_weather.json()
            
            if response_weather.status_code != requests.codes.ok:
                raise Exception(weather)
            
            weather_days = []
            
            for forecast_day in weather["forecast"]["forecastday"]:
                weather_days.append({
                    "date": forecast_day["date"],
                    "condition": forecast_day["day"]["condition"]
                })
                
            info["weather"] = {
                "location": weather["location"],
                "days": weather_days
            }
            return info
        
        except Exception as error:
            return {
                "message": str(error)
            }
        