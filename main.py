import os
from discord.ext import commands
import datetime
from dateutil import tz
from math import floor
import pickle
from keep_alive import keep_alive

db = {}

if os.path.exists("database.pkl"):
  with open("database.pkl", 'rb') as db_put:
    db = pickle.load(db_put)

TOKEN = os.environ['DISCORD_TOKEN']

client = commands.Bot(command_prefix='!')

def ahora():
  return datetime.datetime.now(tz.gettz("Europe/Madrid"))

def guardarDB():
  with open("database.pkl", 'wb') as db_put:
    pickle.dump(db, db_put)

@client.command()
async def fichar(ctx):
  username = ctx.author.nick
  moment = ahora()
  if username in db.keys():
    db[username]["start"] = moment
    await ctx.send(f"{username} ha empezado a trabajar")
  else:
    db[username] = {"start": moment, 'weekly': 0}
    await ctx.send(f"Registrado {username}, ha empezado a trabajar")
  guardarDB()
  
    
@client.command()
async def parar(ctx):
  username = ctx.author.nick
  moment = ahora()
  if username in db.keys():
    if "start" in db[username]:
      start_moment = db[username].pop("start")
      diff = moment - start_moment
      tiempo_sec = diff.total_seconds()
      weekly_sec = db[username]["weekly"]
      weekly_sec += tiempo_sec
      db[username]["weekly"] = weekly_sec
      horas = floor(weekly_sec/3600)
      minutos = floor((weekly_sec%3600)/60)
      start_min = start_moment.minute
      if start_min < 10:
        start_min = '0'+str(start_min)
      stop_min = moment.minute
      if stop_min < 10:
        stop_min = '0'+str(stop_min)
      user_string = f"Nombre del empleado: {username}"
      dia_string = f"Día: [{moment.day}/{moment.month}]"
      entrada_string = f"Hora de entrada: [{start_moment.hour}.{start_min}]"
      salida_string = f"Hora de salida: [{moment.hour}.{stop_min}]"
      horas_weekly_string = f"Horas semanales: [{horas}h{minutos}min]"
      await ctx.send(f"{user_string}\n{dia_string}\n{entrada_string}\n{salida_string}\n{horas_weekly_string}")
      guardarDB()
      return
  await ctx.send("Error, {} no ha empezado a fichar".format(username))

@client.command()
async def reset(ctx):
  username = ctx.author.nick
  db[username]['weekly'] = 0
  await ctx.send("Horas semanales reseteadas")

#  for key in db.keys():
#    if 'weekly' in db[key]:
#      db[key]['weekly'] = 0
#  

#Comentado el comando reset hasta que arreglemos el asunto

keep_alive()
client.run(TOKEN)