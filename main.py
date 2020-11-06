# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument

from fastapi import FastAPI
from pydantic import BaseModel

import requests

app = FastAPI()

db = []

class City(BaseModel):
  name: str
  timezone: str

@app.get('/')
def index():
  return {'Hello': 'World'}

@app.get('/cities')
def get_cities():
  results = []
  for city in db:
    req = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
    
    results.append({
      'name': city['name'],
      'timezone': city['timezone'],
      'current_time': req.json()['datetime']
    })

  return results

@app.get('/cities/{city_id}')
def get_city(city_id: int):
  return db[city_id]

@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
  db.pop(city_id)
  return {}

@app.post('/cities')
def create_city(city: City):
  """ add timezone from here http://worldtimeapi.org/api/timezone """
  db.append(city.dict())
  return db