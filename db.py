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

# connection = DBconnect()
# print(GetRallyType(connection,'2018-Indonesia_open-finals-1-1','25'))