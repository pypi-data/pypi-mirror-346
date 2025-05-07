import openmeteo_requests
from openmeteo_sdk.WeatherApiResponse import WeatherApiResponse

import os
import pandas as pd
import requests_cache
from retry_requests import retry
from typing import Dict, Any

OPENMETEO_URL = "https://api.open-meteo.com/v1/forecast"
HOURLY = 'hourly'
MINUTELY_15 = 'minutely_15'

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

    def forecast(self, params: Dict[str, Any]) -> pd.DataFrame:

        params = {
            "timezone": "Asia/Bangkok",
        } | params


        if (HOURLY not in params) and (MINUTELY_15 not in params):
            return pd.DataFrame()

        responses = self.client.weather_api(OPENMETEO_URL, params=params)
        response = responses[0]

        fifteen_df = self._populate_fifteen_minutely(response, params)
        one_hour_df = self._populate_one_hour(response, params)

        df = pd.DataFrame()
        if MINUTELY_15 in params and HOURLY in params:
            df = pd.merge(fifteen_df, one_hour_df, on='date_time')
        elif MINUTELY_15 in params:
            df = fifteen_df
        elif HOURLY in params:
            df = one_hour_df

        df['date_time'] = df['date_time'] \
            .dt.tz_convert(params['timezone']) \
            .dt.tz_localize(None)

        return df


    def _populate_fifteen_minutely(self, 
            response: WeatherApiResponse,
            params: Dict[str, Any]) -> pd.DataFrame:

        if MINUTELY_15 not in params:
            return pd.DataFrame()

        minutely_15 = response.Minutely15()
        fifteen: Dict[str, Any] = {
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
            params: Dict[str, Any]) -> pd.DataFrame:

        if HOURLY not in params:
            return pd.DataFrame()

        hourly = response.Hourly()
        one_hour: Dict[str, Any] = {
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
        one_hour = one_hour.set_index('date_time')
        fifteen = one_hour.resample('15min').interpolate(method='linear')
        fifteen = fifteen.reset_index()

        return fifteen
