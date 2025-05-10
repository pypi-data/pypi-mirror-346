import pandas as pd
import dataload.utils.logger as l
import dataload.model.datastorageconnection as src

import sqlalchemy

# POSTGRESQL SQL definition object for connection
class POSTGRESQL(src.DataStorageConnection):
    def __init__(self, source):
        self.user = source['USER']
        self.password = source['PASSWORD']
        self.host = source['HOST']
        self.port = source['PORT']
        self.database = source['DATABASE']
        self.logger = l.Logger()

    def read_data(self, query=None):
        self.logger.debug('lecture de la source SQL....')
        engine = sqlalchemy.create_engine(
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}")
        return pd.read_sql(query, engine)
