import pandas as pd
from datetime import datetime
def country(data,start_date,end_date):
     data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
     start_date = datetime.strptime(start_date, '%d/%m/%Y')
     end_date = datetime.strptime(end_date, '%d/%m/%Y')
     filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
     # Để lấy dữ liệu của ngày cuối cùng cho từng quốc gia, ta lấy ngày cuối cùng của mỗi quốc gia trong khoảng thời gian đã lọc
     latest_data = filtered_data.sort_values('Date').groupby('Country/Region')[['Country/Region','Confirmed','Deaths','Recovered']].tail(1)
     # Sắp xếp theo số ca nhiễm giảm dần  
     latest_data = latest_data.sort_values(by='Confirmed', ascending=False)
     return latest_data



