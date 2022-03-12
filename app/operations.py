from sqlite3 import Time
import mysql.connector
from mysql.connector import errorcode
import os
from datetime import datetime, timedelta
from app.models import *

import string
import random
import pytz


# "user": 'mmlink',
#     "password": 'Mmlink@271020',
#     "host": '139.59.28.3',
#     "database": 'ers'
config = {
    
}


def connectToDB(conf):
    result = {}
    try:
        cnx = mysql.connector.connect(**conf)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            result['table'] = []
            result['message'] = "Something is wrong with your user name or password" 
            #  {table:[],msg:"Something is wrong with your user name or password"}
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            result['table'] = []
            result['message'] = "Database does not exist" 
            # return {table:[],msg:"Database does not exist"}
        else:
            result['table'] = []
            result['message'] = err
            # return {table:[],msg:err}
    else:
        table = getTableNames(cnx)
        result['table'] = table
        result['message'] = "Database Connected Successfully!"
        global config 
        config = conf
        cnx.close()
        # return {table:table,msg:"Database Connected Successfully!"}
    return result



def getTableNames(cnx):
    cursor = cnx.cursor()
    query = 'SHOW TABLES'
    cursor.execute(query)
    tableList = cursor.fetchall()
    tables = []
    for t in tableList:
        tables.append(t[0])
    return tables
















def search_solardata(config,start, end, parameters, selecteddevice, weather):
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor()
    data = []
    TimeField = get_Time_Column(cnx,config['database'],selecteddevice)
    if len(parameters) != 0 and len(selecteddevice) != 0:
        parameters = "`,`".join(parameters)
        print(parameters)
        for device in selecteddevice:
            query = f"SELECT `{TimeField}`,`{parameters}` FROM {device} WHERE `{TimeField}` BETWEEN '{start}' AND '{end}'"
            # print(query)
            cursor.execute(query)
            data.append(cursor.fetchall())
    # else:
    #     data.append([])
    if len(weather) != 0:
        weather = "`,`".join(weather)
        query1 = f"SELECT `{TimeField}`,`{weather}` FROM wms WHERE `{TimeField}` BETWEEN '{start}' AND '{end}'"
        cursor.execute(query1)
        data.append(cursor.fetchall())

    cursor.close()
    cnx.close()
    return data


# Live data of solardevice
def get_livedata_solar(device):
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor(buffered=True)
    datalist = []
    IST = pytz.timezone('Asia/Kolkata')
    # print(datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S'))
    if int(datetime.now(IST).strftime('%M')) % 5 == 0:
        date = datetime.now(IST)
    elif int(datetime.now(IST).strftime('%M')) % 5 <= 5:
        date = datetime.now(IST) - timedelta(minutes=int(datetime.now(IST).strftime('%M')) % 5)

    updateddate = "2021-01-23 " + date.strftime('%H:%M') + ":00"

    for i in device:
        # device_parameters = (",").join(get_solar_column_name(i))
        # print(device_parameters)
        # {'%s' + (',%s' * (len(get_solar_column_name(i)) - 1))}
        query = f"SELECT * FROM {i} where TimeCol = '{updateddate}'"
        cursor.execute(query)
        data = cursor.fetchone()
        data = list(data)
        data[0] = data[0].replace(day=datetime.now(IST).day, month=datetime.now().month, year=datetime.now().year)
        # print(data[0])
        datalist.append(data)
    cursor.close()
    cnx.close()
    return datalist


def get_live_weatherparam_data():
    cnx = mysql.connector.connect(**config)
    cnx.time_zone = '+05:30'
    cursor = cnx.cursor(buffered=True)
    IST = pytz.timezone('Asia/Kolkata')
    # print(datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S'))
    if int(datetime.now(IST).strftime('%M')) % 5 == 0:
        date = datetime.now(IST)
    elif int(datetime.now(IST).strftime('%M')) % 5 <= 5:
        date = datetime.now(IST) - timedelta(minutes=int(datetime.now(IST).strftime('%M')) % 5)

    updateddate = "2021-10-13 " + date.strftime('%H:%M') + ":00"
    query = f"SELECT * FROM wms where TimeCol = '{updateddate}'"
    cursor.execute(query)
    datalist = cursor.fetchone()
    datalist = list(datalist)
    datalist[0] = datalist[0].replace(day=datetime.now(IST).day, month=datetime.now().month, year=datetime.now().year)
    cursor.close()
    cnx.close()
    return datalist


# to get the parameter names of device
def get_solar_column_name(config,devicename):
    
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    query = f"SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='{config['database']}' AND `TABLE_NAME`='{devicename}' ORDER BY ORDINAL_POSITION"
    cursor.execute(query)
    col_name = []
    data = cursor.fetchall()
    print(data)
    # [('Date',), ('STB 2.2.2 - 1 - I1 [A]',), ('STB 2.2.2 - 1 - I10 [A]',), ('STB 2.2.2 - 1 - I11 [A]',), ('STB 2.2.2 - 1 - I12 [A]',), ('STB 2.2.2 - 1 - I13 [A]',), ('STB 2.2.2 - 1 - I14 [A]',), ('STB 2.2.2 - 1 - I15 [A]',), ('STB 2.2.2 - 1 - I16 [A]',), ('STB 2.2.2 - 1 - I2 [A]',), ('STB 2.2.2 - 1 - I3 [A]',), ('STB 2.2.2 - 1 - I4 [A]',), ('STB 2.2.2 - 1 - I5 [A]',), ('STB 2.2.2 - 1 - I6 [A]',), ('STB 2.2.2 - 1 - I7 [A]',), ('STB 2.2.2 - 1 - I8 [A]',), ('STB 2.2.2 - 1 - I9 [A]',), ('STB 2.2.2 - 1 - Total power [W]',), ('STB 2.2.2 - 1 - Total voltage [V]',)]
    for d in range(0, len(data)):
        # print(d[0])
        col_name.append(data[d][0])
    # print(col_name)

    cursor.close()
    cnx.close()
    return col_name


def get_Time_Column(cnx,db,table):

    cursor = cnx.cursor(buffered=True)
    query = "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`= %s AND `TABLE_NAME`= %s ORDER BY ORDINAL_POSITION"
    cursor.execute(query,(db,table[0]))
    data = cursor.fetchall()
    return data[0][0]




def solar_genration():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)
    query = f"SELECT `Power AC (Inv 5.1) [W]` FROM inv_1"
    cursor.execute(query)
    data = cursor.fetchall()
    newdata = []
    solardata = [0 for i in range(24)]
    for d, in data:
        newdata.append(d)
    for i in range(0, len(newdata)):
        solardata[i // 12] += newdata[i] / 12000

    cursor.close()
    cnx.close()
    return solardata






def convert_to_Json(labels,legends,selected):

    arr = []
    for j in range(0,len(labels)):
        obj = {}
        obj['datetime'] = labels[j]
        for i in range(0,len(legends)):
            obj[legends[i]] = selected[i][j]
        
        arr.append(obj)
    return arr

