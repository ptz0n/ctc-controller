import time
from os import environ
from datetime import datetime

environ['BLINKA_MCP2221'] = '1'

import board
from digitalio import DigitalInOut, Direction
from numpy import percentile
from influxdb import InfluxDBClient

from prices import get_prices

relay = DigitalInOut(board.G0)
relay.direction = Direction.OUTPUT

db = InfluxDBClient(
  environ.get('INFLUXDB_HOST'),
  8086,
  environ.get('INFLUXDB_USERNAME'),
  environ.get('INFLUXDB_PASSWORD'),
  environ.get('INFLUXDB_DATABASE')
)

def should_drop():
  prices = get_prices()

  # Index current prices.
  totals = []
  points = []
  for day in ['today', 'tomorrow']:
    for price in prices[day]:
      totals.append(price['total'])
      points.append({
        "measurement": "tibber",
        "time": price['startsAt'],
        "fields": {
          "price": price['total']
        }
      })

  # Send prices to db.
  db.write_points(points)

  # Make sure we heat normally for at least 8 hours.
  return prices['current']['total'] > percentile(totals, 33)

while True:
  relay.value = not should_drop() # Low level trigger.

  # Write current value to db.
  db.write_points([{
    "measurement": "ctc",
    "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    "fields": {
      "drop": int(relay.value) # 0 = dropped, 1 = normal operation
    }
  }])

  print("Operation: %s" % ('normal' if relay.value else 'night drop'))

  time.sleep(10 * 60) # TODO: Sleep until an hour have passed.
