import os

def get_data_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'data', 'users')

def auth_make_dir(user, key):
    if user.is_authenticated:
        user_data_dir = os.path.join(get_data_dir(), key)
        os.mkdir(user_data_dir)
    return 'Successful'


def fetch_dir(keys):
    dirs = []
    for key_folder in os.listdir(get_data_dir()):
        if key_folder in keys:
            dirs.append(key_folder)

        if len(dirs) == len(keys):
            break

    return dirs


def dir_searcher(dirs, arg):
    names = []
    urls = []

    for directory in dirs:
        for file_name in os.listdir(f'{get_data_dir()}/{directory}'):
            names.append(file_name)
            urls.append(f'data/users/{directory}/{file_name}')

    if arg == 0:
        return names
    elif arg == 1:
        return urls


def own_dir_searcher(user, arg):
    owned_names = []
    owned_urls = []

    for file_name in os.listdir(f'{get_data_dir()}/{user.key}'):
        owned_names.append(file_name)
        owned_urls.append(f'data/users/{user.key}/{file_name}')

    if arg == 0:
        return owned_names
    elif arg == 1:
        return owned_urls
