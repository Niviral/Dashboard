import pandas as pd 
import numpy as np
import json
import encry
from hdbcli import dbapi
import sys 

config = '/mnt/c/_KOD_/Skrypty/config.json'

def get_data(config_location):
    with open(config_location, "r") as config: #importing "hashed" passwords from JSON config file 
        credentials = json.load(config)

    connect = dbapi.connect(credentials["HANA"]["HANA_ADRESS"], 30015,  # encrypted SAP HANA username and password
                            credentials["HANA"]["HANA_USER"], encry.Decryptor(
                                encry.key, bytes(credentials["HANA"]["HANA_PASSWORD"], 'UTF-8')))

    sql = """
            SELECT
                substring(DATETIME_ADDED,1,10) AS Date,
                TO_TIME(substring(DATETIME_ADDED,11,20)) as TIME,
                QUERY_RAW_PHRASE,
                ITEM_COUNT,
                LOG_TIME
            FROM WWW_TRAFFIC_TEP.SEARCH_CONTEXT
            WHERE
                ACTION_ID = '/search'
                AND QUERY_RAW_PHRASE IN ('5kV 10W 2500mA','1kV 0,001kW 100kohm','DC/DC 5V 1W','kabel')
                AND BROWSER_IP = '172.16.3.254'
            ORDER BY DATETIME_ADDED DESC
        """

    cursor = connect.cursor()
    cursor.execute(sql)
    df = pd.DataFrame.from_records(cursor.fetchall(), columns=[
        x[0] for x in cursor.description])
    df.to_csv('hana_search.csv',',', encoding='UTF-8', index=False)

get_data(config)