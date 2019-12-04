import mysql.connector
import json


class DbConnectionManager:
    def __init__(self):
        self.get_db_credentials()

        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.db_name
        )

    def get_db_credentials(self):
        with open(self.db_creds_fp()) as f:
            creds = json.load(f)

            self.host = creds['host']
            self.user = creds['user']
            self.password = creds['password']
            self.db_name = creds['db-name']

    def db_creds_fp(self):
        return 'db_config.json'

DbConnectionManager()
