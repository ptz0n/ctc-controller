import os

import requests

# Get prices from Tibber.
query = """
{
  viewer {
    homes {
      currentSubscription {
        priceInfo {
          current {
            ...PriceParts
          }
          today {
            ...PriceParts
          }
          tomorrow {
            ...PriceParts
          }
        }
      }
    }
  }
}

fragment PriceParts on Price {
  total
  startsAt
}
"""

options = {
  "json": { "query": query },
  "headers": { "Authorization": "Bearer " + os.environ.get('TIBBER_TOKEN', '') }
}

def get_prices():
  response = requests.post('https://api.tibber.com/v1-beta/gql', **options)
  return response.json()['data']['viewer']['homes'][0]['currentSubscription']['priceInfo']
