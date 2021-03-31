from flask import Flask, render_template, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["ENV"] = 'Production'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# this is our model (aka table)
players = db.Table('players',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('Year', db.Integer),
    db.Column('Player', db.String(80)),
    db.Column('Pos', db.String(3)),
    db.Column('Age', db.Integer),
    db.Column('Tm', db.String(5)),
    db.Column('G', db.Integer),
    db.Column('GS', db.Integer),	
    db.Column('MP', db.Float),
    db.Column('FG', db.Float),
    db.Column('FGA', db.Float),
    db.Column('FG_Per', db.Float),
    db.Column('3P', db.Float),
    db.Column('3PA', db.Float),
    db.Column('3P_Per', db.Float),
    db.Column('2P', db.Float),
    db.Column('2PA', db.Float),
    db.Column('2P_Per', db.Float),		
    db.Column('eFG_per', db.Float),
    db.Column('FT', db.Float),
    db.Column('FTA', db.Float),
    db.Column('FT_Per', db.Float),
    db.Column('ORB', db.Float),
    db.Column('DRB', db.Float),
    db.Column('TRB', db.Float),
    db.Column('AST', db.Float),		
    db.Column('STL', db.Float),
    db.Column('BLK', db.Float),
    db.Column('TOV', db.Float),
    db.Column('PF', db.Float),	
    db.Column('PTS', db.Float)
)
@app.route('/', methods=['GET'])
def root():
   return '<h1>This is only an api please go to /api.</h1>'

@app.route('/api', methods=['GET'])
def get_players():
    l = request.args.get('limit')
    y = request.args.get('year')
    bad = Response("Bad Request",status=400)
    try:
      year = f'WHERE year={y if y != '2020' else 2020}'
      limit = f'limit {l}' if l else ' limit 10'' 
      query = db.engine.execute(f'SELECT * FROM players {year}{limit};').fetchall()
      if query == []: return bad
      lst = [dict(item) for item in query]
      return jsonify(lst)
    except:
      return bad

if __name__ == '__main__':
  app.run(debug=True)