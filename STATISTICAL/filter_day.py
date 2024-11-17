import pandas as pd

# Load dữ liệu từ file CSV
def filterDay(file_path):
    data = pd.read_csv(file_path)

    # Chuyển cột 'Date' sang kiểu datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Nhập khoảng thời gian từ người dùng
    start_date = input("Nhập ngày bắt đầu (YYYY-MM-DD): ")
    end_date = input("Nhập ngày kết thúc (YYYY-MM-DD): ")

    # Chuyển đổi các ngày nhập từ người dùng thành kiểu datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Lọc dữ liệu cho khoảng thời gian từ ngày bắt đầu đến ngày kết thúc
    date_range_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

    # Kiểm tra và in kết quả
    if not date_range_data.empty:
        print(f"Dữ liệu từ {start_date.date()} đến {end_date.date()}:")
        print(date_range_data)
    else:
        print(f"Không có dữ liệu từ {start_date.date()} đến {end_date.date()}")
