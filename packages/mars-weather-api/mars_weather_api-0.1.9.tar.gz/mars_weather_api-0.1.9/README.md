# mars_weather_api

This is a Python wrapper for NASA's InSight Mars Weather Service API. It allows users to fetch and display weather data from Mars, including temperature details. Please note that the API can only access weather data for the last 7 sols (Martian days) that the InSight lander was active.

## Usage

To use the `mars_weather_api`, first import the library and initialize it:

```python
import mars_weather_api
from mars_weather_api import mars_weather_api
api = mars_weather_api.MarsWeatherAPI("your_nasa_api_key")
api.print_week()
```

## Installation

```shell
$ python -m pip install mars_weather_api
```

## Features

- Fetch weather data for a specific sol (Martian day).
- Retrieve weather data for the last 7 sols.
- Extract temperature details (average, minimum, maximum) for each sol.
- Easy-to-use Python interface with formatted output.

## Requirements

- Python 3.7 or higher
- An active NASA API key (you can get one [here](https://api.nasa.gov/)).

## Note

This is a school project and is not open for contributions.
