import os 
if os.environ['ENV'] == 'local':
    postgres = {'drivername': 'postgresql+psycopg2',
                'host': 'localhost',
                'username': 'localhost',
                'password': 'localhost',
                'database': 'x-database',
                'port': 5432}