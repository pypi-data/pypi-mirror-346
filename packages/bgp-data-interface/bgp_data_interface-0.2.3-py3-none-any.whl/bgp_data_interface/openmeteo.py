from openmeteo_api import openmeteo_api as api
import pandas as pd
from typing import Dict, Any

class Openmeteo:

    _om: api.OpenmeteoAPI

    def __init__(self) -> None:
        self._om = api.OpenmeteoAPI()

    def forecast(self, params: Dict[str, Any]) -> pd.DataFrame:
        return self._om.forecast(params)

    def historical(self, params: Dict[str, Any]) -> pd.DataFrame:
        return self._om.historical(params)
