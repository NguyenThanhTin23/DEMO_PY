import pandas as pd

# Load dữ liệu từ file CSV
def new(file_path):
    data = pd.read_csv(file_path)

    # Chuyển cột 'Date' sang kiểu datetime
    data['Date'] = pd.to_datetime(data['Date'])

    # Nhập ngày cụ thể từ người dùng
    specific_date = input("Nhập ngày cần xem (YYYY-MM-DD): ")
    specific_date = pd.to_datetime(specific_date)

    # Lọc dữ liệu cho ngày nhập vào
    specific_day_data = data[data['Date'] == specific_date]

    if specific_day_data.empty:
        print(f"Không có dữ liệu cho ngày {specific_date.date()}.")
    else:
        # Tính tổng số ca mới trong ngày đó trên toàn cầu
        total_new_cases = specific_day_data['New cases'].sum()
        total_new_deaths = specific_day_data['New deaths'].sum()
        total_new_recovered = specific_day_data['New recovered'].sum()

        print(f"\nTổng số ca mới trên toàn cầu vào ngày {specific_date.date()}:")
        print(f"New Cases: {total_new_cases}, New Deaths: {total_new_deaths}, New Recovered: {total_new_recovered}")

    # Tìm ngày có nhiều người chết nhất trong toàn bộ dữ liệu
    day_with_max_deaths = data.loc[data['New deaths'].idxmax()]
    print(f"\nNgày có nhiều người chết nhất trong toàn bộ dữ liệu:")
    print(f"Ngày: {day_with_max_deaths['Date'].date()}, New Deaths: {day_with_max_deaths['New deaths']}")

