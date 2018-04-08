import os



def write_file(file, body):
    if os.access(file, os.R_OK):
        with open(file, 'a') as fp:
            return fp.write(body+'\n')
    return 'no file'

