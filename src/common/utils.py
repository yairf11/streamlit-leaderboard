

def remove_illegal_filename_characters(input_string: str):
    return "".join(x if (x.isalnum() or x in "._- ") else '_' for x in input_string).strip()
