import os, shutil


def upload_files():

    venv_name = "venv"
    setup_cmd = "python setup.py sdist"
    twine_cmd = '{VENV}\Scripts\python {VENV}\Lib\site-packages\{TWINE} upload dist/* -u {USER} -p {PSW}'.format(

        VENV=venv_name,
        TWINE="twine",
        USER="__token__",
        PSW=__read_token()

    )

    base_dir = os.path.dirname(os.path.dirname(__file__))
    os.chdir(base_dir)
    os.system(setup_cmd)
    os.system(twine_cmd)

    shutil.rmtree(os.path.join(base_dir, "dist"))

    for dir in os.listdir(base_dir):

        if ".egg-info" in dir:

            shutil.rmtree(os.path.join(base_dir, dir))

def __read_token():

    with open("pipy_token", "r") as file:
        pypi_token = file.readline().strip("\n")

    return pypi_token


if __name__ == "__main__":

    upload_files()
