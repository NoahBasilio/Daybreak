import os

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "config.json")

if os.path.exists(config_path):
    pass
else:
    user_city = input("What city do you live in? ")