import pandas as pd

def region(data, start_date, end_date):
    # Chuyển đổi định dạng ngày tháng
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')
    start_date = pd.to_datetime(start_date, format='%d/%m/%Y')
    end_date = pd.to_datetime(end_date, format='%d/%m/%Y')

    # Lọc dữ liệu theo khoảng thời gian
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

    # Lấy dữ liệu của ngày cuối cùng cho từng quốc gia
    latest_data = filtered_data.sort_values('Date').groupby('Country/Region').tail(1)

    # Tính tổng số ca theo từng khu vực WHO
    total_by_region = latest_data.groupby('WHO Region')[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index()

    # Tính tổng toàn cầu (global totals)
    global_totals = latest_data[['Confirmed', 'Deaths', 'Recovered']].sum()

    # Thêm dòng global_totals vào total_by_region với WHO Region là 'The world'
    global_totals_df = pd.DataFrame([global_totals], columns=['Confirmed', 'Deaths', 'Recovered'])
    global_totals_df['WHO Region'] = 'The world'

    # Kết hợp total_by_region với global_totals
    total_by_region = pd.concat([total_by_region, global_totals_df], ignore_index=True)

    return total_by_region
