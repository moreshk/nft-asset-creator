import requests
import base64
import time
import os

# Scenario API credentials and setup
api_key = 'api_MZwE8QRKRHyvL5SOPYItew'
api_secret = 'fc2702db015bf48de9971a8c0f08cfda'
model_id = 'WMFVfL6ASISizG1T7X2NNw'

# Encode the API key and secret
encoded_credentials = base64.b64encode(f'{api_key}:{api_secret}'.encode('utf-8')).decode('utf-8')

# Scenario API endpoints
post_url = f'https://api.cloud.scenario.com/v1/models/{model_id}/inferences'
headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'Authorization': f'Basic {encoded_credentials}'
}

# Payload for the Scenario API request
payload = {
    'parameters': {
        'type': 'txt2img',
        'prompt': 'dungeons and dragons female elf character',
        'numSamples': 1  # Set the number of images to generate to 1
    }
}

# Make the initial request to start the inference
response = requests.post(post_url, json=payload, headers=headers)
inference_id = response.json()['inference']['id']

# Poll the API until the inference is complete
get_url = f'https://api.cloud.scenario.com/v1/models/{model_id}/inferences/{inference_id}'
while True:
    response = requests.get(get_url, headers=headers)
    inference_data = response.json()['inference']

    if inference_data['status'] == 'succeeded':
        # Inference is complete, extract the URL of the image
        image_url = inference_data['images'][0]['url']
        break
    elif inference_data['status'] == 'failed':
        # Inference failed, handle accordingly
        print("Inference failed.")
        exit()
    else:
        # Inference is still running, wait before polling again
        time.sleep(5)

# Function to download the image
def download_image(image_url, local_file_path, retries=3, delay=5):
    for attempt in range(retries):
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(local_file_path, 'wb') as file:
                file.write(response.content)
            return local_file_path
        elif response.status_code == 504 and attempt < retries - 1:
            print(f"Attempt {attempt + 1} failed with status code 504. Retrying after {delay} seconds...")
            time.sleep(delay)
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            local_file_path = None
            return local_file_path

# Usage
# local_image_path = download_image(image_url, 'local_image.png')

# Function to upload the image to Pinata
def upload_to_pinata(local_file_path, jwt):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "Authorization": f"Bearer {jwt}"
    }
    with open(local_file_path, 'rb') as file:
        files = {
            'file': file
        }
        response = requests.post(url, files=files, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to upload to Pinata. Status code: {response.status_code}")
        return None

# JWT for Pinata
# jwt = 'your_jwt_token_here'  # Replace with your actual JWT token
jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJiYWJiNGU3OC04ZmY1LTQyZGUtYmI4Mi0xZjdmMTQ4ZWFiYmIiLCJlbWFpbCI6Im1vcmVzaEBrb3JldGV4LmFpIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJGUkExIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9LHsiaWQiOiJOWUMxIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6ImU2ZmM3NmIwNzFmYzcwM2Q1NWI2Iiwic2NvcGVkS2V5U2VjcmV0IjoiMDk1MjUxMjYwMDRkMTA4OTg1ZGM2ZDBmMTVkZTJmZDY2YWQ0NDM3MWU1OWNlZjliZWI3MWU3MzFjZGNlMDhlOCIsImlhdCI6MTcwNTQ3NTExM30.KXx31l8frVOCgdBwSvzNBN728p8yg-ZiSFNUrpMwUdw'

# Download the image from Scenario API
local_image_path = download_image(image_url, 'local_image.png')
if local_image_path:
    # Upload the image to Pinata
    pinata_response = upload_to_pinata(local_image_path, jwt)
    if pinata_response:
        # Get the IPFS hash and construct the URL
        ipfs_hash = pinata_response['IpfsHash']
        pinata_url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
        print(f"Image uploaded to Pinata: {pinata_url}")
        # Optionally, remove the local file after upload
        os.remove(local_image_path)