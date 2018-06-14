# values can be 'hourly', 'daily', 'weekly', 'monthly', 'half_yearly', 'yearly'
# preferrable that the df is a time series
def openaq_averages(file_location, time):

    df = pd.read_json(file_location)
    df.columns = ['date','value']
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    df = df.set_index('date')

    # Check the value of the time parameter in the function
    if (time == 'hourly'):
        # resample the data by 1 hour
        resample = df.resample('1H')['value'].mean()

    elif (time == 'daily'):
        # resample the data by 1 day
        resample = df.resample('1D')['value'].mean()

    elif (time == 'weekly'):
        # resample the data by 1 week
        resample = df.resample('1W')['value'].mean()

    elif (time == 'monthly'):
        # resample the data by 1 month
        resample = df.resample('1M')['value'].mean()

    elif (time == 'half_yearly'):
        # resample the data by 6 months
        resample = df.resample('6M')['value'].mean()

    elif (time == 'yearly'):
        # resample the data by 1 year
        resample = df.resample('1Y')['value'].mean()

    # a valid value is not submitted. return a message letting the user know what the value can be
    else:
        return "Not an accepted time value. Accepted values are hourly, daily, monthly, half year, or yearly."

    return resample
