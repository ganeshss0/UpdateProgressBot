import os
from github import Github
import subprocess


ACCESS_TOKEN = 'ACCESS_TOKEN'
USERNAME = 'ganeshss0'
REPOSITORY = 'my_data'
CSV_FILE = 'GoodDay.csv'
IMG_FILE = 'progress.png'
SHA_FILE = 'git_sha.json'


def update():
    run_script('visualization.py')
    
    g = Github(ACCESS_TOKEN)
    user = g.get_user(USERNAME)
    repo = user.get_repo(REPOSITORY)

    csv_path = os.path.join(REPOSITORY, CSV_FILE)
    img_path = os.path.join(REPOSITORY, IMG_FILE)

    with open(csv_path, 'r') as file:
        csv_content = file.read()
    with open(img_path, 'rb')as file:
        img_content = file.read()

    sha_csv = repo.get_contents(CSV_FILE).sha
    sha_img = repo.get_contents(IMG_FILE).sha

    try:
        csv_commit = repo.update_file(
            path=CSV_FILE,
            message='Update Progress',
            content=csv_content,
            branch='main',
            sha=sha_csv
        )

        img_commit = repo.update_file(
            path = IMG_FILE,
            message='Update Progress',
            content=img_content,
            branch='main',
            sha=sha_img
        )

        print('Pushed Changes to Github Successfully')


    except Exception as e:
        print(f'Error occured: {str(e)}')


def run_script(module_name:str):
    current_dir = os.getcwd()
    os.chdir(REPOSITORY)
    subprocess.run(["python", module_name])
    os.chdir(current_dir)