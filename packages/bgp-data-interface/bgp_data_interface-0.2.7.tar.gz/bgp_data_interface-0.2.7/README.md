# B.Grimm Power Data Interface


This is a python library for accessing internal and public data e.g. PI, AMR, openmeteo, etc.


## Installation

```sh
pip install bgp-data-interface
```


## Openmeteo API

### Forecast data

> Openmeteo allows retrieving **15 minute interval** of forecast data for **up to 16 days** \
> and past forecast data **back to around 3 months**.

Calling openmeteo with empty dict will retrieve today's forecast data at Bangbo site with all parameters.

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

### Historical data

> There could be **around 5-day delay** before historical data can be retrieved.


Calling openmeteo with empty dict will retrieve yesterday's historical data at Bangbo site with all parameters.

```py
    from bgp_data_interface.openmeteo import Openmeteo

    df = Openmeteo().historical({})
```

Passing different location parameters will retrieve historical data at the different site.

```py
    loc = location.get_location(location.ABP)

    api = Openmeteo()
    df = api.historical({
        "latitude": loc["latitude"],
        "longitude": loc["longitude"],
    })
```

Passing datetime parameters will specify the historical data period.

```py
    api = Openmeteo()
    last2days = pd.Timestamp.now() + pd.Timedelta(days=-2)
    df = api.historical({
        "start_date": last2days.strftime("%Y-%m-%d"),
        "end_date": (last2days + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
    })
```

Passing hourly parameters will filter the resulting historical data.

```py
    api = Openmeteo()
    df = api.historical({
        "hourly": ["temperature_2m", "wind_speed_10m", "wind_direction_10m"],
    })
```



## PI API


To retrieve webIDs from PI tags, use `get_webids` with a list of tags.

```py
    USERNAME = 'username'
    PASSWORD = 'password'
    SERVER = 'PI server'

    api = PI(USERNAME, PASSWORD)
    webids = pi.get_webids(SERVER, ['first PI tag', 'second PI tag'])
```

To retrieve a summary data during a time period, use `get_summary` with
1. a dataframe of PI tags and PI webIDs
2. PI parameters dict
3. start timestamp
4. end timestamp

```py
    pi = PI(USERNAME, PASSWORD)

    tag_webids = pd.DataFrame([['a PI tag', 'a PI webID']])
    params = {
        'timeZone': 'Asia/Bangkok',
        'summaryDuration': '15m',
        'summaryType': 'Average',
        'calculationBasis': 'TimeWeighted'
    }

    df = pi.get_summary(tag_webids, params,
            pd.Timestamp('2024-12-01 00:00:00'),
            pd.Timestamp('2024-12-01 01:00:00'))
```


To retrieve only the latest summary data, use `get_latest_summary` with
1. a dataframe of PI tags and PI webIDs
2. PI parameters dict

```py
    pi = PI(USERNAME, PASSWORD)

    tag_webids = pd.DataFrame([['a PI tag', 'a PI webID']])
    params = {
        'timeZone': 'Asia/Bangkok',
        'summaryDuration': '15m',
        'summaryType': 'Average',
        'calculationBasis': 'TimeWeighted'
    }
    df = pi.get_latest_summary(tag_webids, params)
```


To retrieve a summary data from Bangbo site during a time period, use `get_bangbo_summary` with start timestamp and end timestamp.

```py
    pi = PI(USERNAME, PASSWORD)
    df = pi.get_bangbo_summary(pd.Timestamp('2024-12-01 00:00:00'),
                        pd.Timestamp('2024-12-01 01:00:00'))
```


To retrieve only the latest summary data from Bangbo site, use `get_bangbo_latest_summary`.

```py
    pi = PI(USERNAME, PASSWORD)
    df = pi.get_bangbo_latest_summary()
```


To retrieve a summary data from Bothong site during a time period, use `get_bothong_summary` with start timestamp and end timestamp.

```py
    pi = PI(USERNAME, PASSWORD)
    df = pi.get_bothong_summary(pd.Timestamp('2024-12-01 00:00:00'),
                        pd.Timestamp('2024-12-01 01:00:00'))
```


To retrieve only the latest summary data from Bothong site, use `get_bothong_latest_summary`.

```py
    pi = PI(USERNAME, PASSWORD)
    df = pi.get_bothong_latest_summary()
```
