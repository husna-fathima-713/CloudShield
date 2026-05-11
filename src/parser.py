def read_log_file(filepath):

    with open(filepath, "r") as file:
        lines = file.readlines()

    return [line.strip() for line in lines]