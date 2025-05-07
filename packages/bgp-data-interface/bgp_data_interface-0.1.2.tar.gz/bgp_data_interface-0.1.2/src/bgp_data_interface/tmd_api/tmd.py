from datetime import datetime, timedelta
import pandas as pd
import requests

RANGE_URL =    "https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly"
HOURLY_URL = "https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly/at"

HOURLY_PARAMS = {
    "lat":"13.10",
    "lon":"100.10",
    "fields":"tc,rh,slp,rain,ws10m,wd10m,cloudlow,cloudmed,cloudhigh,cond",
    "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
    "hour":"0",
    "duration":"24"
}

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjhjODkxNmQ3NDc1NDc1NmE5NjI1YWEwZGU3ZjY0ZjcxNzgwYmNiNGI4YzhkNTQ2MTE4ZDQ5MjU0YmUxZWU1NWI3MjZkYzlkZTI1MGIwNzljIn0.eyJhdWQiOiIyIiwianRpIjoiOGM4OTE2ZDc0NzU0NzU2YTk2MjVhYTBkZTdmNjRmNzE3ODBiY2I0YjhjOGQ1NDYxMThkNDkyNTRiZTFlZTU1YjcyNmRjOWRlMjUwYjA3OWMiLCJpYXQiOjE3MzM3OTQ0MjgsIm5iZiI6MTczMzc5NDQyOCwiZXhwIjoxNzY1MzMwNDI4LCJzdWIiOiIzNjAxIiwic2NvcGVzIjpbXX0.R8xgT_RsaGi2KaxcW_QV6acowM0zxB0VBWqxPMxcgJxvE9Zt7QNfpHqQumphL0lyH-QhXw6WMEHyvIfcHlgtFFZyKajgiJpAVGA94IF7-We_WuaDxdcvgum1rw9k8Uy792iw4Q_upPSiuuP2KlWI2_sSwQ1gPq9KBsJqvoZ-pePYPVoYaIdadA0K5ybgVfLVSVnlUiRCfYbmteQj8F4Wajj1-qYkmStNx-5OOAo_7-q58MYBr359rtqnUCzsgGq-U4kLX16toX1Mvv91lM1w_HqvJ7dbp25KjkYRxUptHim6k5g03q9DuEER1fpD0EAb-fMBX5gAqUeLyofMiSsO4cWvU9rMacx_teWCwZNH2CAp2i1izz_jfwnmdnGSWTWqI6jCeJDRg6QIOFnKlyhDndj6ah6LXgL-Cr85H3equK6YAYu3DAKeBt7peMkWcP2FoE8zcIWg3354SJOVTnHbN5cPD2wge86A00SdBy-hssczk67BNwFIMvxAD6N3UaMwtCIx-qcmWjYMdVb6yXAWvyOHkDCIvxft7MeuNb7741Hb8LecYEgJMOw7TJDRccrYfDonjgboKuyNL6an55th5tpj6kmq6fgL2HED7rqcFois6wmBBiGa3whAtha7Ad7zcRk6xL_2ZJDtwLytozUvZ20jZxhW_yuSE2WZ_8fOKO4"

HEADERS = {
    'accept': "application/json",
    'authorization': "Bearer " + TOKEN,
}

FIELDS = {
    'tc': 'temperature',
    'rh': 'relative humidity',
    'slp': 'sea level pressure',
    'rain': 'rain',
    'ws10m': 'wind speed 10m',
    'wd10m': 'wind direction 10m',
    'cloudlow': 'cloud low',
    'cloudmed': 'cloud medium',
    'cloudhigh': 'cloud high',
    'cond': 'weather condition'
}

# hourly variables
# https://data.tmd.go.th/nwpapi/doc/apidoc/forecast_location.html

CONDITIONS = [
    (1, 'ท้องฟ้าแจ่มใส', 'Clear'),
    (2, 'มีเมฆบางส่วน', 'Partly cloudy'),
    (3, 'เมฆเป็นส่วนมาก', 'Cloudy'),
    (4, 'มีเมฆมาก', 'Overcast'),
    (5, 'ฝนตกเล็กน้อย', 'Light rain'),
    (6, 'ฝนปานกลาง', 'Moderate rain'),
    (7, 'ฝนตกหนัก', 'Heavy rain'),
    (8, 'ฝนฟ้าคะนอง', 'Thunderstorm'),
    (9, 'อากาศหนาวจัด', 'Very cold'),
    (10, 'อากาศหนาว', 'Cold'),
    (11, 'อากาศเย็น', 'Cool'),
    (12, 'อากาศร้อนจัด', 'Very hot'),
]

class TMD_API:
    def range(self) -> dict:
        response = requests.request("GET", 
            RANGE_URL,
            headers=HEADERS,
        )

        if response.status_code != 200:
            print(f"Failed to retrieve hourly forecast. ({response.status_code})")

        return response.json()['hourly_data']

    def hourly_forecast(self, params: dict) -> pd.DataFrame:
        all_params = HOURLY_PARAMS | params

        response = requests.request("GET", 
            HOURLY_URL,
            headers=HEADERS,
            params= all_params,
        )

        if response.status_code != 200:
            print(f"Failed to retrieve hourly forecast. ({response.status_code})")

        data = response.json()['WeatherForecasts'][0]
        formatted = [[o['time']] + 
                [o['data'][key.strip()] for key in all_params['fields'].split(',')]
            for o in data['forecasts']
        ]

        columns = ['datetime'] + [FIELDS[key] for key in all_params['fields'].split(',')]

        df = pd.DataFrame(data=formatted, columns=columns)
        df['datetime'] = pd.to_datetime(df['datetime'])

        return df

    def bangbo_forecast(self, params: dict) -> pd.DataFrame:
        # Bangbo solar farm location
        all_params = params | {
            "lat": 13.4916354486428,
            "lon": 100.85609829815238,
        }

        return self.hourly_forecast(all_params)

    def btmt_forecast(self, params: dict) -> pd.DataFrame:
        # Bridgestone Tire Manufactoring (Thailand) location
        all_params = params | {
            "lat": 13.449113552830395,
            "lon": 101.05251291232882,
        }

        return self.hourly_forecast(all_params)
    
    def ms_forecast(self, params: dict) -> pd.DataFrame:
        # Michelin Siam location
        all_params = params | {
            "lat": 13.097281399993221,
            "lon": 100.913597969655,
        }

        return self.hourly_forecast(all_params)

    def svb_forecast(self, params: dict) -> pd.DataFrame:
        # Michelin Siam location
        all_params = params | {
            "lat": 13.682354854382313,
            "lon": 100.74670116685681,
        }

        return self.hourly_forecast(all_params)
