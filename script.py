import os
import time

import send2trash
import re

from PIL import Image, ImageFilter
from pathlib import Path

USERNAME = os.getlogin()
DIRECTORY_NAME = 'Desktop'
FOLDER_NAME = 'ABE'
ORIGINALS_DIRECTORY = 'Originals'
ORIGINALS_DIRECTORY_PATH = f'/Users/{USERNAME}/{DIRECTORY_NAME}/{FOLDER_NAME}/{ORIGINALS_DIRECTORY}'
RENDERS_DIRECTORY = 'Renders'
RENDERS_DIRECTORY_PATH = f'/Users/{USERNAME}/{DIRECTORY_NAME}/{FOLDER_NAME}/{RENDERS_DIRECTORY}'
TEMP_DIRECTORY = 'temp'
TEMP_DIRECTORY_PATH = f'/Users/{USERNAME}/{DIRECTORY_NAME}/{FOLDER_NAME}/{TEMP_DIRECTORY}'
TEMP_ORIGINALS_DIRECTORY = 'temp_originals'
TEMP_ORIGINALS_DIRECTORY_PATH = f'/Users/{USERNAME}/{DIRECTORY_NAME}/{FOLDER_NAME}/{TEMP_DIRECTORY}/{TEMP_ORIGINALS_DIRECTORY}'
WATERMARK_PATH = f'/Users/{USERNAME}/{DIRECTORY_NAME}/{FOLDER_NAME}/watermark.png'

def check_originals_directory():
    if os.path.isdir(ORIGINALS_DIRECTORY_PATH) != True:
        os.mkdir(ORIGINALS_DIRECTORY_PATH)

def check_render_directory():
    if os.path.isdir(RENDERS_DIRECTORY_PATH) != True:
        os.mkdir(RENDERS_DIRECTORY_PATH)

def check_temp_directory():
    if os.path.isdir(TEMP_DIRECTORY_PATH) != True:
        os.mkdir(TEMP_DIRECTORY_PATH)

def check_temp_originals_directory():
    if os.path.isdir(TEMP_ORIGINALS_DIRECTORY_PATH) != True:
        os.mkdir(TEMP_ORIGINALS_DIRECTORY_PATH)

def check_necessary_directory():
    check_originals_directory()
    check_render_directory()
    check_temp_directory()
    check_temp_originals_directory()

def check_watermark():
    if 'watermark.PNG' not in os.listdir(f'/Users/{USERNAME}/{DIRECTORY_NAME}/{FOLDER_NAME}'):
        raise FileNotFoundError(f'Ensure watermark is placed in {FOLDER_NAME} and named "watermark.PNG"')

def originals_format_homogeniser():
    while True:
        for _ in os.listdir(ORIGINALS_DIRECTORY_PATH):
            image_path = Path(ORIGINALS_DIRECTORY_PATH, _)
            modified_image_path = Path(ORIGINALS_DIRECTORY_PATH, _.upper())
            print(image_path)
            if image_path.is_file() and image_path.suffix.upper() in ('.PNG', '.JPG', '.JPEG', '.TIF', '.TIFF'):
                image = Image.open(image_path)
                original_exif = image.info.get('exif')
                if image.mode != 'RGB':
                    modified_image = image.convert('RGB')
                    if original_exif is not None:
                        modified_image.save(image_path, quality = 100, exif = original_exif)
                    if original_exif is None:
                        modified_image.save(image_path, quality = 100)
            os.rename(image_path, modified_image_path)
        return

def copy_entire_originals_directory():
    while True:
        for _ in os.listdir(ORIGINALS_DIRECTORY_PATH):
            original_path = Path(ORIGINALS_DIRECTORY_PATH, _)
            if original_path.suffix in ('.PNG', '.JPG', '.JPEG', '.TIF', '.TIFF'):
                image = Image.open(f'{ORIGINALS_DIRECTORY_PATH}/{_}')
                original_exif = image.info.get('exif')
                if original_exif is not None:
                    image.save(f'{TEMP_ORIGINALS_DIRECTORY_PATH}/{_}', quality = 100, exif = original_exif)
                elif original_exif is None:
                    image.save(f'{TEMP_ORIGINALS_DIRECTORY_PATH}/{_}', quality = 100)
        return

def clear_temp_originals_directory():
    while True:
        for _ in os.listdir(TEMP_ORIGINALS_DIRECTORY_PATH):
            temp_path = Path(TEMP_ORIGINALS_DIRECTORY_PATH, _)
            if temp_path.suffix in ('.PNG', '.JPG', '.JPEG', '.TIF', '.TIFF'):
                send2trash.send2trash(temp_path)
        return

def check_presence_of_user_input_original_to_open():
    while True:
        user_input = input('\nEnter Name of Original: ')
        processed_user_input = user_input.upper()
        for _ in os.listdir(ORIGINALS_DIRECTORY_PATH):
            original_path = Path(ORIGINALS_DIRECTORY_PATH, _)
            if original_path.suffix.upper() in ('.PNG', '.JPG', '.JPEG', '.TIF', '.TIFF'):
                if processed_user_input == original_path.stem.upper():
                    processed_user_input_with_extension = processed_user_input + original_path.suffix.upper()
                    return processed_user_input_with_extension
        else:
            print('\nEnter a Valid File Name')

def get_file_extension(user_input_to_open, directory):
    for _ in os.listdir(directory):
        direcotry_path = Path(directory, _)
        file_extension = direcotry_path.suffix.upper()
        if user_input_to_open == direcotry_path.name.upper():
            if file_extension in ('.PNG', '.JPG', '.JPEG', '.TIF', '.TIFF'):
                return file_extension
            else:
                raise ValueError('Invalid File Extension')

def rename_original_to_temp(original_name):
    original_path = Path(ORIGINALS_DIRECTORY_PATH, original_name)
    if original_path.suffix in ('.PNG', '.JPG', '.JPEG', '.TIF', '.TIFF'):
        original_extension = get_file_extension(original_name, ORIGINALS_DIRECTORY_PATH)
        temp = original_name[:-len(original_extension)] + f'_TEMP{original_extension}'
        print(temp)
    return temp

def rename_temp_to_original(temp_name):
    temp_path = Path(TEMP_DIRECTORY_PATH, temp_name)
    if temp_path.suffix in ('.PNG', '.JPG', '.JPEG', '.TIF', '.TIFF'):
        original_extension = get_file_extension(temp_name, TEMP_DIRECTORY_PATH)
        if str(temp_path).endswith(('_TEMP.PNG', '_TEMP.JPG', '_TEMP.JPEG', '_TEMP.TIF', '_TEMP.TIFF')):
            original = temp_name[:-(len(original_extension)+5)] + f'{original_extension}'
            print(original)
    return original
    
def render_or_delete(image_name):
    while True:
        user_input = input('Render[R] or Delete[D]: ')
        processed_user_input = user_input.upper()
        if processed_user_input == 'D':
            send2trash.send2trash(f'{TEMP_DIRECTORY_PATH}/{image_name}')
            return
        elif processed_user_input == 'R':
            render_name = rename_temp_to_original(image_name)
            temp_directory_path = Path(TEMP_DIRECTORY_PATH, image_name)
            render_directory_path = Path(RENDERS_DIRECTORY_PATH, render_name)
            os.rename(temp_directory_path, render_directory_path)
            return
        else:
            print('Enter R or D')

def print_all_original():
    for _ in sorted(os.listdir(TEMP_ORIGINALS_DIRECTORY_PATH)):
        original_path = Path(TEMP_ORIGINALS_DIRECTORY_PATH, _)
        if original_path.suffix in ('.PNG', '.JPG', '.JPEG', '.TIF', '.TIFF'):
            print(_)
    return

def user_input_delete_view_original(temp_name):
    while True:
        user_input = input('Done with Preview? [Y]: ')
        processed_user_input = user_input.upper()
        if processed_user_input == 'Y':
            send2trash.send2trash(f'{TEMP_ORIGINALS_DIRECTORY_PATH}/{temp_name}')
            return
        else:
            print('Enter Valid Option')

def view_user_input_original(user_input_original_to_open):
    selected_original = Image.open(f'{TEMP_ORIGINALS_DIRECTORY_PATH}/{user_input_original_to_open}')
    selected_original_exif = selected_original.info.get('exif')
    renamed_selected_original = rename_original_to_temp(user_input_original_to_open)
    if selected_original_exif is not None:
        selected_original.save(f'{TEMP_DIRECTORY_PATH}/{renamed_selected_original}', quality = 100, exif = selected_original_exif)
    elif selected_original_exif is None:
        selected_original.save(f'{TEMP_DIRECTORY_PATH}/{renamed_selected_original}', quality = 100)   
    os.system(f'open -a Preview {TEMP_DIRECTORY_PATH}/{renamed_selected_original}')
    user_input_delete_view_original(renamed_selected_original)

def image_width_height(image_path):
    image = Image.open(image_path)
    if hasattr(image, '_getexif'):
        width, height = image.size
        exif = image._getexif()
        if exif:
            orientation = exif.get(0x0112)
            if orientation in [5, 6, 7, 8]:
                width, height = height, width
    return(width, height)

def image_horizontal(image_path):
    image = Image.open(image_path)
    horizontal = True
    if hasattr(image, '_getexif'):
        exif = image._getexif()
        if exif:
            orientation = exif.get(0x0112)
            print(image_path, orientation)
            if orientation in [5, 6, 7, 8]:
                horizontal = False
    return horizontal

def compression(user_input_original_to_open):
    user_input_original_path = Path(ORIGINALS_DIRECTORY_PATH, user_input_original_to_open)
    user_input_original = Image.open(user_input_original_path)
    user_input_original_size = '{:.2f}'.format(os.path.getsize(user_input_original_path) / 1000000)
    user_input_original_exif = user_input_original.info.get('exif')
    while True:
        user_input_target_size = input(f'Original Size: {user_input_original_size}MB\nEnter Target Size [MB]: ')
        modified_user_input_target_size = (float(user_input_target_size) * 1000000)
        if user_input_target_size.isdigit():
            for level_of_compression in range(95, 0, -5):
                if float(user_input_target_size) >= float(user_input_original_size):
                    print(f'\nOriginal size {float(user_input_original_size)}MB has already met target size of {int(user_input_target_size)}.00MB')
                    return
                else:
                    temp_name = rename_original_to_temp(user_input_original_to_open, f'C{level_of_compression}')
                    temp_path = Path(TEMP_DIRECTORY_PATH, temp_name)
                    if user_input_original_exif is not None:
                        user_input_original.save(temp_path, quality = level_of_compression, exif = user_input_original_exif)
                    elif user_input_original_exif is not None:
                        user_input_original.save(temp_path, quality = level_of_compression)
                    temp_size = os.path.getsize(temp_path)
                    if int(temp_size) <= int(modified_user_input_target_size):
                        modified_temp_size = '{:.2f}'.format(temp_size / 1000000)
                        renamed_temp = rename_temp_to_original(temp_name, f'C{level_of_compression}')
                        current_temp_directory_path = Path(TEMP_DIRECTORY_PATH, temp_name)
                        new_temp_directory_path = Path(RENDERS_DIRECTORY_PATH, renamed_temp)
                        os.rename(current_temp_directory_path, new_temp_directory_path)
                        time.sleep(2)
                        print(f'Original image has been compressed to {float(modified_temp_size)}MB')
                        return
                    else:
                        send2trash.send2trash(temp_path)
        else:
            print('Enter a Whole Number')

def gaussian_blur(user_input_original_to_open):
    user_input_original_path = Path(ORIGINALS_DIRECTORY_PATH, user_input_original_to_open)
    user_input_original = Image.open(user_input_original_path)
    user_input_original_exif = user_input_original.info.get('exif')
    while True:
        user_input_radius = input('Enter Gaussian Blur Level [10 - 99]: ')
        temp_name = rename_original_to_temp(user_input_original_to_open, f'G{user_input_radius}')
        temp_directory_path = Path(TEMP_DIRECTORY_PATH, temp_name)
        if user_input_radius.isdigit():
            processed_user_input_radius = int(user_input_radius)/10
            if 1 <= processed_user_input_radius <= 9.9:
                user_input_original_blurred = user_input_original.filter(ImageFilter.GaussianBlur(radius = processed_user_input_radius))
                if user_input_original_exif is not None:
                    user_input_original_blurred.save(temp_directory_path, quality = 100, exif = user_input_original_exif)
                elif user_input_original_exif is None:
                    user_input_original_blurred.save(temp_directory_path, quality = 100)
                os.system(f'open -a Preview {temp_directory_path}')
                render_or_delete(temp_name, f'G{user_input_radius}')
                break
            else:
                print('\nEnter Number Between 10 and 99')
        else:
            print('\nEnter a Number [10 - 99]')

def watermark(user_input_original_to_open):
    check_watermark()
    original_path = Path(ORIGINALS_DIRECTORY_PATH, user_input_original_to_open)
    original = Image.open(original_path)
    original_exif = original.info.get('exif')
    original_width, original_height = image_width_height(original_path)
    watermark = Image.open(WATERMARK_PATH)
    while True:
        user_input_downsize_factor = input('Enter Size of Watermark [1 - 3]: ')
        if 1 <= int(user_input_downsize_factor) <= 3:
            processed_downsize_factor = int(user_input_downsize_factor) + 4
            if image_horizontal(original_path) == True:
                adjusted_watermark_width = original_width // processed_downsize_factor
                adjusted_watermark_height = adjusted_watermark_width // 5
                border_size = adjusted_watermark_width // 4
                resized_watermark = watermark.resize((adjusted_watermark_width, adjusted_watermark_height))
                watermark_coordinate = ((original_width - border_size - adjusted_watermark_width), (original_height - border_size - adjusted_watermark_height))
                original.paste(resized_watermark, watermark_coordinate, resized_watermark)
                temp_name = rename_original_to_temp(user_input_original_to_open, 'W0'+str(user_input_downsize_factor))
                original.save(f'{TEMP_DIRECTORY_PATH}/{temp_name}', quality = 100, exif = original_exif)
                render_or_delete(temp_name, 'W0'+str(user_input_downsize_factor))
                return
            elif image_horizontal(original_path) == False:
                adjusted_watermark_width = original_height // processed_downsize_factor
                adjusted_watermark_height = adjusted_watermark_width // 5
                border_size = adjusted_watermark_width // 4
                resized_watermark = watermark.resize((adjusted_watermark_width, adjusted_watermark_height))
                watermark_coordinate = ((border_size), (original_width - border_size - adjusted_watermark_width))
                rotated_watermark = resized_watermark.rotate(270, expand = True)
                original.paste(rotated_watermark, watermark_coordinate, rotated_watermark)
                temp_name = rename_original_to_temp(user_input_original_to_open, 'W0'+str(user_input_downsize_factor))
                original.save(f'{TEMP_DIRECTORY_PATH}/{temp_name}', quality = 100, exif = original_exif)
                render_or_delete(temp_name, 'W0'+str(user_input_downsize_factor))
                return
        else:
            print('Enter a Valid Number [1 - 3]')

def continue_or_end():
    while True:
        continue_or_end = input(f'\nContinue? [Y/N] ')
        modified_continue_or_end = continue_or_end.upper()
        if modified_continue_or_end == 'N':
            response = 'N'
            return response
        elif modified_continue_or_end == 'Y':
            return
        else:
            print('Enter Y or N')

def main_menu(user_input_original_to_open):
    menu = {
        1 : view_user_input_original,
        2 : compression,
        3 : gaussian_blur,
        4 : watermark
    }
    while True:
        user_input = input('\nSelect:\n[1] View Image\n[2] Compress Image\n[3] Apply Gaussian Blue\n[4] Overlay Watermark\n[5] Choose New Image\n\n')
        if user_input.isdigit():
            if int(user_input) in range(1, 6):
                print(f'\nSelected {user_input}')
                menu[int(user_input)](user_input_original_to_open)
                if continue_or_end() == 'N':
                    return
            else:
                print('\nEnter a Number Between 1 and 4')
        else:
            print('\nEnter the Option Number')

if __name__ == '__main__':
    #user_input_original_to_open = check_presence_of_user_input_original_to_ope('POOP_temp.JPG')
    #print(sorted(os.listdir(ORIGINALS_DIRECTORY_PATH)))

    #
    #check_necessary_directory()
    #clear_temp_originals_directory()
    #time.sleep(10)
    #copy_entire_originals_directory()
    #view_user_input_original('POOP.PNG')
    
    