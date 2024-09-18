import json
import base64
import hashlib
import hmac
import requests
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
from urllib.parse import urlencode  # 确保导入 urlencode
from img import process_user_image

APPId = "您的APPId"  # 控制台获取
APISecret = "您的APISecret"  # 控制台获取
APIKey = "您的APIKey"  # 控制台获取

def sha256base64(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
    return digest

class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg

class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema

def parse_url(request_url):
    stidx = request_url.index("://")
    host = request_url[stidx + 3:]
    schema = request_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("invalid request url:" + request_url)
    path = host[edidx:]
    host = host[:edidx]
    u = Url(host, path, schema)
    return u

def assemble_ws_auth_url(request_url, method="POST", api_key="", api_secret=""):
    u = parse_url(request_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }
    return request_url + "?" + urlencode(values)

def perform_ocr(image_path):
    with open(image_path, "rb") as f:
        imageBytes = f.read()

    url = 'https://api.xf-yun.com/v1/private/sf8e6aca1'
    body = {
        "header": {
            "app_id": APPId,
            "status": 3
        },
        "parameter": {
            "sf8e6aca1": {
                "category": "ch_en_public_cloud",
                "result": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json"
                }
            }
        },
        "payload": {
            "sf8e6aca1_data_1": {
                "encoding": "jpg",
                "image": str(base64.b64encode(imageBytes), 'UTF-8'),
                "status": 3
            }
        }
    }

    request_url = assemble_ws_auth_url(url, "POST", APIKey, APISecret)
    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': APPId}
    response = requests.post(request_url, data=json.dumps(body), headers=headers)
    response_content = response.content.decode()

    tempResult = json.loads(response_content)
    finalResult = base64.b64decode(tempResult['payload']['result']['text']).decode()
    finalResult = finalResult.replace(" ", "").replace("\n", "").replace("\t", "").strip()

    data = json.loads(finalResult)
    text_content = ""

    for page in data.get("pages", []):
        for line in page.get("lines", []):
            for word in line.get("words", []):
                text_content += word.get("content", "")

    return text_content

def main():
    image_url = input("请输入验证码图片的链接: ")
    processed_image_path = process_user_image(image_url)
    if processed_image_path:
        text_content = perform_ocr(processed_image_path)
        print("识别为：=>" + text_content)
    else:
        print("图像处理失败。")

if __name__ == "__main__":
    main()
