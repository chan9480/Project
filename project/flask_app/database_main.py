import psycopg2
from .crawling_main import get_sales_data, get_play_time
import pandas as pd
import pandas.io.sql as sqlio
from sqlalchemy import create_engine

host = 'fanny.db.elephantsql.com'
user = 'pkhyshqr'
password = 'WtJjN-4WtpgFDLsBT1xGb_te49FWMxNb'
database = 'pkhyshqr'

#클라우드 데이터베이스 연결+cursor생성
conn = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cur=conn.cursor()

def make_database():
    # 테이블 제거
    cur.execute("DROP TABLE IF EXISTS game")
    conn.commit()
    # 테이블 생성(steamDB와 howlongis플레이타임 데이터 가져옴)
    cur.execute("""CREATE TABLE game(
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(256),
    Discount_rate INT,
    Price INT,
    Rating FLOAT,
    Playtime VARCHAR(16)
    )
    """)

    # 값 삽입

    url = 'https://steamdb.info/sales/'
    game_data = get_sales_data(url, 0)
    for game_data_ in game_data:
        playtime = get_play_time(game_data_['name'])
        cur.execute("""INSERT INTO game (Name, Discount_rate, Price, Rating, Playtime) VALUES (%s,%s,%s,%s,%s)""",
        (game_data_['name'], game_data_['discount_rate'], game_data_['price'], game_data_['rating'], playtime))
    conn.commit()


# eda table 생성
def eda():

    # 이미 있으면 삭제
    cur.execute("DROP TABLE IF EXISTS game_to_analysis")
    conn.commit()
    
    ###pandas DataFrame으로 불러옴.------------------------------------
    #feature : id(=순위나마찬가지), name, discount_rate, price, rating, playtime
    df=sqlio.read_sql_query("""SELECT * FROM game WHERE playtime is not null""", conn)

    ###전처리----------------------------------------------
    # playtime 변경. (1/2 랑 hours와 min 존재)
    df['playtime']=df['playtime'].apply(lambda x: x.replace('Hours', ''))

    df['playtime']=df['playtime'].apply(lambda x: round(float(x.replace('Mins', ''))/60, 2) if 'Mins' in x else x)

    df['playtime']=df['playtime'].apply(lambda x: float(x.replace('½', ''))+0.5 if '½' in str(x) else float(x))
    #id feature삭제
    df=df.drop(['id'], axis=1)

    ####새로운 feature--------------------------------------
    # 가성비 cost performance
    df['cost_performance'] = round(df['price']/df['playtime'], 2)
    #원래 가격
    df['origin_price']=round(df['price']/(df['discount_rate'] + 100)*100 , 2)
    #원래 가성비
    df['origin_performance']=round(df['origin_price']/df['playtime'],2)
    df_sort = df.sort_values(by='rating', ascending=True)
    #아낀 금액
    df['money_save']=df['origin_price']-df['price']
    #시간당 아낀금액
    df['money_save_per_hour'] = round(df['money_save']/df['playtime'] , 2)


    #sqlio.write_frame(df, 'game_to_analysis', conn, flavor='postgresql')

    #클라우드 데이터베이스에 테이블 생성
    engine = create_engine(f'postgresql://{user}:{password}@{host}/{database}')
    df.to_sql('game_to_analysis', engine)

def get_data():
    df=sqlio.read_sql_query("""SELECT * FROM game WHERE playtime is not null""", conn)
    return df.drop('id', axis=1)

def get_data_to_anal():
    df=sqlio.read_sql_query("""SELECT * FROM game_to_analysis """, conn)
    return df.drop('index', axis=1)

def get_best_games():
    result={}
    # 할인되는 금액 최대
    cur.execute("""SELECT * FROM game_to_analysis ORDER BY money_save DESC limit 1""")
    result['할인개이득']=cur.fetchall()
    # 플레이시간당 가격 최소
    cur.execute("""SELECT * FROM game_to_analysis ORDER BY cost_performance limit 1""")
    result['시간당가격최소']=cur.fetchall()
    # 플레이시간당 아낄수 있는 금액 최대
    cur.execute("""SELECT * FROM game_to_analysis ORDER BY money_save_per_hour DESC limit 1""")
    result['시간당할인이득']=cur.fetchall()
    return result
if __name__ == '__main__':
    make_database()
    eda()