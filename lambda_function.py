"""
This lambda function accepts an external post request with a JSON body like this:
    {
    "datetime": "2024-02-08 06:12:11",
    "send_id": "WhOeRlLlDo",
    "event": "delivered"
    }
and writes that data into the SQLite table [email_events] hosted on an EFS filesystem mounted on /mnt/efs/user_data.db 

This code is extremely incomplete - I was still at the point of commenting and uncommenting different bits as I needed them.
"""

import json
import sqlite3
import subprocess


def lambda_handler(event, context):
    # subprocess.run(["rm","/mnt/efs/user_data.db"]) # delete the database

    try:
        sql = sqlite3.connect("/mnt/efs/user_data.db")
        # sql.execute('PRAGMA journal_mode=wal') # facilitates concurrent writes - only need to do this once for the DB
        # sql.execute('PRAGMA locking_mode=EXCLUSIVE') # stops errors related to distributed system - only need to do this once for the DB
        # sql.execute("CREATE TABLE email_events (datetime DATETIME, send_id TEXT, event TEXT);")

        # sql_cursor = sql.cursor(); sql_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';"); table_names = sql_cursor.fetchall()
        # sql.execute("""INSERT INTO email_events (datetime, send_id, event) VALUES ("2024-12-05 11:55:54", "5e2o4j09", "hard bounce")"""); sql.commit()
        # sql_cursor = sql.cursor(); sql_cursor.execute("SELECT COUNT(*) from email_events;"); fetch_one = sql_cursor.fetchone()[0]
        # sql_cursor = sql.cursor(); sql_cursor.execute("SELECT * FROM email_events;"); select_all = sql_cursor.fetchall()

        # insert record from external post request to lambda URL #
        request_json = json.loads(event["body"])
        sql.execute(
            """
            INSERT INTO email_events (datetime, send_id, event)
            VALUES (?, ?, ?)
            """,
            (request_json["datetime"], request_json["send_id"], request_json["event"]),
        )
        sql.commit()

        sql.close()

        return {
            "statusCode": 200,
            "body": "OK",
            # "files_on_efs": subprocess.run(["ls", "/mnt/efs"], stdout=subprocess.PIPE, text=True).stdout.split()
        }

    except Exception as err:
        return {"statusCode": 500, "body": str(err)}
