from openmeteo_api.openmeteo import OpenmeteoAPI
import pandas as pd
from typing import Dict, Any

class Openmeteo:

    _om: OpenmeteoAPI

    def __init__(self) -> None:
        self._om = OpenmeteoAPI()

    def forecast(self, params: Dict[str, Any]) -> pd.DataFrame:
        return self._om.forecast(params)

    def historical(self, params: Dict[str, Any]) -> pd.DataFrame:
        return self._om.historical(params)
