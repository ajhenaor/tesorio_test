import os
import json
import psycopg2
import logging
from uuid import UUID
from flask import Flask, request

app = Flask(__name__)

def get_conn():
    host= 'db'
    dbname= 'tesorio'
    user= 'postgres'
    password= 'postgres'
    try:
        logging.warning('connecting...')
        # connect to the database
        conn = psycopg2.connect(host= host, database= dbname, user= user, password= password)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        return False

def create_table():
    """ create tables in the PostgreSQL database"""
    sql ="""
            CREATE TABLE IF NOT EXISTS measurement (
                utime varchar(255) NOT NULL,
                partition char(1) NOT NULL,
                uuid uuid NOT NULL,
                hastags varchar(255) NOT NULL
            );
        """
    conn = None
    try:
        conn = get_conn()
        logging.warning('cursor...')
        cur = conn.cursor()
        # create table one by one
        cur.execute(sql)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        return False
    finally:
        if conn is not None:
            conn.close()
            return True

def insert_data(measurement_list):
    sql = """INSERT INTO measurement (utime, partition, uuid, hastags) VALUES(%s, %s, %s, %s);"""
    conn = None
    try:
        conn = get_conn()
        logging.warning('cursor...')
        cur = conn.cursor()
        # execute the INSERT statement
        logging.warning('inserting...')
        cur.executemany(sql, measurement_list)
        # commit the changes to the database
        logging.warning('committing...')
        conn.commit()
        logging.warning('{} rows inserted...'.format(cur.rowcount))
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        return False
    finally:
        if conn is not None:
            conn.close()
            return True

def check_format(line_array):
    '''
        In this function the array format is inspected to check if:
            1- The partition belongs to valid values: 1, 2, 3, 4
            2- The UUID is a valid UUID
            3- There is at least a hastag
    '''
    try:
        if line_array[1] in ('1', '2', '3', '4') and UUID(line_array[2]) is not None and line_array[3] is not None:
            return True
    except Exception as error:
        return False

@app.route('/save_data', methods=['POST'])
def save_data():
    #The table should be created by the initdb process of Postgres. However, sometime it fails. So,
    #in that case the table is created using python
    create_table()
    # Read the file...
    file = request.files['myfile']
    # Save the file in a temp directory...
    file.save(os.path.join("/temp/temp.txt"))

    measurement_list = []
    with open("/temp/temp.txt") as fp:
        for cnt, line in enumerate(fp):
            try:
                line_array = line.rstrip().split(',')
                logging.warning(line_array)
                if check_format(line_array):
                    measurement = (line_array[0], line_array[1], line_array[2], ', '.join(line.split(',')[3:]))
                    logging.warning(measurement)
                    measurement_list.append(measurement)
            except Exception as error:
                pass
    if (insert_data(measurement_list)):
        return json.dumps({'success' : True, 'status' : 200, 'author' : '@ajhenaor', 'version' : '1.0'})
    else:
        return json.dumps({'fail' : True, 'status' : 200, 'author' : '@ajhenaor', 'version' : '1.0'})

@app.route('/clean_db', methods=['GET'])
def clean_db():
    sql = """INSERT INTO measurement (utime, partition, uuid, hastags) VALUES(%s, %s, %s, %s);"""
    conn = None
    try:
        conn = get_conn()
        logging.warning('cursor...')
        cur = conn.cursor()
        # execute the INSERT statement
        logging.warning('inserting...')
        cur.execute("DELETE FROM measurement")
        # commit the changes to the database
        logging.warning('committing...')
        conn.commit()
        # Commit the changes to the database
        logging.warning('{} rows deleted...'.format(cur.rowcount))
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        return json.dumps({'success' : True, 'status' : 200, 'author' : '@ajhenaor', 'version' : '1.0'})
    finally:
        if conn is not None:
            conn.close()
            return json.dumps({'fail' : True, 'status' : 200, 'author' : '@ajhenaor', 'version' : '1.0'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
