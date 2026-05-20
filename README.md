import os
import yaml

# Get the project root dynamically (works from anywhere)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define config path
CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config', 'config.yaml')

print("Project Root :", PROJECT_ROOT)
print("Looking for config at:", CONFIG_PATH)

# Load the yaml file
with open(CONFIG_PATH, 'r') as file:
    config = yaml.safe_load(file)

# Example: db_path
db_path = config.get('db_path')   # or whatever key you have

print("✅ Config loaded successfully!")