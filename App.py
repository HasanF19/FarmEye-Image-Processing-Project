import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import requests
from datetime import datetime, timedelta


client_id = 'You need to enter your client id'
client_secret = 'You need to enter your client secret'

# OAuth2 Client
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

#Get token from sentinel hub
token = oauth.fetch_token(
    token_url='https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token',
    client_secret=client_secret,
    include_client_id=True
)

# API Headers
access_token = token['access_token']
headers = {
    "Authorization": f"Bearer {access_token}"
}

# file name
output_folder = "Yunanistan_Canlı_Test"

# Create folder
os.makedirs(output_folder, exist_ok=True)

# Get image function
def download_image(bounds, date_range, evalscript, index):
    url = "https://services.sentinel-hub.com/api/v1/process"
    
    payload = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "bbox": bounds
            },
            "data": [
                {
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {
                            "from": date_range[0],
                            "to": date_range[1]
                        }
                    }
                }
            ]
        },
        "output": {
            "width": 512,
            "height": 512
        }
    }
    
    form_data = {
        "request": (None, json.dumps(payload)),
        "evalscript": (None, evalscript)
    }
    
    response = requests.post(url, headers=headers, files=form_data)
    
    if response.status_code == 200:
        # Convert date range to file name
        date_range_str = f"{date_range[0].replace(':', '').replace('-', '').replace('T', '_')}_{date_range[1].replace(':', '').replace('-', '').replace('T', '_')}"
        
        # Create file path
        file_path = os.path.join(output_folder, f"sentinel_image_{date_range_str}.png")
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved successfully: {file_path}")
    else:
        print(f"Hata (Görüntü Çekme): {response.text}")


# Check cloud coverage function
def get_cloud_coverage(bounds, date_range):
    catalog_url = "https://services.sentinel-hub.com/api/v1/catalog/search"
    catalog_payload = {
        "bbox": bounds,
        "datetime": f"{date_range[0]}/{date_range[1]}",
        "collections": ["sentinel-2-l2a"],
        "limit": 1  # Check only the nearest image
    }

    catalog_response = requests.post(catalog_url, headers=headers, json=catalog_payload)
    if catalog_response.status_code == 200:
        catalog_data = catalog_response.json()
        features = catalog_data.get("features", [])
        if features:
            cloud_coverage = features[0].get("properties", {}).get("eo:cloud_cover", 100)  # Get cloud coverage
            return cloud_coverage
    return None  # If image not found

# Set date range and bbox
start_date = datetime(2024,1, 1)  # Start date
end_date = datetime(2024, 12, 30)  # End date
bbox = [23.88033,
        38.24560, 
        23.97268, 
        38.18506] 

# Evalscript
evalscript = """
let index = (1-((B06*B07*B8A)/B04)**0.5)*((B12-B8A)/((B12+B8A)**0.5)+1);
let min = 0;
let max = 0.99;
let zero = 0.5;

let underflow_color = [1, 1, 1];
let low_color = [0/255, 0/255, 255/255];
let high_color = [255/255, 20/255, 20/255];
let zero_color = [250/255, 255/255, 10/255];
let overflow_color = [255/255, 0/255, 255/255];

return colorBlend(index, [min, min, zero, max],
[
	underflow_color,
	low_color,
	zero_color,
	high_color,
	overflow_color
]);
"""

# Get data with 5 days steps
current_date = start_date
index = 1

while current_date <= end_date:
    # 5 days steps
    next_date = current_date + timedelta(days=5)
    date_range = [
        current_date.strftime("%Y-%m-%dT00:00:00Z"),
        next_date.strftime("%Y-%m-%dT00:00:00Z")
    ]
    
    print(f"Kontrol ediliyor: {date_range[0]} - {date_range[1]}")
    
    # Check cloud coverage
    cloud_coverage = get_cloud_coverage(bbox, date_range)
    
    if cloud_coverage is not None and cloud_coverage <= 10:  
        print(f"Bulut oranı uygun (%{cloud_coverage}). Görüntü indiriliyor...")
        download_image(bbox, date_range, evalscript, index)
        index += 1
    elif cloud_coverage is not None:
        print(f"Bulut oranı yüksek (%{cloud_coverage}). Görüntü indirilmiyor.")
    else:
        print("Image not found.")
    
    # Next step
    current_date = next_date
