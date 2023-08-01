from core.core.utils.collections import deep_update
from core.core.utils.settings import get_settings_from_environment

"""
This takes env variables with a matching prefix, strips out the prefix, and adds it to global

For example:
- export CORESETTING_IN_DOCKER=true (environment variable)

Could then be referenced as a global as:
IN_DOCKER (where the value would be true)
"""

# globals() is a dict of global variables

deep_update(globals(), get_settings_from_environment(ENVVAR_SETTINGS_PREFIX))  # type: ignore
