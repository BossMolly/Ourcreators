import os, requests
from datetime import datetime

def fetch_weather():
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key:
        return _mock_weather()

    base = "https://api.openweathermap.org/data/2.5"
    params = {"q": "Seoul,KR", "appid": key, "units": "metric", "lang": "kr"}

    try:
        current = requests.get(f"{base}/weather", params=params, timeout=10).json()
        forecast = requests.get(f"{base}/forecast", params=params, timeout=10).json()

        # 일별 요약 (오후 12시 기준)
        daily = {}
        for item in forecast.get("list", []):
            dt = datetime.fromtimestamp(item["dt"])
            day = dt.strftime("%m/%d")
            if day not in daily and dt.hour == 12:
                daily[day] = {
                    "date": dt.strftime("%a"),
                    "temp": round(item["main"]["temp"]),
                    "desc": item["weather"][0]["description"],
                    "icon": item["weather"][0]["main"]
                }
        weekly = list(daily.values())[:5]

        return {
            "today": {
                "temp": round(current["main"]["temp"]),
                "feels_like": round(current["main"]["feels_like"]),
                "desc": current["weather"][0]["description"],
                "icon": current["weather"][0]["main"],
                "humidity": current["main"]["humidity"]
            },
            "weekly": weekly
        }
    except Exception as e:
        print(f"[weather] error: {e}")
        return _mock_weather()


def _mock_weather():
    return {
        "today": {"temp": 18, "feels_like": 15, "desc": "흐리고 비", "icon": "Rain", "humidity": 75},
        "weekly": [
            {"date": "Thu", "temp": 18, "desc": "비", "icon": "Rain"},
            {"date": "Fri", "temp": 22, "desc": "맑음", "icon": "Clear"},
            {"date": "Sat", "temp": 24, "desc": "맑음", "icon": "Clear"},
            {"date": "Sun", "temp": 20, "desc": "구름", "icon": "Clouds"},
            {"date": "Mon", "temp": 19, "desc": "흐림", "icon": "Clouds"},
        ]
    }
