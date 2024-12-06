import requests
import json
import time
#/dev/ttyUSB0
url = "http://192.168.20.245:5000/api/gps"
points = [
    [-3.99659499731008, -79.20530077631336],
    [-3.9968400732366396, -79.20527220964115],
    [-3.997219580798013, -79.2052440294276],
    [-3.99756394861836, -79.20520175910731],
    [-3.99799094222539, -79.20514558877136],
    [-3.9983154233598905, -79.20510251219892],
    [-3.9986491708526364, -79.2051156235549],
    [-3.9988957209995974, -79.20506954440651],
    [-3.9992592778601797, -79.20504441032368],
    [-3.9995805203014942, -79.20498746300784]
]

headers = {
  'Content-Type': 'application/json'
}
for i in points:
    payload = json.dumps({
    "lat": i[0],
    "lon": i[1]
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    time.sleep(5)
    print(response.text)
payload = json.dumps({
    "lat": points[0][0],
    "lon": points[0][1]
    })
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)


