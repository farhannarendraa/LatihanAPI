# import package
from fastapi import FastAPI, HTTPException, Header
import psycopg2
import pandas as pd

# create FastAPI object
app = FastAPI()

# api password
password = "postgres"

def getConnection():
    # create connection
    conn = psycopg2.connect(
        dbname="neondb", user="neondb_owner", password="npg_sLfVg8iW4EwO",
        host="ep-steep-water-a102fmjl-pooler.ap-southeast-1.aws.neon.tech",
    )

    return conn

# endpoint
@app.get('/')
async def getWelcome():
    return {
        "msg": "sample-fastapi-pg"
    }


@app.get('/profiles')
async def getProfiles():
    # define connection
    connection = getConnection()
    df = pd.read_sql("SELECT * FROM profiles", connection)
    return {
        "data": df.to_dict(orient = "records")
    }

# endpoint - protected
@app.get('/profiles/{id}')
async def getProfileById(id: int, api_key: str = Header(None)):
    if api_key == None or api_key != password:
        raise HTTPException(status_code = 401, detail = "Password Salah")
                        
    connection = getConnection()
    df = pd.read_sql(f"SELECT * FROM profiles WHERE id = {id}", connection)

    if len(df) == 0:
        raise HTTPException(status_code = 404, detail = "data not found")
    return {
        "data": df.to_dict(orient = "records"),
        "columns": list(df.columns)}



# @app.post(...)
# async def createProfile():
#     pass


# @app.patch(...)
# async def updateProfile():
#     pass


# @app.delete(...)
# async def deleteProfile():
#     pass
