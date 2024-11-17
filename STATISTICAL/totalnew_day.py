import pandas as pd

# Load dữ liệu từ file CSV
def totalNewDay(file_path):
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
        # Tính tổng số ca mới, chết mới, hồi phục mới cho từng ngày
        daily_totals = date_range_data.groupby('Date')[['New cases', 'New deaths', 'New recovered']].sum()

        print(f"\nTổng số ca mới, chết mới, hồi phục mới cho từng ngày từ {start_date.date()} đến {end_date.date()}:")
        print(daily_totals)

        # Tìm ngày có nhiều ca mới nhất
        day_with_max_new_cases = daily_totals['New cases'].idxmax()
        print(f"\nNgày có nhiều ca mới nhất:")
        print(f"Ngày: {day_with_max_new_cases}, New Cases: {daily_totals.loc[day_with_max_new_cases, 'New cases']}")

        # Tìm ngày có nhiều ca chết mới nhất
        day_with_max_new_deaths = daily_totals['New deaths'].idxmax()
        print(f"\nNgày có nhiều ca chết mới nhất:")
        print(f"Ngày: {day_with_max_new_deaths}, New Deaths: {daily_totals.loc[day_with_max_new_deaths, 'New deaths']}")

        # Tìm ngày có nhiều ca hồi phục mới nhất
        day_with_max_new_recovered = daily_totals['New recovered'].idxmax()
        print(f"\nNgày có nhiều ca hồi phục mới nhất:")
        print(f"Ngày: {day_with_max_new_recovered}, New Recovered: {daily_totals.loc[day_with_max_new_recovered, 'New recovered']}")
