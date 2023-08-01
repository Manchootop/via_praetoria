import yaml


def yaml_coerce(value):
    # Convert value to proper Python
    # Convert stringed dict to Python dict
    # Useful for Dockerfiles
    if isinstance(value, str):
        return yaml.load(f'dummy: {value}', Loader=yaml.SafeLoader)['dummy']
