# CTC Controller

Retrofitting of an old CTC Ecoheat geothermal heat pump to act on electricity price fluctuations.

## Interfaces

### Output: Heat pump

Our heat pump does support an external control switch to be connected for activating a feature they call "Night drop". When activated, the target indoor temperature is dropped according to the setting. If Night drop is set to -5° C and activated, the target will drop from 22 to 17° C until deactivated.

![CTC Ecoheat terminal block](/ctc-io.png)

### Input: Electricity price

We're using [Tibber](https://tibber.com/se/invite/fb7a2cc5) and they have a great API for getting the current prices.

```json
{
  "total": 0.2328,
  "energy": 0.1658,
  "tax": 0.067,
  "startsAt": "2021-11-23T00:00:00.000+01:00"
}
```

### Controller: USB controlled relay

I could have used a RaspberryPi (or similar) but wanted to try out the [Adafruit MCP2221A Breakout](https://www.adafruit.com/product/4471), which I hooked up to my home server via USB. Using a compatible one channel relay module and some Python logic to analyze the current prices to know when we should activate the Night drop.

## Installation

After setting up the required hardware, run:

```bash
pip3 install -r requirements.txt
python3 main.py
```
