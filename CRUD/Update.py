import pandas as pd

def update(file_path, updated_data):
    # Đọc dữ liệu từ tệp CSV
    data = pd.read_csv(file_path)
    
    # Tìm kiếm bản ghi cần cập nhật
    mask = (data['Date'] == updated_data[0]) & (data['Country/Region'] == updated_data[1])
    
    
    # Cập nhật các giá trị mới cho bản ghi
    data.loc[mask, 'Confirmed'] = updated_data[2]
    data.loc[mask, 'Deaths'] = updated_data[3]
    data.loc[mask, 'Recovered'] = updated_data[4]
    data.loc[mask, 'Active'] = updated_data[5]
    data.loc[mask, 'New cases'] = updated_data[6]
    data.loc[mask, 'New deaths'] = updated_data[7]
    data.loc[mask, 'New recovered'] = updated_data[8]
    data.loc[mask, 'WHO Region'] = updated_data[9]
    
    # Lưu dữ liệu đã cập nhật vào tệp CSV
    data.to_csv(file_path, index=False)
