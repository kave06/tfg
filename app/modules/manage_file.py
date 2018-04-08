import os



def write_file(file, body):
    if os.access(file, os.R_OK):
        with open(file, 'w') as fp:
            return fp.write(body)
    return 'no file'

