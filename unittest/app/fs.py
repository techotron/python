from subprocess import check_output

def print_contents_of_cwd():
    contents = check_output(['ls']).split()
    return contents
