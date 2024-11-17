import pandas as pd


def delete(file_path,data,rows_to_delete):
    """
    Chức năng: Xóa các Data theo các hàng với index các hàng lưu trong rows_to_delete
    """
    data = data.drop(rows_to_delete).reset_index(drop=True)
    # Lưu lại dữ liệu đã xóa vào tệp CSV
    data.to_csv(file_path, index=False)
    
