# encoding: utf-8

"""
Convenience functions for authenticating with Google
and asking for authorization with Google, with
`authenticate` at its core.

`authenticate` will do what it says on the tin, but unlike
the basic `googleanalytics.oauth.authenticate`, it prompts for information when required and so on.
"""
import re

from . import oauth


def navigate(accounts, account=None, webproperty=None, profile=None, ga_url=None, default_profile=True):
     
    if ga_url:
        return get_profile_from_url(accounts, ga_url)
        
    if webproperty and not account:
        raise KeyError("Cannot navigate to a webproperty or profile without knowing the account.")
    if profile and not (webproperty and account):
        raise KeyError("Cannot navigate to a profile without knowing account and webproperty.")

    if profile:
        return accounts[account].webproperties[webproperty].profiles[profile]
    elif webproperty:
        scope = accounts[account].webproperties[webproperty]
        if default_profile:
            return scope.profile
        else:
            return scope
    elif account:
        return accounts[account]
    else:
        return accounts

    

def get_profile_from_url(accounts, ga_url):
        
  if isinstance(ga_url, str) and "https://analytics.google.com/" in ga_url:
    
    psearch = re.search('^https:\/\/analytics\.google\.com\/analytics\/web\/.*\/a(?P<a>[0-9]+)w(?P<w>[0-9]+)p(?P<p>[0-9]+).*$', str(ga_url), re.IGNORECASE)

    if len(psearch.groups()) == 3:
      return get_profile(accounts, psearch['a'], psearch['w'], psearch['p'])

    else:
      error = 'The URL was not correct.  it should include a portion matching `/a23337837w45733833p149423361/`'

  else:
    error = 'The url provided should start with `https://analytics.google.com\/`'

  raise KeyError(error)

    

def get_profile(accounts, account, webproperty, profile):

  try:
    
    account = accounts[account]
    webproperty = [w for w in account.webproperties if w.raw['internalWebPropertyId'] == webproperty][0]
    profile = webproperty.profiles[profile]

    return profile

  except Exception as e:
    print('Unknown Exception:', str(e))
    return None    


def authenticate(
        service_account_key=None, service_account_subject=None,
        account=None, webproperty=None, profile=None,
        ga_url=None, identity=None, prefix=None,
        suffix=None):
    """
    The `authenticate` function will authenticate the user with the Google Analytics API,
    using a variety of strategies: keyword arguments provided to this function, credentials
    stored in in environment variables, credentials stored in the keychain and, finally, by
    asking for missing information interactively in a command-line prompt.

    If necessary (but only if `interactive=True`) this function will also allow the user
    to authorize this Python module to access Google Analytics data on their behalf,
    using an OAuth2 token.
    """

    accounts = oauth.authenticate(service_account_key, service_account_subject)
    scope = navigate(accounts, account=account, webproperty=webproperty, profile=profile, ga_url=ga_url)
    return scope



def authorize(client_id=None, client_secret=None, client_email=None, private_key=None, identity=None, prefix=None, suffix=None):
    """ Not used anymore.  Keeping here to reduce errors"""
    return None


def revoke(client_id, client_secret,
        client_email=None, private_key=None,
        access_token=None, refresh_token=None,
        identity=None, prefix=None, suffix=None):
    """ Not used anymore.  Keeping here to reduce errors"""
    return None

    
