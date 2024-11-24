import pandas as pd

# Load dữ liệu từ file CSV
def day(data,start_date,end_date):

     data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
     start_date = pd.to_datetime(start_date, format='%d/%m/%Y')
     end_date = pd.to_datetime(end_date, format='%d/%m/%Y')
     date_range_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

     daily_totals = date_range_data.groupby('Date')[['New cases', 'New deaths', 'New recovered']].sum().reset_index()

     return daily_totals




       