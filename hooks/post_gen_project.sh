#!/bin/sh
pip install -r requirements.txt

echo "Export DataPlatform Token"
export PATH="Basic MG9hNjEwaHRqN25kSldpMkszNTc6U3lIa2FEejQ4WGIySFVyd1lURTBvb0NLVlJ5ZmVlZnViRExlZzctRw=="
echo "Export DataPlatform Token done!"
echo "Export Zoura SAND BOX Client ID"
export ZOURA_SAND_BOX='client_id=c49e3886-f9a9-4edd-bed2-704db6257267&grant_type=client_credentials&client_secret=Unm0vTHEsYMBEqudOBm%2BhSG%2BTBf73qeRe%2BG%3D3c'
echo "Export Zoura SAND BOX Client ID done!"
echo "Export local Silk settings set to true"
export SILK='True'
echo "Export local Silk settings set to true done!"

rm bitbucket-pipelines.yml
