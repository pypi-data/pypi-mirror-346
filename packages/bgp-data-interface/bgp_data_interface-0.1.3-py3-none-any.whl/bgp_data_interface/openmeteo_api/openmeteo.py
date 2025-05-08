import openmeteo_requests
from openmeteo_sdk.WeatherApiResponse import WeatherApiResponse

import os
import pandas as pd
import requests_cache
from retry_requests import retry
from typing import Any

OPENMETEO_URL = "https://api.open-meteo.com/v1/forecast"
HOURLY = 'hourly'
MINUTELY_15 = 'minutely_15'
DATE_TIME_COL = 'date_time'

DEFAULT_PARAMS: dict[str, Any] = {
    "start_date": pd.Timestamp.now().strftime('%Y-%m-%d'),
    "end_date": pd.Timestamp.now().strftime('%Y-%m-%d'),
    "latitude": 13.4916354486428,
    "longitude": 100.85609829815238,
    "timezone": "Asia/Bangkok",
    MINUTELY_15: [
        "temperature_2m", "precipitation", "freezing_level_height",
        "wind_speed_80m", "visibility", "shortwave_radiation",
        "global_tilted_irradiance", "diffuse_radiation_instant",
        "relative_humidity_2m", "rain", "sunshine_duration",
        "wind_direction_10m", "cape", "direct_radiation",
        "terrestrial_radiation", "direct_normal_irradiance_instant",
        "dew_point_2m", "snowfall", "weather_code", "wind_direction_80m",
        "lightning_potential", "diffuse_radiation",
        "shortwave_radiation_instant", "global_tilted_irradiance_instant",
        "apparent_temperature", "snowfall_height", "wind_speed_10m",
        "wind_gusts_10m", "is_day", "direct_normal_irradiance",
        "direct_radiation_instant", "terrestrial_radiation_instant"
    ],
    HOURLY: [
        "precipitation_probability", "showers",
        "snow_depth", "pressure_msl",
        "surface_pressure", "cloud_cover", "cloud_cover_low",
        "cloud_cover_mid", "cloud_cover_high",
        "evapotranspiration", "et0_fao_evapotranspiration",
        "vapour_pressure_deficit",
        "wind_speed_120m", "wind_speed_180m",
        "wind_direction_120m", "wind_direction_180m",
        "temperature_80m", "temperature_120m",
        "temperature_180m", "soil_temperature_0cm", "soil_temperature_6cm",
        "soil_temperature_18cm", "soil_temperature_54cm",
        "soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm",
        "soil_moisture_3_to_9cm", "soil_moisture_9_to_27cm",
        "soil_moisture_27_to_81cm", "uv_index", "uv_index_clear_sky",
        "wet_bulb_temperature_2m",
        "total_column_integrated_water_vapour", "lifted_index",
        "convective_inhibition", "boundary_layer_height"
    ],
}

class OpenmeteoAPI:

    client = None

    def __init__(self) -> None:
        self.__setup()

    def __setup(self) -> None:
        cache_file = '.cache'
        if os.environ.get('AWS_EXECUTION_ENV') is not None:
            cache_file = '/tmp/.cache'

        cache_session = requests_cache.CachedSession(cache_file, expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.client = openmeteo_requests.Client(session=retry_session)

    def forecast(self, params: dict[str, Any]) -> pd.DataFrame:

        params = DEFAULT_PARAMS | params

        responses = self.client.weather_api(OPENMETEO_URL, params=params)
        response = responses[0]

        fifteen_df = self._populate_fifteen_minutely(response, params)
        one_hour_df = self._populate_one_hour(response, params)

        df = pd.DataFrame()
        if params[MINUTELY_15] and params[HOURLY]:
            df = pd.merge(fifteen_df, one_hour_df, on=DATE_TIME_COL, how="left")
        elif params[MINUTELY_15]:
            df = fifteen_df
        elif params[HOURLY]:
            df = one_hour_df
        else:
            return df

        df[DATE_TIME_COL] = df[DATE_TIME_COL] \
            .dt.tz_convert(params['timezone']) \
            .dt.tz_localize(None)

        return df


    def _populate_fifteen_minutely(self, 
            response: WeatherApiResponse,
            params: dict[str, Any]) -> pd.DataFrame:

        if not params[MINUTELY_15]:
            return pd.DataFrame()

        minutely_15 = response.Minutely15()
        fifteen: dict[str, Any] = {
            "date_time": pd.date_range(
                start=pd.to_datetime(minutely_15.Time(), unit="s", utc=True),
                end=pd.to_datetime(minutely_15.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=minutely_15.Interval()),
                inclusive = "right"
        )}

        for i, variable_name in enumerate(params[MINUTELY_15]):
            fifteen[variable_name] = minutely_15.Variables(i).ValuesAsNumpy()

        return pd.DataFrame(fifteen)


    def _populate_one_hour(self,
            response: WeatherApiResponse,
            params: dict[str, Any]) -> pd.DataFrame:

        if not params[HOURLY]:
            return pd.DataFrame()

        hourly = response.Hourly()
        one_hour: dict[str, Any] = {
            "date_time": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive = "right"
        )}

        for i, variable_name in enumerate(params[HOURLY]):
            one_hour[variable_name] = hourly.Variables(i).ValuesAsNumpy()

        return self._interpolate_1hour_to_15min(pd.DataFrame(one_hour))


    def _interpolate_1hour_to_15min(self, one_hour: pd.DataFrame) -> pd.DataFrame:
        one_hour = one_hour.set_index(DATE_TIME_COL)
        fifteen = one_hour.resample('15min').interpolate(method='linear')
        fifteen = fifteen.reset_index()

        return fifteen
