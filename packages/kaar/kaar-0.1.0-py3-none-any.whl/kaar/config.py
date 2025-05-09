import yaml
import os

def load_config(config_path):
    """Load configuration from a YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Validate required fields
    required_fields = {
        'aws': ['region', 'sns_topic_arn', 'log_group', 'log_stream'],
        'bedrock': ['model', 'temperature', 'max_tokens'],
        'k8sgpt': ['backend', 'explain'],
        'remediation': ['max_attempts', 'retry_interval_seconds']
    }
    
    for section, fields in required_fields.items():
        if section not in config:
            raise ValueError(f"Missing section '{section}' in config.yaml")
        for field in fields:
            if field not in config[section]:
                raise ValueError(f"Missing field '{field}' in section '{section}' of config.yaml")
    
    return config
