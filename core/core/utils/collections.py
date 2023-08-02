# allows you to insert keys into settings dicts

def deep_update(base_dict, update_with):
    # iterate over each item in the new dict
    for key, value in update_with.items():
        # if the value is a dict
        if isinstance(value, dict):
            base_dict_value = base_dict.get(key)

            # if the original value is also a dict then run it through this same function: recursive func
            if isinstance(base_dict_value, dict):
                deep_update(base_dict_value, value)
            # if the original value is NOT a dict the just set the new value from the new dict to base
            else:
                base_dict[key] = value
        # if the new value is NOT a dict DO THE SAME AS ^^ line 13

        else:
            base_dict[key] = value

    return base_dict
