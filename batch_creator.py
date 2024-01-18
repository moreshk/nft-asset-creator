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
        
# Loop to generate 5 characters
for i in range(5):
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
        'None', 'Hat', 'Hood', 'Headband', 'Coif',
        'Headdress', 'Crown/Tiara', 'Wizard Hat', 'Horned Helmet'
    ]
    jewelery_options = ['None', 'Necklace', 'Earrings']
    tattoos_markings = ['None', 'Tattoos', 'Facial Scars']

    # Define eye colors and skin colors
    eye_colours = ['Brown', 'Blue', 'Green', 'Hazel', 'Grey', 'Amber', 'Violet']
    skin_colours = [
        'Fair', 'Beige', 'Olive', 'Tan', 'Brown', 'Ebony',
        'Pale Blue', 'Red', 'Purple', 'Gold', 'Silver'
    ]
    # Additional attribute for pfp_traits
    image_backgrounds = [
        'Woods', 'Mountains', 'Volcanic', 'Ruins', 'Arctic', 'Coastal', 'Desert'
    ]

    # Randomly select one option from each new attribute list for pfp_traits
    character_hair_colour = random.choice(hair_colours)
    character_clothing = random.choice(clothing_options)
    character_headpiece = random.choice(headpieces)
    character_jewelery = random.choice(jewelery_options)
    character_tattoos_markings = random.choice(tattoos_markings)
    # Randomly select one option from each new attribute list for pfp_traits
    character_eye_colour = random.choice(eye_colours)
    character_skin_colour = random.choice(skin_colours)
    character_image_background = random.choice(image_backgrounds)

    # Add the new attributes to the pfp_traits
    character_json['pfp_traits']['Hair Colour'] = character_hair_colour
    character_json['pfp_traits']['Clothing'] = character_clothing
    character_json['pfp_traits']['Headpiece'] = character_headpiece
    character_json['pfp_traits']['Jewelery'] = character_jewelery
    character_json['pfp_traits']['Tattoos/Markings'] = character_tattoos_markings
    # Add the new attributes to the pfp_traits
    character_json['pfp_traits']['Eye Colour'] = character_eye_colour
    character_json['pfp_traits']['Skin Colour'] = character_skin_colour
    character_json['pfp_traits']['Image Background'] = character_image_background

    # Scenario API credentials and setup
    api_key = 'api_MZwE8QRKRHyvL5SOPYItew'
    api_secret = 'fc2702db015bf48de9971a8c0f08cfda'
    # model_id = 'WMFVfL6ASISizG1T7X2NNw'
    model_id = 'pixel-blender'

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
            f"facial expression:  {character_traits['Alignment'].lower()}, " \
            f"close up portrait, " \
            f"{pfp_traits['Hair Colour'].lower()} hair, {pfp_traits['Eye Colour'].lower()} eyes, " \
            f"{pfp_traits['Skin Colour'].lower()} skin, wearing {pfp_traits['Clothing'].lower()} and " \
            f"wearing a {pfp_traits['Headpiece'].lower()} on the head, with {pfp_traits['Jewelery'].lower()} jewelery." \
            f"Facial markings : {pfp_traits['Tattoos/Markings'].lower()}, character profession: {character_traits['Background'].lower()} , " \
            f"in front of a {pfp_traits['Image Background'].lower()} background, " \
            

    print("Prompt",prompt)

    # Update the payload with the new prompt
    payload = {
        'parameters': {
            'type': 'txt2img',
            'prompt': prompt,
            'numSamples': 1,
            'numInferenceSteps': 50
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



    # Download the image from Scenario API
    image_filename = f'{i}.png'
    local_image_path = download_image(image_url, f'assets/{image_filename}')  # Save to assets folder with a unique name
    if local_image_path:
        print(f"Image downloaded to: {local_image_path}")

        # Add the local image path to the character JSON
        character_json['Image'] = local_image_path

    # Reformat the character_json to the desired output structure
    formatted_json = {
        "name": character_json.get('Name', ''),
        "symbol": "CHRONICLE",
        "image": image_filename,  # Use the unique image filename
        "description": character_json.get('Lore', ''),
        "attributes": [
            {"trait_type": key, "value": value}
            for key, value in {**character_json['character_traits'], **character_json['pfp_traits']}.items()
            # if key != 'Image Background'  # Exclude 'Image Background' from attributes
        ],
        "properties": {
            "files": [
                {
                    "uri": image_filename,
                    "type": "image/png"
                }
            ]
        }
    }

    # Save the formatted JSON to a file with a unique name
    json_filename = f'{i}.json'
    with open(f'assets/{json_filename}', 'w') as json_file:
        json.dump(formatted_json, json_file, indent=4)

    print(f"JSON saved to: assets/{json_filename}")