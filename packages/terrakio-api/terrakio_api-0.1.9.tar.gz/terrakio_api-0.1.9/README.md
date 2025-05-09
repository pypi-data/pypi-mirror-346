# Terrakio API Client

A Python client for Terrakio's Web Coverage Service (WCS) API. This package provides a user-friendly interface for accessing Terrakio's data services.

## Features

- Authentication and user management
- WCS queries and data retrieval
- Efficient data handling with xarray and pandas

## Installation

```bash
pip install terrakio-api
```

## Usage Example

```python
from terrakio_api import Client
from shapely.geometry import Point

# Initialize the client
client = Client(url="https://api.terrak.io", key="your-api-key")

# Create a geographic feature
point = Point(149.057, -35.1548)
geojson = {
     "type": "Feature",
     "geometry": {
          "type": "Point",
          "coordinates": [point.x, point.y]
     },
     "properties": {
          "name": "Location in Canberra region",
          "description": "Coordinates: 149.057, -35.1548"
     }
}

# Make a WCS request
dataset = client.wcs(
     expr="prec=MSWX.precipitation@(year=2024, month=1)\nprec",
     feature=geojson,
     output="netcdf"
)
```

For more documentation, see the [main repository](https://github.com/HaizeaAnalytics/terrakio-python-api). 