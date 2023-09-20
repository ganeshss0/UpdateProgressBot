import os
from github import Github
import json


ACCESS_TOKEN = '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'
USERNAME = 'ganeshss0'
REPOSITORY = 'my_data'
CSV_FILE = 'GoodDay.csv'
IMG_FILE = 'progress.png'
SHA_FILE = 'git_sha.json'


def update():
    
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
