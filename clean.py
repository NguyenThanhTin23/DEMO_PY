import pandas as pd

def delete_empty(df):
    df = df.dropna(how='all')
    df = df.dropna(axis=1, how='all') 
    df = df.fillna(0)
    return df

def format_number(df):
    numeric_columns = df.select_dtypes(include=['float', 'int']).columns
    for col in numeric_columns:
        df[col] = df[col].astype(int)
    return df

def cleanData(file_path):
    df = pd.read_csv(file_path)
    # Xoá giá trị NA
    df = delete_empty(df)

    # Chuyển toàn bộ dữ liệu dạng số thành số nguyên
    df = format_number(df)

    # Thay giá trị nhỏ hơn 0 bằng trị tuyệt đối
    numeric_columns = df.select_dtypes(include=['int', 'float']).columns
    for col in numeric_columns:
        df[col] = df[col].abs()
        
    # Xóa kí tự đặc biệt
    for column in df.columns: 
        if column != 'Date': 
            df[column] = df[column].astype(str).str.replace(r"[^\w\s]", "", regex=True)

    # Chuyển dữ liệu cột 'Country/Region' và 'WHO Region' thành dạng title
    df['Country/Region'] = df['Country/Region'].str.title()
    df['WHO Region'] = df['WHO Region'].str.title()

    # Đổi định dạng ngày thành DD/MM/YYYY
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', dayfirst=True, errors='coerce')
    df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')

    # Xoá các hàng trùng lặp và giữ lại hàng đầu tiên
    df = df.drop_duplicates(keep='first')

    return df
