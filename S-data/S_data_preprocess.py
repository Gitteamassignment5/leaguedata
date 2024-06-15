import os
import pandas as pd
import json

# 현재 스크립트의 디렉토리 경로 가져오기
current_dir = os.path.dirname(os.path.abspath(__file__))

# CSV 파일들이 저장된 result 폴더 경로 설정
csv_folder_path = os.path.join(current_dir, 'result')

# JSON 파일을 저장할 경로 설정 (CSV 파일과 동일한 폴더)
json_folder_path = csv_folder_path

def csv_to_json(csv_folder_path, json_folder_path, start_year, end_year):
    # 지정된 년도 범위 내의 파일들을 처리
    for year in range(start_year, end_year):
        csv_filename = f'{year}-{year+1}.csv'
        csv_file_path = os.path.join(csv_folder_path, csv_filename)
        
        # 파일이 존재하는지 확인
        if os.path.exists(csv_file_path):
            # CSV 파일 읽기
            df = pd.read_csv(csv_file_path)
            
            # JSON 형식으로 변환
            json_data = df.to_dict(orient='records')
            
            # JSON 파일로 저장
            json_filename = f'{year}-{year+1}.json'
            json_file_path = os.path.join(json_folder_path, json_filename)
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)
            
            print(f'Successfully converted {csv_filename} to {json_filename}')
        else:
            print(f'File {csv_filename} does not exist')

# 예시 사용법
start_year = 2014
end_year = 2022

csv_to_json(csv_folder_path, json_folder_path, start_year, end_year)