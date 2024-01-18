import requests
import base64
import time
import os
import json
import random
from dotenv import load_dotenv
from openai import OpenAI

# Load the environment variables from .env file
load_dotenv()

# Define the species and attributes
species = [
    'Human', 'Elf', 'Dwarf', 'Halfling', 'Dragonborn',
    'Gnome', 'Half-Elf', 'Half-Orc', 'Tiefling'
]

classes = [
    'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter',
    'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer',
    'Warlock', 'Wizard'
]

backgrounds = [
    'Acolyte', 'Charlatan', 'Criminal/Spy', 'Entertainer',
    'Folk Hero', 'Guild Artisan', 'Hermit', 'Noble',
    'Outlander', 'Sage', 'Sailor', 'Pirate', 'Soldier', 'Urchin'
]

alignments = [
    'Lawful Good', 'Neutral Good', 'Chaotic Good',
    'Lawful Neutral', 'True Neutral', 'Chaotic Neutral',
    'Lawful Evil', 'Neutral Evil', 'Chaotic Evil'
]

sexes = ['Male', 'Female']

# Randomly select one species, class, background, alignment, level, and XP bonus
character_species = random.choice(species)
character_class = random.choice(classes)
character_background = random.choice(backgrounds)
character_alignment = random.choice(alignments)
character_level = random.randint(1, 10)  # Level between 1 and 10
character_xp_bonus = random.randint(50, 1000)  # XP Bonus between 50 and 1000
character_sex = random.choice(sexes)

# Bundle attributes under 'character_traits' and 'pfp_traits'
character_traits = {
    'Species': character_species,
    'Class': character_class,
    'Background': character_background,
    'Alignment': character_alignment,
    'Level': character_level,
    'XP Bonus': character_xp_bonus
}

pfp_traits = {
    'Sex': character_sex
}

# Create a character JSON with nested traits
character_json = {
    'character_traits': character_traits,
    'pfp_traits': pfp_traits
}

# Function to generate a character name using OpenAI's API
def generate_character_name(species, character_class):
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        prompt = f"Generate a fantasy name suitable for a {species} {character_class}."

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a creative writer."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=10
        )

        name = response.choices[0].message.content.strip()
        return name

    except Exception as e:
        print(f"Failed to generate name: {str(e)}")
        return None

# Function to generate character lore using OpenAI's API
def generate_character_lore(attributes):
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        prompt = f"Create a dungeons and dragons style backstory for a character with the following attributes: {json.dumps(attributes, indent=4)}. Up to 5 sentences."

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a creative writer."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            temperature=1,
            max_tokens=150
        )

        lore = response.choices[0].message.content.strip()
        return lore

    except Exception as e:
        print(f"Failed to generate lore: {str(e)}")
        return None

# Generate a name for the character
character_name = generate_character_name(character_species, character_class)

# Add the name to the character JSON if it was successfully generated
if character_name:
    character_json['Name'] = character_name

    # Generate the lore for the character with the name included
    character_lore = generate_character_lore(character_json)

    # Add the lore to the character JSON if it was successfully generated
    if character_lore:
              character_json['Lore'] = character_lore

# Additional attributes for pfp_traits
hair_colours = [
    'Black', 'Brown', 'Blonde', 'Red', 'Gray', 'White',
    'Blue', 'Green', 'Purple', 'Pink', 'Orange', 'Silver', 'Gold'
]
clothing_options = [
    'Basic Tunic', 'Cloak/Cape', 'Leather Jacket', 'Leather Armour',
    'Fine Robes', 'Noble Robes', "Mage's Robes", 'Chainmail Armour', 'Plate Armour'
]
headpieces = [
    'None', 'Hat', 'Hood', 'Headband', 'Mask', 'Coif',
    'Headdress', 'Crown/Tiara', 'Open Helm', 'Full Helm', 'Great Helm'
]
jewelery_options = ['None', 'Necklace', 'Earrings']
tattoos_markings = ['None', 'Tattoos', 'Facial Scars']

# Define eye colors and skin colors
eye_colours = ['Brown', 'Blue', 'Green', 'Hazel', 'Grey', 'Amber', 'Violet']
skin_colours = ['Fair', 'Light', 'Medium', 'Tan', 'Dark', 'Ebony', 'Alabaster', 'Blue', 'Gold', 'Pink']


# Randomly select one option from each new attribute list for pfp_traits
character_hair_colour = random.choice(hair_colours)
character_clothing = random.choice(clothing_options)
character_headpiece = random.choice(headpieces)
character_jewelery = random.choice(jewelery_options)
character_tattoos_markings = random.choice(tattoos_markings)
# Randomly select one option from each new attribute list for pfp_traits
character_eye_colour = random.choice(eye_colours)
character_skin_colour = random.choice(skin_colours)


# Add the new attributes to the pfp_traits
character_json['pfp_traits']['Hair Colour'] = character_hair_colour
character_json['pfp_traits']['Clothing'] = character_clothing
character_json['pfp_traits']['Headpiece'] = character_headpiece
character_json['pfp_traits']['Jewelery'] = character_jewelery
character_json['pfp_traits']['Tattoos/Markings'] = character_tattoos_markings
# Add the new attributes to the pfp_traits
character_json['pfp_traits']['Eye Colour'] = character_eye_colour
character_json['pfp_traits']['Skin Colour'] = character_skin_colour


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

# Extract pfp_traits and character_traits from character_json
pfp_traits = character_json['pfp_traits']
character_traits = character_json['character_traits']

# Update the prompt with the new pfp_traits
prompt = f"dungeons and dragons {pfp_traits['Sex'].lower()} {character_traits['Species'].lower()} character, " \
         f"{pfp_traits['Hair Colour'].lower()} hair, {pfp_traits['Eye Colour'].lower()} eyes, " \
         f"{pfp_traits['Skin Colour'].lower()} skin, wearing {pfp_traits['Clothing'].lower()} and " \
         f"{pfp_traits['Headpiece'].lower()}, with {pfp_traits['Jewelery'].lower()} and " \
         f"{pfp_traits['Tattoos/Markings'].lower()}, {character_traits['Background'].lower()} background, " \
         f"portrait front facing, 16 pixel resolution design, game character"

# Update the payload with the new prompt
payload = {
    'parameters': {
        'type': 'txt2img',
        'prompt': prompt,
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

        # Add the image URL to the character JSON
        character_json['Image'] = pinata_url

        # Optionally, remove the local file after upload
        os.remove(local_image_path)

# # After generating the image and uploading to Pinata, add the image URL to the character_json
# if 'pinata_url' in locals():  # Check if the image URL has been set
#     character_json['Image'] = pinata_url

# Print out the character JSON with the new structure
print(json.dumps(character_json, indent=4))