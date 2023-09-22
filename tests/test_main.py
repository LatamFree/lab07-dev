from fastapi.testclient import TestClient
from tests.utils import check_valid_schema

from src.main import app


def test_get_all():
    all_schema = {
        "type": "array",
        "items": {
            "title": "Items",
            "type": "object",
            "required": [
                "name",
                "cca2",
                "cca3",
                "currency",
                "capital",
                "flag_url"
            ],
            "properties": {
                "name": {
                    "title": "Name",
                    "type": "string"
                },
                "cca2": {
                    "title": "Cca2",
                    "type": "string"
                },
                "cca3": {
                    "title": "Cca3",
                    "type": "string"
                },
                "currency": {
                    "title": "Currency",
                    "type": "string"
                },
                "capital": {
                    "title": "Capital",
                    "type": "string"
                },
                "flag_url": {
                    "title": "Flag_url",
                    "type": "string"
                }
            }
        }

    }

    test_client = TestClient(app)

    response = test_client.get('/all')
    data = response.json()

    assert response.status_code == 200
    assert check_valid_schema(all_schema, data) == True

def test_get_weather_cl():
    test_client = TestClient(app)

    # https://swagger.io/specification/
    # https://jsonschemalint.com/#!/version/draft-07/markup/json
    weather_schema = {
        "$ref": "#/definitions/MySchema",
        "definitions": {
            "MySchema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "cca2": {
                        "type": "string"
                    },
                    "cca3": {
                        "type": "string"
                    },
                    "currency": {
                        "type": "string"
                    },
                    "capital": {
                        "type": "string"
                    },
                    "flag_url": {
                        "type": "string",
                        "format": "uri",
                        "qt-uri-protocols": [
                            "https"
                        ],
                        "qt-uri-extensions": [
                            ".png"
                        ]
                    },
                    "weather": {
                        "$ref": "#/definitions/Weather"
                    }
                },
                "required": [
                    "capital",
                    "cca2",
                    "cca3",
                    "currency",
                    "flag_url",
                    "name",
                    "weather"
                ],
                "title": "Welcome5"
            },
            "Weather": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "location": {
                        "$ref": "#/definitions/Location"
                    },
                    "days": {
                        "type": "array",
                        "items": {
                            "$ref": "#/definitions/Day"
                        }
                    }
                },
                "required": [
                    "days",
                    "location"
                ],
                "title": "Weather"
            },
            "Day": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "date": {
                        "type": "string",
                        "format": "date"
                    },
                    "condition": {
                        "$ref": "#/definitions/Condition"
                    }
                },
                "required": [
                    "condition",
                    "date"
                ],
                "title": "Day"
            },
            "Condition": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "text": {
                        "type": "string"
                    },
                    "icon": {
                        "type": "string"
                    },
                    "code": {
                        "type": "integer"
                    }
                },
                "required": [
                    "code",
                    "icon",
                    "text"
                ],
                "title": "Condition"
            },
            "Location": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "region": {
                        "type": "string"
                    },
                    "country": {
                        "type": "string"
                    },
                    "lat": {
                        "type": "number"
                    },
                    "lon": {
                        "type": "number"
                    },
                    "tz_id": {
                        "type": "string"
                    },
                    "localtime_epoch": {
                        "type": "integer"
                    },
                    "localtime": {
                        "type": "string"
                    }
                },
                "required": [
                    "country",
                    "lat",
                    "localtime",
                    "localtime_epoch",
                    "lon",
                    "name",
                    "region",
                    "tz_id"
                ],
                "title": "Location"
            }
        }
    }

    response = test_client.get('/countries/cl')
    data = response.json()

    assert response.status_code == 200
    assert check_valid_schema(weather_schema, data) == True
