import pandas as pd
from astropy.time import Time
import numpy as np

def MJD_Hourly2daily(fname):
    '''Read 3-hour interval EOST displacement files in Modified Julian Date (MJD), 
    and resample into daily intervals'''
    ext_daily = '.daily'
    header = ['MJD_d','NS','EW','UD']
    df = pd.read_csv(fname, names=['MJD_d','NS','EW','UD'], header=None, delim_whitespace=True)
    # convert from MJD to Julian date
    time_mjd = Time(df['MJD_d'].values, format='mjd')
    df['JD'] = time_mjd.jd
    # Convert Julian date to datetime format
    df['datetime'] = pd.to_datetime(df['JD'], origin='julian', unit='D')
    # Resample the data into daily intervals, taking the mean of the values for each day
    daily_df = df.resample('D', on='datetime').mean()
    # Convert the datetime index back to MJD format
    daily_df.index = (daily_df.index - pd.Timestamp('1858-11-17')) / pd.Timedelta('1 day') #+ 2400000.5
    daily_df.reset_index(inplace=True)
    daily_df2= daily_df[['datetime','NS','EW','UD']] 
    daily_df2 = daily_df2.interpolate()
    # Save the resampled data to a new file
    fmt = '%8.1f %7.3f %7.3f %7.3f'
    np.savetxt(fname + ext_daily, daily_df2.values, fmt=fmt)
    return fname + ext_daily
