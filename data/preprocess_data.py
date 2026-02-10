import pandas as pd
import os

# 1. 업로드하신 파일 읽기
# (파일명이 다를 경우 아래 파일명을 실제 파일명으로 수정하세요)
raw_file = '한국인터넷진흥원_피싱사이트 URL_20231231.csv'
df = pd.read_csv(raw_file)

# 2. '홈페이지주소' 컬럼을 'url'로 이름 변경 및 날짜 제외
# 우리 AI 엔진은 'url'이라는 헤더를 사용합니다.
blacklist_df = df[['홈페이지주소']].rename(columns={'홈페이지주소': 'url'})

# 3. data 폴더가 없다면 생성
if not os.path.exists('data'):
    os.makedirs('data')

# 4. 프로젝트가 인식할 수 있는 위치에 저장
blacklist_df.to_csv('data/blacklist.csv', index=False, encoding='utf-8')

print(f"✅ 변환 완료! 총 {len(blacklist_df)}개의 블랙리스트가 data/blacklist.csv에 저장되었습니다.")