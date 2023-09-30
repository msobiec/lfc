#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import time
import psycopg2
import sys
import pytz

def get_people_count(url, place_name):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        place_data_elems = soup.find(id='list-view').find_all(itemtype='http://schema.org/Place')
        elems_with_right_name = [e for e in place_data_elems if e.find(string=place_name)]
        place_data = elems_with_right_name[0]
        counter_container_elem = place_data.find('p', string='Aktualne obciążenie').parent
        people_count_elem = counter_container_elem.find(class_='overview-value')
        people_count_text = people_count_elem.text
        people_count = [int(i) for i in people_count_text.split() if i.isdigit()][0]
        return people_count
    except:
        return -999

def add_record_to_db(people_count):
    conn = psycopg2.connect(
        dbname=os.getenv('PGDATABASE'),
        user=os.getenv('PGUSER'),
        password=os.getenv('PGPASSWORD'),
        host=os.getenv('PGHOST'),
        port=os.getenv('PGPORT')
    )
    cursor = conn.cursor()
    sql_cmd = '''INSERT INTO counter_data 
        (time, count) VALUES (%s, %s)'''
    now_time = datetime.now(tz=pytz.timezone('Europe/London'))
    cursor.execute(sql_cmd, (now_time, people_count))
    conn.commit()
    cursor.close()
    conn.close()

def main():
    args = sys.argv
    url = args[1]
    place_name = args[2]

    while(True):
        # Record data in 5 minute intervals
        now_minutes = datetime.now().minute
        while (now_minutes % 5 != 0):
            now_minutes = datetime.now().minute
            time.sleep(15)
        add_record_to_db(get_people_count(url, place_name))
        time.sleep(61)
            
if __name__ == '__main__':
    main()
