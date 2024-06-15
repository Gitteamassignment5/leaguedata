import pandas as pd
import os
import json

# 현재 스크립트의 디렉토리 경로 가져오기
current_dir = os.path.dirname(os.path.abspath(__file__))

# 파일 경로 설정
premier_league_path = os.path.join(current_dir, 'original/PremierLeague.csv')
season_0910_path = os.path.join(current_dir, 'original/season-0910.csv')

# 데이터 불러오기
premier_league_df = pd.read_csv(premier_league_path)
season_0910_df = pd.read_csv(season_0910_path)

# 컬럼 매칭 딕셔너리
column_mapping = {
    'FullTimeHomeTeamGoals': 'FTHG',
    'FullTimeAwayTeamGoals': 'FTAG',
    'FullTimeResult': 'FTR',
    'HalfTimeHomeTeamGoals': 'HTHG',
    'HalfTimeAwayTeamGoals': 'HTAG',
    'HalfTimeResult': 'HTR',
    'HomeTeamShots': 'HS',
    'AwayTeamShots': 'AS',
    'HomeTeamShotsOnTarget': 'HST',
    'AwayTeamShotsOnTarget': 'AST',
    'HomeTeamCorners': 'HC',
    'AwayTeamCorners': 'AC',
    'HomeTeamFouls': 'HF',
    'AwayTeamFouls': 'AF',
    'HomeTeamYellowCards': 'HY',
    'AwayTeamYellowCards': 'AY',
    'HomeTeamRedCards': 'HR',
    'AwayTeamRedCards': 'AR',
    'B365HomeTeam': 'B365H',
    'B365Draw': 'B365D',
    'B365AwayTeam': 'B365A'
}

# 컬럼 이름 변경
premier_league_df.rename(columns=column_mapping, inplace=True)

# season-0910.csv의 컬럼명 사용
column_names = season_0910_df.columns.tolist()

# Season 컬럼 추가 (날짜 데이터를 기반으로 시즌 추정)
premier_league_df['Season'] = premier_league_df['Date'].apply(
    lambda x: f"{x.split('/')[2]}-{str(int(x.split('/')[2]) + 1)[-2:]}" if int(x.split('/')[1]) >= 8 else f"{str(int(x.split('/')[2]) - 1)}-{x.split('/')[2][-2:]}"
)

# Div 컬럼에 E0 값을 할당하여 프리미어리그임을 명시
premier_league_df['Div'] = 'E0'

# 누락된 컬럼을 추가하고 NaN으로 채움
missing_in_premier_league = set(column_names) - set(premier_league_df.columns)
for column in missing_in_premier_league:
    premier_league_df[column] = pd.NA

# 주요 컬럼 중 NaN 값이 없는 행만 필터링
main_columns = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
premier_league_df = premier_league_df.dropna(subset=main_columns)

# 컬럼 순서를 season-0910.csv 파일과 동일하게 설정
reordered_columns = column_names + ['Season']
premier_league_df = premier_league_df[reordered_columns]

# Season 컬럼을 기준으로 연도별로 분할
seasons = premier_league_df['Season'].unique()

# 결과를 저장할 result 디렉토리 생성
result_dir = os.path.join(current_dir, 'result')
os.makedirs(result_dir, exist_ok=True)

# 연도별로 파일 저장 및 JSON 생성
output_files = []

for season in seasons:
    season_df = premier_league_df[premier_league_df['Season'] == season]
    start_year = season.split('-')[0]
    end_year = season.split('-')[1]
    output_filename = f'{start_year}-{end_year}season.csv'
    output_path = os.path.join(result_dir, output_filename)
    season_df.to_csv(output_path, index=False)
    output_files.append(output_path)
    
    # JSON 파일 저장
    json_output_filename = f'{start_year}-{end_year}season.json'
    json_output_path = os.path.join(result_dir, json_output_filename)
    season_df.to_json(json_output_path, orient='records', date_format='iso')
    output_files.append(json_output_path)

# 생성된 파일 목록 출력
print("Generated CSV and JSON files:")
for file in output_files:
    print(file)