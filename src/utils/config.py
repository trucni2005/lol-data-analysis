# src/utils/config.py

import os
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env nếu có
load_dotenv()

# Đường dẫn tới thư mục dữ liệu
RAW_DATA_FOLDER = os.path.join('data', 'raw_data')
PROCESSED_DATA_FOLDER = os.path.join('data', 'processed_data')
EXTERNAL_DATA_FOLDER = os.path.join('data', 'external_data')
CRAWLED_DATA_FOLDER = os.path.join('data', 'crawled_data')

# Đảm bảo các thư mục dữ liệu tồn tại
os.makedirs(RAW_DATA_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_DATA_FOLDER, exist_ok=True)
os.makedirs(EXTERNAL_DATA_FOLDER, exist_ok=True)
os.makedirs(CRAWLED_DATA_FOLDER, exist_ok=True)

# Danh sách các server
SERVERS = [
    'oce', 'ph', 'ru', 'sg', 'th', 'tr', 'tw', 'vn',
    'br', 'eune', 'euw', 'jp', 'kr', 'lan', 'las', 'na'
]

# Danh sách các độ dài trận đấu
DURATIONS = ['short', 'medium']  # 'long' có thể được thêm nếu cần

# Số trang tối đa để crawl
MAX_PAGES = 10

# Số lần lặp tối đa để kiểm soát vòng lặp
MAX_ITERATIONS = 2

# Tên file CSV lưu trữ dữ liệu đã crawl
CSV_FILENAME = os.path.join(CRAWLED_DATA_FOLDER, 'raw_data.csv')

# URL mẫu để crawl
BASE_URL_TEMPLATE = 'https://www.leagueofgraphs.com/replays/all/{server}/{duration}/sr-ranked'

