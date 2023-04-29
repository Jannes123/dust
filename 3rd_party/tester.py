import requests
import xml.etree.ElementTree as ET
from requests import Request, Session, post

jurl = "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/434f2194-d6f6-11ed-a93b-6dd2c6f6a995/"
jurl2 = "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/b0973f38-d6fc-11ed-a93b-6dd2c6f6a995/"


s = Session()
headers = {'content-type': 'text/xml'}

request = Request('GET', jurl, headers=headers)
request2 = Request('GET', jurl2, headers=headers)
print(request)
print(request2)
print(s.cookies)

# prepped_request = s.prepare(request)
# prepped_request2 = s.prepare(request2)
# print(prepped_request)
# print(prepped_request2)

response = s.get(jurl, headers=headers)
response2 = s.get(jurl2, headers=headers)
print(response)
print(response2)

root = ET.fromstring(response.text)
root2 = ET.fromstring(response2.text)
print(root)
print(root2)

nr = root.find(".//user_number").text
nr2 = root.find(".//user_number").text
print(nr)
print(nr2)

print(s.cookies)


url_mob = [
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/434f2194-d6f6-11ed-a93b-6dd2c6f6a995/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/c9814c8e-d781-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/ccd685fe-d7ca-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/1bfc88e2-d837-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/051fc7f2-d863-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/69645524-d88c-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/434f2194-d6f6-11ed-a93b-6dd2c6f6a995/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/c9814c8e-d781-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/ccd685fe-d7ca-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/1bfc88e2-d837-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/051fc7f2-d863-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/69645524-d88c-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/434f2194-d6f6-11ed-a93b-6dd2c6f6a995/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/c9814c8e-d781-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/ccd685fe-d7ca-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/1bfc88e2-d837-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/051fc7f2-d863-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/69645524-d88c-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/434f2194-d6f6-11ed-a93b-6dd2c6f6a995/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/c9814c8e-d781-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/ccd685fe-d7ca-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/1bfc88e2-d837-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/051fc7f2-d863-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/69645524-d88c-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/434f2194-d6f6-11ed-a93b-6dd2c6f6a995/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/c9814c8e-d781-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/ccd685fe-d7ca-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/1bfc88e2-d837-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/051fc7f2-d863-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/69645524-d88c-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/434f2194-d6f6-11ed-a93b-6dd2c6f6a995/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/c9814c8e-d781-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/ccd685fe-d7ca-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/1bfc88e2-d837-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/051fc7f2-d863-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/69645524-d88c-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/434f2194-d6f6-11ed-a93b-6dd2c6f6a995/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/c9814c8e-d781-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/ccd685fe-d7ca-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/1bfc88e2-d837-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/051fc7f2-d863-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/69645524-d88c-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/434f2194-d6f6-11ed-a93b-6dd2c6f6a995/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/c9814c8e-d781-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/ccd685fe-d7ca-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/1bfc88e2-d837-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/051fc7f2-d863-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/69645524-d88c-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/434f2194-d6f6-11ed-a93b-6dd2c6f6a995/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/c9814c8e-d781-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/ccd685fe-d7ca-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/1bfc88e2-d837-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/051fc7f2-d863-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/69645524-d88c-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/434f2194-d6f6-11ed-a93b-6dd2c6f6a995/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/c9814c8e-d781-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/ccd685fe-d7ca-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/1bfc88e2-d837-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/051fc7f2-d863-11ed-992e-274483c0b938/",
    "https://www.pleasetopmeup.com/ussdincoming/routa/xmlapi/69645524-d88c-11ed-992e-274483c0b938/",
]


def process_unit(session, url, headers):
    """process one url at a time using same session"""
    print(session.cookies)
    try:
        x = session.get(url, headers=headers)
    except ConnectionError as c_err:
        print(c_err)
    except BlockingIOError as bl_err:
        print(bl_err)
    return x.text


for inc in url_mob:
    dt = process_unit(s, inc, headers=headers)
    print(dt)

s.close()