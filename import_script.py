import pandas as pd
from app import db

def scrape_with_pd():
  db.drop_all()
  db.create_all() 
  for year in range(1950,2021):
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html'
    html = pd.read_html(url, header = 0)
    df = html[0]
    df.columns = df.columns.str.replace('%', '_per')
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    playerstats['year'] = year
    playerstats.to_sql('players', db.engine, if_exists='append', index=False)

if __name__ == '__main__':
    scrape_with_pd()