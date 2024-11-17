import pandas as pd

# Đọc dữ liệu từ file CSV
def total(file_path):
     data = pd.read_csv(file_path)

     # Chuyển cột 'Date' thành kiểu dữ liệu ngày tháng
     data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

     # Nhập ngày bắt đầu và ngày kết thúc từ người dùng
     start_date = input("Nhập ngày bắt đầu (YYYY-MM-DD): ")
     end_date = input("Nhập ngày kết thúc (YYYY-MM-DD): ")

     # Chuyển đổi đầu vào người dùng sang định dạng datetime
     start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
     end_date = pd.to_datetime(end_date, format='%Y-%m-%d')

     # Lọc dữ liệu trong khoảng thời gian từ start_date đến end_date
     filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

     # Để lấy dữ liệu của ngày cuối cùng cho từng quốc gia, ta lấy ngày cuối cùng của mỗi quốc gia trong khoảng thời gian đã lọc
     latest_data = filtered_data.sort_values('Date').groupby('Country/Region').tail(1)

     # Tính tổng số ca theo từng khu vực WHO
     total_by_region = latest_data.groupby('WHO Region')[['Confirmed', 'Deaths', 'Recovered']].sum()

     # Tính tổng số ca trên toàn cầu
     global_totals = latest_data[['Confirmed', 'Deaths', 'Recovered']].sum()

     # Hiển thị kết quả
     print(f"\nTổng số ca nhiễm, tử vong và hồi phục theo khu vực WHO từ {start_date.date()} đến {end_date.date()}:")
     print(total_by_region)

     print(f"\nTổng số ca nhiễm, tử vong và hồi phục trên toàn cầu từ {start_date.date()} đến {end_date.date()}:")
     print(global_totals)
