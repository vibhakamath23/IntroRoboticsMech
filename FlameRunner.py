'''
by Maddie Pero 
Edited by Ethan, Vibha, and Cardi

In this example we will get data from Airtable.
'''

'''
These statements allow us to make get requests of the Airtable API & parse that information
'''
import requests # you may need to run 'pip install requests' to install this library
import json 


''' This function makes a get request to the airtable API which will tell us how fast to spin the wheels'''

''' Put the URL for your Airtable Base here'''
''' Format: 'https://api.airtable.com/v0/BaseID/tableName '''
URL = 'https://api.airtable.com/v0/appRKhczb0hVWRjFF/Table%201'



''' Format: {'Authorization':'Bearer Access_Token'}
Note that you need to leave "Bearer" before the access token '''
Headers = {'Authorization':'Bearer patY3r4zobCuX8W0e.70be6f31bc1dd09d216d4c6bced3a8f744475b949f6ad58e24701436db75e59b'}

def get_data(): 
    r = requests.get(url = URL, headers = Headers, params = {})
    '''
    The get request data comes in as a json package. We will convert this json package to a python dictionary so that it can be parsed
    '''
    data = r.json()
    print(data)
    # print(data['records'][2]['fields']['X'])
    linear = data['records'][2]['fields']['X']
    angular = data['records'][3]['fields']['Z']

    return (linear, angular)
