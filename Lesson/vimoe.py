import json
import os

import requests
from requests_toolbelt import MultipartEncoder

api_secret_key = "Sa4o3GvlmOVUPCr8Oh9ERZ7C517y2MLxCAZROVrEOLu5eiz9NntLjMMJ2rSSaFoK"

url = "https://dev.vdocipher.com/api/videos"

headers = {
    'Authorization': "Apisecret " + api_secret_key
}


def getOtp(videoId):
    video_url = url + "/"+videoId + "/otp"
    response = requests.request("POST", video_url, headers=headers)
    print(response.json())

def upload(filename, title):
    querystring = {"title": title}

    response = requests.request("PUT", url, headers=headers, params=querystring)

    ############# STEP 2 ####################

    uploadInfo = response.json()
    print(uploadInfo)
    clientPayload = uploadInfo['clientPayload']
    uploadLink = clientPayload['uploadLink']

    m = MultipartEncoder(fields=[
        ('x-amz-credential', clientPayload['x-amz-credential']),
        ('x-amz-algorithm', clientPayload['x-amz-algorithm']),
        ('x-amz-date', clientPayload['x-amz-date']),
        ('x-amz-signature', clientPayload['x-amz-signature']),
        ('key', clientPayload['key']),
        ('policy', clientPayload['policy']),
        ('success_action_status', '201'),
        ('success_action_redirect', ''),
        ('file', ('filename', open(filename, 'rb'), 'text/plain'))
    ])

    response = requests.post(
        uploadLink,
        data=m,
        headers={'Content-Type': m.content_type}
    )

    response.raise_for_status()
    return uploadInfo["videoId"]
