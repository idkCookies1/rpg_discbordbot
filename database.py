import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def createTable():
    
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS player_stats ("
            "discord_id BIGINT NOT NULL,"
            "currency INT NOT NULL,"
            "health INT NOT NULL,"
            "attack INT NOT NULL,"
            "armor INT NOT NULL,"
            "level INT NOT NULL,"
            "xp INT NOT NULL,"
            "dungeon_level INT NOT NULL,"
            "equipment TEXT [],"
            "current_health INT NOT NULL)"
        )
        
        cursor.close()
        
        connection.commit()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if connection is not None:
            connection.close()
            
def registerUser(userID):
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = connection.cursor()
        
        existflag = IsUserRegistered(userID)
        
        if not existflag:
            sql = "INSERT INTO player_stats (discord_id, currency, health, attack, armor, level, xp, dungeon_level, equipment, current_health) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (userID, 0, 100, 20, 0, 1, 0, 1, [], 100))
        
        cursor.close()
        
        connection.commit()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if connection is not None:
            connection.close()
    return existflag
        
def IsUserRegistered(userID):
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = connection.cursor()
        
        sql = "SELECT discord_id FROM player_stats WHERE discord_id =" + str(userID)
        
        existflag = None
        
        cursor.execute(sql)
        if cursor.fetchone() is not None:
            existflag = True
            print("user is in the database")
        else:
            existflag = False
            print("user is not in the database")
        
        cursor.close()
        
        connection.commit()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if connection is not None:
            connection.close()
    return existflag

def getInfo(userID):
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode="require")
        cursor = connection.cursor()
        
        sql = "SELECT * FROM player_stats WHERE discord_id =" + str(userID)
        cursor.execute(sql)
        
        player_data = cursor.fetchall()
        
        cursor.close()
        connection.commit()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if connection is not None:
            connection.close()
    
    return player_data


"""# Function to update data base with new column
def updateDatabase():

    try:
        # Connect to Database
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()

        # Excute SQL Statement to create table
        cursor.execute(
            "ALTER TABLE users "
            "ADD COLUMN IF NOT EXISTS exp BIGINT DEFAULT 0 NOT NULL"
            )

        # Close communication to Database
        cursor.close()

        # Commit Changes
        connection.commit()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    # Close Connection
    finally:
        if connection is not None:
            connection.close()
"""
