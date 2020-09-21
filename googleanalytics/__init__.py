# encoding: utf-8

import pkg_resources
import re

from . import auth, commands, tests, utils, account, auth, blueprint, columns, errors, query, segments
from .auth import authenticate, authorize, revoke
from .blueprint import Blueprint

__version__ = pkg_resources.get_distribution("googleanalytics").version



def get_profile_from_url(ga_url):
        
  if isinstance(ga_url, str) and "https://analytics.google.com/" in ga_url:
    psearch = re.search('^https:\/\/analytics\.google\.com\/analytics\/web\/.*\/a(?P<a>[0-9]+)w(?P<w>[0-9]+)p(?P<p>[0-9]+).*$', str(ga_url), re.IGNORECASE)

    if len(psearch.groups()) == 3:
      return get_profile(psearch['a'], psearch['w'], psearch['p'])
    else:
      error = 'The URL was not correct.  it should include a portion matching `/a23337837w45733833p149423361/`'

  else:
    error = 'The url provided should start with `https://analytics.google.com\/`'

  raise errors.GoogleAnalyticsError(error)

    

def get_profile(account, webproperty, profile):

  try:

    accounts = authenticate(
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET, 
        identity=IDENTITY, 
        interactive=True
    )

    account = accounts[account]
    webproperty = [w for w in ga_a.webproperties if w.raw['internalWebPropertyId'] == webproperty.strip()][0]
    profile = ga_w.profiles[profile]

    return profile

  except errors.GoogleAnalyticsError as e:
      print('Error: ', str(e))
      return None
