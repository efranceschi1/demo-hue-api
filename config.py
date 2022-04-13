import os
import yaml
import cm_client
from os.path import expanduser


class Config:
    def __init__(self):
        config_dir = expanduser("~/.hue")

        if not os.path.isdir(config_dir):
            os.mkdir(config_dir)

        config_file = f"{config_dir}/config.yaml"
        if not os.path.isfile(config_file):
            print(f"Config file not found: {config_file}")
            cm_template_file = "config_template.yaml"
            with open(cm_template_file, "r") as src:
                with open(config_file, "w") as dst:
                    print(f"Creating config file from template: {cm_template_file}")
                    dst.write(src.read())
                    print(f"Created the new config file: {config_file}")
                    print("Please, edit this file and try again")
                    exit(1)

        with open(config_file, "r") as config_stream:
            try:
                self.config = yaml.safe_load(config_stream)
            except yaml.YAMLError as err:
                print(err)

        cfg = self.config['hue']['configuration']
        self.username = cfg['username']
        self.password = cfg['password']
        self.api_url = cfg['api_url']

