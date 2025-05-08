# Weather Underground web scraping
# using Playwright

from datetime import datetime
from io import StringIO
import os
import pandas as pd
from playwright.sync_api import sync_playwright

URL = 'https://www.wunderground.com/hourly/th/bang-phli/VTBS/date/{DATE_STR}'
TABLE_XPATH = '//*[@id="hourly-forecast-table"]'

OUTPUT_PATH = 'wun_forecast'

def extract_table(table: pd.DataFrame, curr_date: str) -> pd.DataFrame:

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    
    df = pd.DataFrame()
    df['DateTime'] = pd.to_datetime(curr_date + " " + table['Time'],
        format="%Y-%m-%d %I:%M %p")
    df['Condition'] = table['Conditions'].astype("string")
    df['Temp(F)'] = table['Temp.'].str.extract(r'(\d+)').astype(int)
    df['Feels Like(F)'] = table['Feels Like'].str.extract(r'(\d+)').astype(int)
    df['Precipitation(%)'] = table['Precip'].str.extract(r'(\d+)').astype(int)
    df['Amount(in)'] = table['Feels Like'].str.extract(r'(\d+)').astype(int)
    df['Cloud Cover(%)'] = table['Cloud Cover'].str.extract(r'(\d+)').astype(int)
    df['Dew Point(%)'] = table['Dew Point'].str.extract(r'(\d+)').astype(int)
    df['Humidity(%)'] = table['Humidity'].str.extract(r'(\d+)').astype(int)
    df['Wind(mph)'] = table['Wind'].str.extract(r'(\d+)').astype(int)
    df['Wind Direction'] = table['Wind'].str.extract(r' (\w+)$').astype("string")
    df['Pressure(in)'] = table['Pressure'].str.extract(r'([\d\.]+)').astype(float)

    return df

def interpolate_forecast(df: pd.DataFrame) -> pd.DataFrame:

    df = df.set_index('DateTime')
    df = df.resample('15min').asfreq()
    for column in df.columns:
        if column in ['Condition', 'Wind Direction']:
            df[column] = df[column].ffill()
        else:
            df[column] = df[column].interpolate()

    df = df.reset_index()

    return df

def wun_forecast(forecast_date: datetime) -> pd.DataFrame:

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        forecast = pd.DataFrame()
        for curr in pd.date_range(forecast_date, forecast_date + pd.DateOffset(days=1)):
            
            curr_date = curr.strftime("%Y-%m-%d")
            url = URL.replace('{DATE_STR}', curr_date)
            print(url)
            page.goto(url, wait_until="commit")
            table = page.locator(TABLE_XPATH)
            table.wait_for(timeout=60000)
            print("table loaded")

            tables = pd.read_html(StringIO(page.content()))
            table = tables[0].head(-1).copy()
            df = extract_table(table, curr_date)
            forecast = pd.concat([forecast, df], ignore_index=True)

        forecast = interpolate_forecast(forecast)
        forecast = forecast[forecast['DateTime'].dt.date == forecast_date.date()]

        path = f"{OUTPUT_PATH}/{forecast_date.strftime('%Y-%m-%d')}.csv"
        forecast.to_csv(path, index=False)
        print(f"{path} saved")

        browser.close()

    return pd.DataFrame()

def tomorrow_forecast() -> pd.DataFrame:
    tomorrow = datetime.now() + pd.DateOffset(days=1)
    return wun_forecast(tomorrow)

if __name__ == "__main__":
    tomorrow_forecast()
