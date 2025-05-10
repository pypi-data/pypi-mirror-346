import pandas as pd
import dataload.utils.logger as l
import dataload.conf.model.connection as con
import dataload.model.datastorageconnection as src

# from mysql.connector import Error, connect
from sqlalchemy import create_engine

class MYSQLSource(src.DataStorageConnection):
    def __init__(self, source):
        self.logger = l.Logger()

        self.mysql_connect = con.Mysql(
            host=source['HOST'],
            user=source['USER'],
            password=source['PASSWORD'],
            port=source['PORT'],
            database=source['DATABASE']
        )
        self.connection = con.Connection(
            alias=source['ALIAS'],
            type='MYSQL',
            mysql=self.mysql_connect
        )

    def read_data(self, query=None):
        self.logger.debug('lecture de la source MYSQL....')
        engine = None
        try:
            user=self.connection.mysql.user
            password=self.connection.mysql.password
            host=self.connection.mysql.host
            database=self.connection.mysql.database
            db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
            engine = create_engine(db_uri)
            df = pd.read_sql(self.connection.query, engine)
            return df

        except Exception as e:
            print(f"Erreur lors de la lecture de la base de données : {e}")

        finally:
            engine.dispose()

    def write_data(self, df=None, table=None, key_columns=None):
        self.logger.debug('ecriture des données dans la BDD Mysql....')
        engine = None
        try:
            user = self.connection.mysql.user
            password = self.connection.mysql.password
            host = self.connection.mysql.host
            database = self.connection.mysql.database
            db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
            engine = create_engine(db_uri)

            existing_data = pd.read_sql_table(table, engine)
            if key_columns is not None:
                key_columns = ['Coin', 'Timestamp']
                index_existing = existing_data.set_index(key_columns).index
                index_entry = df.set_index(key_columns).index
                new_rows = df[~index_entry.isin(index_existing)]
            else:
                new_rows = df

            if not new_rows.empty:
                new_rows.to_sql(table, con=engine, if_exists='append', index=False)

            print(f"Données insérées dans la table {table}.")

        except Exception as e:
            print(f"Erreur lors de l ecriture de la base de données : {e}")

        finally:
            engine.dispose()