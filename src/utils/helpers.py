# src/utils/helpers.py

import os
import pandas as pd

def load_csv(filepath: str) -> pd.DataFrame:
    """
    Tải dữ liệu từ file CSV.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File {filepath} không tồn tại.")
    return pd.read_csv(filepath)

def save_csv(df: pd.DataFrame, filepath: str) -> None:
    """
    Lưu DataFrame vào file CSV.
    Tạo các thư mục nếu chưa tồn tại.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
