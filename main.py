import time
import os

os.environ['BLINKA_MCP2221'] = '1'

import board
from digitalio import DigitalInOut, Direction
from numpy import percentile

from prices import get_prices

relay = DigitalInOut(board.G0)
relay.direction = Direction.OUTPUT

def should_drop():
  prices = get_prices()

  # Index current prices.
  totals = []
  for day in ['today', 'tomorrow']:
    for price in prices[day]:
      totals.append(price['total'])

  # Make sure we heat normally for at least 8 hours.
  return prices['current']['total'] > percentile(totals, 33)

while True:
  relay.value = not should_drop() # Low trigger.
  print(relay.value)
  time.sleep(10 * 60)
