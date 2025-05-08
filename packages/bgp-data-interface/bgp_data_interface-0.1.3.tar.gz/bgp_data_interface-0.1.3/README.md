# B.Grimm Power Data Interface


## Introduction

This is a python library for accessing internal and public data e.g. PI, AMR, openmeteo, etc.


## Installation

```sh
pip install bgp-data-interface
```


## Openmeteo API

### Forecast

Calling openmeteo with empty dict will retrieve today's forecast at Bangbo site with all parameters.

```py
    from bgp_data_interface.openmeteo import Openmeteo

    df = Openmeteo().forecast({})
```

Passing different location parameters will retrieve forecast data at the different site.

```py
    loc = location.get_location(location.ABP)

    api = Openmeteo()
    df = api.forecast({
        "latitude": loc["latitude"],
        "longitude": loc["longitude"],
    })
```

Passing datetime parameters will specify the forecast data period.

```py
    api = Openmeteo()
    today = pd.Timestamp.now()
    df = api.forecast({
        "start_date": today.strftime("%Y-%m-%d"),
        "end_date": (today + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
    })
```

Passing hourly and minutely_15 parameters will filter the resulting forecast data.

```py
    api = Openmeteo()
    df = api.forecast({
        "hourly": [],
        "minutely_15": ["temperature_2m", "wind_speed_10m", "wind_direction_10m"],
    })
```
