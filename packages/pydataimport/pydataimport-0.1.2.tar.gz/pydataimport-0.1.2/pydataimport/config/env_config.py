# from dotenv import load_dotenv
# import os

# # Load the .env file
# load_dotenv()

# # Read the environment variables
# database_url = os.getenv("DATABASE_URL")
# api_key = os.getenv("API_KEY")

# Read all the properties from the .env file
env_properties = {}
with open('.env', 'r') as file:
    for line in file:
        if line.strip().startswith('#'):
            continue
        if '=' in line:
            key, value = line.strip().split('=', 1)
            env_properties[key] = value

# Initialize the object with the environment properties
env_object = type('EnvConfig', (), env_properties)