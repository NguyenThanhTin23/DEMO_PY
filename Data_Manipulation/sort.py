import pandas as pd

def sort_csv(file_path, ascending=True):
    """
    Chức năng:
    Hàm sắp xếp file CSV theo cột Date và cột Country/Region.
    file_path: Đường dẫn đến file CSV đầu vào.

    Tham số:
    file_path: Đường dẫn tới file CSV.
    ascending: Thứ tự sắp xếp, True là tăng dần, False là giảm dần.

    """
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(file_path)
    if ascending == 'false':
        ascending = False
    else:
        ascending = True
    # Sắp xếp dữ liệu theo cột chỉ định
    sort_column = ['Date', 'Country/Region']
    df_sorted = df.sort_values(by=sort_column, ascending=ascending)

    # Lưu lại DataFrame đã sắp xếp vào file CSV
    df_sorted.to_csv(file_path, index=False)

    print(f"Dữ liệu đã được sắp xếp theo cột '{sort_column}' và lưu vào '{file_path}'.")

