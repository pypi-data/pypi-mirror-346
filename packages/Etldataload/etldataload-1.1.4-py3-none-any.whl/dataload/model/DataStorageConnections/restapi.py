import pandas as pd
import dataload.utils.logger as l
import dataload.conf.model.connection as con
import dataload.model.datastorageconnection as src

import requests

# API REST definition object for connection
class RESTAPISource(src.DataStorageConnection):
    def __init__(self, source):
        self.logger = l.Logger()

        # definition des parameter de la connexion API REST
        self.headers = con.Headers(
            token=source['HEADERS']['x_access_token'],
            content_type=source['HEADERS']['content_type']
        )
        self.api_connect = con.RestAPI(
            base_url=source['BASE_URL'],
            key=source['KEY'],
            headers= self.headers
        )
        self.connection = con.Connection(
            alias=source['ALIAS'],
            type='RESTAPI',
            restapi = self.api_connect
        )

    def read_data(self, query=None):
        self.logger.debug('lecture de la source RESTAPI....')

        # define connection parameter
        base_url = self.api_connect.base_url

        headers = {
                    'x-access-token': self.connection.restapi.headers.token,
                    'Content-Type': self.connection.restapi.headers.content_type
                }

        params = {}

        # if (auth is not None) and (accept is not None) :
        #     headers = {
        #         'Authorization': auth,
        #         'accept': accept
        #     }
        # else:
        #     print("param null dans le header")
        #     headers = {
        #         'Authorization': auth,
        #         'accept': accept
        #     }

        # api request execution
        session = requests.Session()
        response = session.get(base_url, headers=headers, params=params)

        # process the api result
        if response.status_code == 200:
            data = response.json()
            print(data)
            if isinstance(data, list):
                print("data est une liste")
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                print("data est un dictionnaire")
                df = pd.DataFrame([data])
            # df['time_period_end'] = pd.to_datetime(df['time_period_end'])
            return df
        else:
            print(f"Erreur lors de la requête : {response.status_code}")
            return None