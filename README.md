A URL shortener based on Redis NoSql database and made using Flask Python micro web-framework.

# Create virtualenv 
python3 -m venv my_env

# Activate virtualenv
source my_env/bin/activate 

# Install dependencies
pip3 install -r requirements.txt
sudo apt install redis-tools
sudo apt install redis-server

# To Run API
sh dev.sh

# API will be running @ http://localhost:5000


Example of Req and res can be found in Postman directory.
 
POST http://My_IP:5000/shortenUrl

Request:
Content-Type: application/json
{"url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4321165/"}

Response:
{
    "code": "KEbLe",
    "shorturl": "http://192.168.13.40:5000/KEbLe",
    "success": true,
    "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4321165/"
}

Request:
Content-Type: application/json
{"url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4321165/"}

Response:
{
    "code": "KEbLe",
    "message": "URL is repeated",
    "shorturl": "http://192.168.13.40:5000/KEbLe",
    "success": true,
    "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4321165/"
}


POST http://My_IP:5000/KEbLe


To run: 

```
docker-compose up --build
```

