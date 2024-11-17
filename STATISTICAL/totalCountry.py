import pandas as pd

# Load dữ liệu từ file CSV
def totalCountry(file_path):
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

    # Kiểm tra xem dữ liệu có tồn tại trong khoảng thời gian không
    if date_range_data.empty:
        print(f"Không có dữ liệu từ {start_date.date()} đến {end_date.date()}")
    else:
        # Nhập tên quốc gia từ người dùng
        country_name = input("Nhập tên quốc gia: ")

        # Kiểm tra xem quốc gia có trong dữ liệu không
        country_data = date_range_data[date_range_data['Country/Region'].str.contains(country_name, case=False, na=False)]

        if country_data.empty:
            print(f"Không có dữ liệu cho quốc gia '{country_name}' trong khoảng thời gian này.")
        else:
            # Lấy thống kê của ngày cuối cùng trong khoảng thời gian cho quốc gia nhập vào
            latest_data = country_data.sort_values('Date').groupby('Country/Region').tail(1).iloc[0]
            
            # Hiển thị thống kê cho quốc gia
            print(f"\nThống kê cho quốc gia {country_name} từ {start_date.date()} đến {end_date.date()}:")
            print(f"Confirmed={latest_data['Confirmed']}, Deaths={latest_data['Deaths']}, Recovered={latest_data['Recovered']}")
        
        # Tính tổng số ca theo toàn cầu
        latest_data_per_country = date_range_data.sort_values('Date').groupby('Country/Region').tail(1)
        global_totals = latest_data_per_country[['Confirmed', 'Deaths', 'Recovered']].sum()
        print(f"\nTổng số ca trên toàn cầu từ {start_date.date()} đến {end_date.date()}:")
        print(global_totals)
