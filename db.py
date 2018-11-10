import pymysql
import csv
import numpy as np
from connect import DBconnect

def GetAllRally(connection):
    
    mycursor = connection.cursor()

    sql="""select distinct unique_id,rally from clip_info order by unique_id,rally; 
                """
    mycursor.execute(sql)  
    connection.commit() 
    
    result = mycursor.fetchall()
    result = np.asarray(result)
    
    mycursor.close()  
     
    return result
def GetLoseRally(connection,player):
    
    mycursor = connection.cursor()

    sql="""select distinct unique_id,rally from clip_info where getpoint_player = %s order by unique_id,rally; 
                """
    mycursor.execute(sql,player)  
    connection.commit() 
    
    result = mycursor.fetchall()
    result = np.asarray(result)
    
    mycursor.close()  
     
    return result
def GetRallyPosition(connection,unique_id,rally):
    
    mycursor = connection.cursor()

    sql="""select hit_x,hit_y from clip_info where unique_id = %s and rally = %s; 
                """
    mycursor.execute(sql,(unique_id,rally))  
    connection.commit() 
    
    result = mycursor.fetchall()
    result = np.asarray(result)
    
    mycursor.close()  

    return result

def GetRallyType(connection,unique_id,rally):
    
    mycursor = connection.cursor()

    sql="""select type from clip_info where unique_id = %s and rally = %s; 
                """
    mycursor.execute(sql,(unique_id,rally))  
    connection.commit() 
    
    result = mycursor.fetchall()
    result = np.asarray(result)
    
    mycursor.close()  

    return result

def GetRallyType(connection,unique_id,rally):
    
    mycursor = connection.cursor()

    sql="""select type from clip_info where unique_id = %s and rally = %s; 
                """
    mycursor.execute(sql,(unique_id,rally))  
    connection.commit() 
    
    result = mycursor.fetchall()
    result = np.asarray(result)
    
    mycursor.close()  

    return result

def GetCourtUpper(connection,unique_id):
    
    mycursor = connection.cursor()

    sql="""select player_ename,player_num from player_info where unique_id = %s and half_court = 'upper'; 
                """
    mycursor.execute(sql,unique_id)  
    connection.commit() 
    
    result = mycursor.fetchall()
    result = np.asarray(result)
    
    mycursor.close()  

    return result[0]

def GetCourtLower(connection,unique_id):
    
    mycursor = connection.cursor()

    sql="""select player_ename,player_num from player_info where unique_id = %s and half_court = 'lower'; 
                """
    mycursor.execute(sql,unique_id)  
    connection.commit() 
    
    result = mycursor.fetchall()
    result = np.asarray(result)
    
    mycursor.close()  

    return result[0]

def GetRallyPoints(connection,unique_id,rally,player):
    
    mycursor = connection.cursor()

    if player == 'A':
        sql="""select roundscore_A from clip_info where unique_id = %s and rally = %s limit 1; 
                """
    if player == 'B':
        sql="""select roundscore_B from clip_info where unique_id = %s and rally = %s limit 1; 
                """
    mycursor.execute(sql,(unique_id,rally))  
    connection.commit() 
    
    result = mycursor.fetchall()
    result = np.asarray(result)
    
    mycursor.close()  

    return result[0][0]

# connection = DBconnect()
# print(GetRallyPoints(connection,'2018-Indonesia_open-finals-1-1',1,'B'))