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

# query = gql("""
#     query {
#         rateLimitData {
#             limitPerHour
#         }
#     }
# """)


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}



# Execute the query on the transport
result = client.execute(query)
print(result)
