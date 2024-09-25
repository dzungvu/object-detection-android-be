import os

def runtest():
    print('run test')

class FileUtils:
    def __init__(self) -> None:
        print('This is initial from FileUtils')

    DEBUG_FOLDER = 'debug'
    LOG_FILE_FOLDER = "log_file"

    @staticmethod
    def is_folder_exist(path):
        return os.path.exists(path)

    @staticmethod
    def create_folder_if_not_exist(folder_path):
        if not FileUtils.is_folder_exist(path=folder_path):
            os.makedirs(folder_path)
            print(f'Folder {folder_path} created.')
        else:
            print(f'Folder {folder_path} already existed.')

    @staticmethod
    def write_debug_file(file_name, content):
        debug_log_file_path = os.path.join(FileUtils.DEBUG_FOLDER, FileUtils.LOG_FILE_FOLDER)
        FileUtils.create_folder_if_not_exist(debug_log_file_path)
        raw_data_file = os.path.join(debug_log_file_path, file_name)
        with open(raw_data_file, 'w', encoding='utf-8') as file:
            file.write(content)
            file.close()

    @staticmethod
    def get_ggm_folder():
        return os.path.join(FileUtils.SHOP_DATA_FOLDER, FileUtils.GGM_FOLDER)

    @staticmethod
    def get_ggm_data_file(keyword):
        data_folder = os.path.join(FileUtils.SHOP_DATA_FOLDER, FileUtils.GGM_FOLDER)
        data_file = os.path.join(data_folder, f'{keyword}.csv')

        file_suffix = 0
        while True:
            if FileUtils.is_folder_exist(path=data_file):
                file_suffix = file_suffix + 1
                data_file = os.path.join(data_folder, f'{keyword}_{file_suffix}.csv')
            else: 
                break
        return data_file

    @staticmethod
    def create_ggm_data_folder():
        FileUtils.create_folder_if_not_exist(FileUtils.get_ggm_folder())