from requests.structures import CaseInsensitiveDict 
import requests
import json

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

'''
TODO:
Functions:
- getGuildSummary
- getReportSummary


Save data to db/file:
- All data centers and their respective worlds
    - updateServers (half done -> have to organize and save data somewhere)
- All zones with encounters and patch cycles
    - updateEncounters/updateZones (half done -> have to organize and save data somewhere)

Other:
- Return result of query instead of just printing it

DONE:
Functions:
- prettyPrint
'''

# Optain clientID and clientSecret from .json file
f = open('client_info.json')
clientInfo = json.load(f)
clientID = clientInfo['id']
clientSecret = clientInfo['secret']

FFLOGS_OAUTH_URL = "https://www.fflogs.com/oauth/token"
FFLOGS_URL = "https://www.fflogs.com/api/v2/client"

# Global access token var
token = ""




def refreshToken():
    global token
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = "grant_type=client_credentials"

    response = requests.post(FFLOGS_OAUTH_URL, headers=headers, data=data, auth=(clientID, clientSecret))
    print(f'Status code: {response.status_code}')

    token = response.json()['access_token']

def setupClient():
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
    }

    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url=FFLOGS_URL, headers=headers)

    # Create a GraphQL client using the defined transport
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client




def getRateLimit():
    client = setupClient()
    query = gql("""
        query {
            rateLimitData {
                limitPerHour
                pointsSpentThisHour
                pointsResetIn
            }
        }
    """)
    result = client.execute(query)
    print(json.dumps(result, indent=4, sort_keys=True))


def prettyPrint(result):
    print(json.dumps(result, indent=4, sort_keys=True))




def updateServers():
    client = setupClient()
    query = gql("""
        query {
            worldData{
                regions {
                    compactName
                    subregions {
                        name
                        servers {
                            data {
                                name
                            }
                        }
                    }
                }
            }
        }
    """)
    result = client.execute(query)
    prettyPrint(result)


def updateEncounters():
    client = setupClient()
    query = gql("""
            query {
                worldData{
                    expansions{
                        name
                        zones {
                            difficulties{id, name}
                            id
                            name
                            frozen
                            brackets {
                                min
                                max
                            }
                            encounters {
                                id
                                name
                            }
                        }
                    }
                }
            }      
    """)
    result = client.execute(query)
    prettyPrint(result)


def getCharSummary(name="", serverSlug="", serverRegion="", id=0):
    client = setupClient()

    # GQL Query by character ID
    if id != 0:
        query = gql(f"""
            query {{
                characterData{{
                    character(id: {id}) {{
                        zoneRankings(zoneID: 0)
                    }}
                }}
            }}
        """)

    # GQL Query by Name, Slug, and Region
    elif (name and serverSlug and serverRegion != ""):
        query = gql(f"""
            query {{
                characterData {{
                    character(name: "{name}"
                    serverSlug: "{serverSlug}"
                    serverRegion: "{serverRegion}"
                    ) {{
                        zoneRankings(zoneID: 0)
                    }}
                }}
            }}
        """)

    result = client.execute(query)
    prettyPrint(result)



def getGuildSummary():
    pass



def getReportSummary():
    pass

