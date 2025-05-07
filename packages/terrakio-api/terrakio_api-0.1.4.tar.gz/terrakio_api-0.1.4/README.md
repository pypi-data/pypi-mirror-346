# Terrakio API Client

A Python client for Terrakio's Web Coverage Service (WCS) API.

## Installation

Install the package using pip:

```bash
$ pip install terrakio-api==0.1.4
```

## Configuration

1. Obtain a Personal Access Token:
   - Open the following link for the terrakio_doc - https://test-341.gitbook.io/terrakio/terrak.io/authentication
   - Sign up for the terrakio platform illustrated in the doc
   - Log in for the terrakio platform illustrated in the doc
   - Generate the key for the platform
   - The above generate command should have generated a config file (`$HOME/.tkio_config.json`, if you are on a linux system, the $HOME indicates the root), in which it stores the EMAIL and the TERRAKIO_API_KEY
   - The personal access key is being stored here

## Important Notes
- Always review and agree to the Terms and Conditions for each dataset you intend to download.

# Test

Perform a small test retrieve of precipitation_m15 data:

```
import terrakio_api
from terrakio_api import Client
from shapely.geometry import Point
# 1. Initialize the client
client = Client()  # This will read from $HOME/.tkio_config.json, which will get the your api key, the default url for the server is https://api.terrak.io
# 2. Create a geographic feature (point)
point = Point(149.057, -35.1548)
geojson ={
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
# 3. Make a WCS request
dataset = client.wcs(
     expr="prec=MSWX.precipitation@(year=2024, month=1)\nprec",
     feature=geojson,
     output="netcdf"  # Specify output format (csv, netcdf, etc.)
     )
# 4. Work with the resulting xarray dataset
print(dataset)

# If you want to change the key, you could either pass the new key to the Client function like client = Client( key = NEW_KEY ) or just go into the $HOME/.tkio_config.json file and change it manually.
# If you want to change the url, you could just pass the new url to the Client function like client = Client( url = NEW_URL )
```


# License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

In applying this licence, ECMWF does not waive the privileges and immunities granted to it by virtue of its status as an intergovernmental organisation nor does it submit to any jurisdiction.