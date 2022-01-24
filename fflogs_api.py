import graphene
import extraction
from requests.structures import CaseInsensitiveDict 
import requests
import json

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

f = open('client_info.json')
clientInfo = json.load(f)
clientID = clientInfo['id']
clientSecret = clientInfo['secret']

FFLOGS_OAUTH_URL = "https://www.fflogs.com/oauth/token"
FFLOGS_URL = "https://www.fflogs.com/api/v2/client"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"

data = "grant_type=client_credentials"


response = requests.post(FFLOGS_OAUTH_URL, headers=headers, data=data, auth=(clientID, clientSecret))
print(f'Status code: {response.status_code}')

token = response.json()['access_token']
# print(token)


# -------------------------------------------------------

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url=FFLOGS_URL, headers=headers)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    query getContinents {
      continents {
        code
        name
      }
    }
"""
)

query = gql("""
    query {
        characterData{
            character(name: "Calad Baal"
                    serverSlug: "Spriggan"
                    serverRegion: "EU"
            ) {
            zoneRankings(zoneID: 0)
            }
        }
    }
""")

# me
# query = gql("""
#     query {
#         characterData{
#             character(id: 17421979) {
#             zoneRankings(zoneID: 42)
#             }
#         }
#     }
# """)

# Kimi
query = gql("""
    query {
        characterData{
            character(name: "K'imi Verona"
                    serverSlug: "Coeurl"
                    serverRegion: "NA"
            ) {
            encounterRankings(encounterID: 1058)
            }
        }
    }
""")
# query = gql("""
#     query {
#         characterData{
#             character(name: "K'imi Verona"
#                     serverSlug: "Coeurl"
#                     serverRegion: "NA"
#             ) {
#             zoneRankings(zoneID: 0)
#             }
#         }
#     }
# """)


# report
query = gql("""
    query {
        reportData{
            report(code: "p74QHJhZ2cB8FmXa"){
                fights {
                    averageItemLevel
                    bossPercentage
                    fightPercentage
                    name
                }
            }
        }
    }
""")

# rate limit
# query = gql("""
#     query {
#         rateLimitData {
#             limitPerHour
#             pointsSpentThisHour
#             pointsResetIn
#         }
#     }
# """)




# Execute the query on the transport
result = client.execute(query)
# print(result)
print(json.dumps(result, indent=4, sort_keys=True))
