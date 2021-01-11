import http.client
import ssl
import datetime 

ssl._create_default_https_context = ssl._create_unverified_context

conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "720b2beefemsh17802dccb5f8d6dp1efcc4jsn87b74001509d",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

conn.request("GET", "/stock/v3/get-historical-data?symbol=AMRN&region=US", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
