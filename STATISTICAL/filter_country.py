import pandas as pd

def filterCountry(file_path):
    file_path = 'full_grouped.csv'  # Thay thế đường dẫn file nếu cần
    data = pd.read_csv(file_path)

    # Chuyển cột 'Date' sang kiểu datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Nhập khoảng thời gian và quốc gia từ người dùng
    start_date = input("Nhập ngày bắt đầu (YYYY-MM-DD): ")
    end_date = input("Nhập ngày kết thúc (YYYY-MM-DD): ")
    selected_country = input("Nhập quốc gia bạn muốn xem dữ liệu: ")

    # Chuyển đổi các ngày nhập từ người dùng thành kiểu datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Lọc dữ liệu cho khoảng thời gian và quốc gia cụ thể
    date_country_data = data[
        (data['Date'] >= start_date) & 
        (data['Date'] <= end_date) & 
        (data['Country/Region'] == selected_country)
    ]

    # Kiểm tra và in kết quả
    if not date_country_data.empty:
        print(f"Dữ liệu từ {start_date.date()} đến {end_date.date()} cho quốc gia {selected_country}:")
        print(date_country_data)
    else:
        print(f"Không có dữ liệu từ {start_date.date()} đến {end_date.date()} cho quốc gia {selected_country}")
    
    
