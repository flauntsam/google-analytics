# encoding: utf-8


import addressable

import googleapiclient.discovery as discovery
from google.oauth2 import service_account

from googleanalytics import utils, account



def get_service_credentials(service_account_key, service_account_subject):
    return service_account.Credentials.from_service_account_file(service_account_key, 
                                                                 scopes=['https://www.googleapis.com/auth/analytics.readonly'], 
                                                                 subject=service_account_subject

                                                                 
def authenticate(service_account_key, service_account_subject):

    service = discovery.build('analytics', 'v3', 
                              credentials=get_service_credentials(service_account_key, service_account_subject), 
                              cache_discovery=False)

    raw_accounts = service.management().accounts().list().execute()['items']
    accounts = [account.Account(raw, service, credentials) for raw in raw_accounts]
    return addressable.List(accounts, indices=['id', 'name'], insensitive=True)
