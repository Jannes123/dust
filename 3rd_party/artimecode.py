
# Fetching Balance
import requests
import xml.etree.ElementTree as ET
import json

url = "https://ws.freepaid.co.za/airtimeplus/"
headers = {'content-type': 'text/xml'}
body = f"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:air="https://ws.freepaid.co.za/airtimeplus/">
   <soapenv:Header/>
   <soapenv:Body>
      <air:fetchBalance>
         <request>
            <user>{'5883139'}</user>
            <pass>{'Free123'}</pass>
         </request>
      </air:fetchBalance>
   </soapenv:Body>
</soapenv:Envelope>
"""

response = requests.post(url,data=body,headers=headers)
root = ET.fromstring(response.text)

balance = root.find(".//balance").text

# response_is = print("Respone",response.text)
data = {"balance": balance}

json_data = json.dumps(data)

print(json_data)


# end in fetching balance


#Buying Airtime
url = "https://ws.freepaid.co.za/airtimeplus/"
headers = {'content-type': 'text/xml'}
body = f"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:air="https://ws.freepaid.co.za/airtimeplus/">
   <soapenv:Header/>
   <soapenv:Body>
      <air:placeOrder>
         <request>
            <user>{'5883139'}</user>
            <pass>{'Free123'}</pass>
            <refno>{'5883139'}</refno>
            <network>{'p-vodacom'}</network>
            <sellvalue>{'2'}</sellvalue>
            <count>{'1'}</count>
            <extra>{'0711579435'}</extra>
         </request>
      </air:placeOrder>
   </soapenv:Body>
</soapenv:Envelope>
"""

response = requests.post(url,data=body,headers=headers)
root = ET.fromstring(response.text)

order_nr = root.find(".//orderno").text
data = {"orderno": order_nr}

json_data = json.dumps(data)

print(json_data)

order_number = data['orderno']






# checking Bought Airtime
url = "https://ws.freepaid.co.za/airtimeplus/"
headers = {'content-type': 'text/xml'}
body = f"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:air="https://ws.freepaid.co.za/airtimeplus/">
   <soapenv:Header/>
   <soapenv:Body>
      <air:fetchOrder>
         <request>
            <user>{'5883139'}</user>
            <pass>{'Free123'}</pass>
            <orderno>{order_number}</orderno>
         </request>
      </air:fetchOrder>
   </soapenv:Body>
</soapenv:Envelope>
"""

response = requests.post(url,data=body,headers=headers)
root = ET.fromstring(response.text)

# print(response.text)
order_status = root.find(".//status").text
data = {"status": order_status}

json_data = json.dumps(data)

print(json_data)



# checking Bought Airtime
url = "https://ws.freepaid.co.za/airtimeplus/"
headers = {'content-type': 'text/xml'}
body = f"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:air="https://ws.freepaid.co.za/airtimeplus/">
   <soapenv:Header/>
   <soapenv:Body>
      <air:queryOrder>
         <request>
            <user>{'5883139'}</user>
            <pass>{'Free123'}</pass>
            <orderno>{order_number}</orderno>
         </request>
      </air:queryOrder>
   </soapenv:Body>
</soapenv:Envelope>
"""

response = requests.post(url,data=body,headers=headers)
root = ET.fromstring(response.text)

# print(response.text)
error_code = root.find(".//errorcode").text
data = {"error_code": error_code}

json_data = json.dumps(data)

print(json_data)


url = "https://ws.freepaid.co.za/airtimeplus/"
headers = {'content-type': 'text/xml'}
body = f"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:air="https://ws.freepaid.co.za/airtimeplus/">
   <soapenv:Header/>
   <soapenv:Body>
      <air:fetchBalance>
         <request>
            <user>{'5883139'}</user>
            <pass>{'Free123'}</pass>
         </request>
      </air:fetchBalance>
   </soapenv:Body>
</soapenv:Envelope>
"""

response = requests.post(url,data=body,headers=headers)
root = ET.fromstring(response.text)

balance = root.find(".//balance").text

# response_is = print("Respone",response.text)
data = {"balance": balance}

json_data = json.dumps(data)

print(json_data)


#end in fetching balance
