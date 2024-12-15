import os
import time
import platform
import subprocess

import send2trash
#import re

from PIL import Image, ImageFilter, ImageDraw, ImageFont
from pathlib import Path
import matplotlib.pyplot as plt

USERNAME = Path.home()
# CHANGE DIRECTORY NAME TO BE USER INPUT SELECTED LOCATION
DIRECTORY_NAME = 'Desktop'
ROOT_FOLDER_DIRECTORY = 'ABE'
ROOT_FOLDER_DIRECTORY_PATH = f'{USERNAME}/{DIRECTORY_NAME}/{ROOT_FOLDER_DIRECTORY}'
ORIGINALS_DIRECTORY = 'ORIGINALS'
ORIGINALS_DIRECTORY_PATH = f'{USERNAME}/{DIRECTORY_NAME}/{ROOT_FOLDER_DIRECTORY}/{ORIGINALS_DIRECTORY}'
RENDERS_DIRECTORY = 'RENDERS'
RENDERS_DIRECTORY_PATH = f'{USERNAME}/{DIRECTORY_NAME}/{ROOT_FOLDER_DIRECTORY}/{RENDERS_DIRECTORY}'
TEMP_DIRECTORY = 'TEMP'
TEMP_DIRECTORY_PATH = f'{USERNAME}/{DIRECTORY_NAME}/{ROOT_FOLDER_DIRECTORY}/{TEMP_DIRECTORY}'
TRASH_DIRECTORY = 'TRASH'
TRASH_DIRECTORY_PATH = Path(USERNAME, DIRECTORY_NAME, ROOT_FOLDER_DIRECTORY, TEMP_DIRECTORY,TRASH_DIRECTORY)
REJECT_ORIGINALS_DIRECTORY = 'REJECT'
REJECT_ORIGINALS_DIRECTORY_PATH = f'{USERNAME}/{DIRECTORY_NAME}/{ROOT_FOLDER_DIRECTORY}/{REJECT_ORIGINALS_DIRECTORY}'
ACCEPTED_IMAGE_SUFFIX = ('.PNG', '.JPG', '.JPEG', '.TIF', '.TIFF') # GATHER ACCEPTED IMAGE EXTENSIONS HERE FOR EASY UPDATING

def directory_setup():

    main_directories = ('ORIGINALS', 'TEMP', 'REJECT')

    directories = (ROOT_FOLDER_DIRECTORY_PATH, ORIGINALS_DIRECTORY_PATH, RENDERS_DIRECTORY_PATH, TEMP_DIRECTORY_PATH, REJECT_ORIGINALS_DIRECTORY_PATH, TRASH_DIRECTORY_PATH)
    for directory in directories:
        if os.path.isdir(directory) != True:
            os.mkdir(directory)

    'COMPRESSION', 'GAUSSIAN BLUR', 'WATERMARK'

def originals_format_homogeniser_and_rejector():
    while True:
        for _ in os.listdir(ORIGINALS_DIRECTORY_PATH):
            image_path = Path(ORIGINALS_DIRECTORY_PATH, _)
            modified_image_path = Path(ORIGINALS_DIRECTORY_PATH, _.upper())
            if image_path.is_file() and image_path.suffix.upper() in ACCEPTED_IMAGE_SUFFIX:
                image = Image.open(image_path)
                original_exif = image.info.get('exif')
                if image.mode != 'RGB':
                    modified_image = image.convert('RGB')
                    if original_exif is not None:
                        modified_image.save(image_path, quality = 100, exif = original_exif)
                    if original_exif is None:
                        modified_image.save(image_path, quality = 100)
                image.close()
                os.rename(image_path, modified_image_path)
            else:
                os.rename(image_path, os.path.join(REJECT_ORIGINALS_DIRECTORY_PATH, _))
        return

def check_presence_of_user_input_original_to_open(): # change else print to raise valueerror
    while True:
        user_input = input('\nEnter Name of Original: ')
        processed_user_input = user_input.upper()
        if processed_user_input in os.listdir(ORIGINALS_DIRECTORY_PATH):
            return processed_user_input
        else:
            print('\nEnter a Valid File Name')

def get_file_extension(user_input_to_open):
    return ('.' + str(user_input_to_open).split('.')[1])

def rename_original_to_temp(original_name):
    original_path = Path(ORIGINALS_DIRECTORY_PATH, original_name)
    original_extension = get_file_extension(original_name)
    temp = original_name[:-len(original_extension)] + f'_TEMP{original_extension}'
    return temp

def rename_temp_to_original(temp_name):
    temp_path = Path(TEMP_DIRECTORY_PATH, temp_name)
    original_extension = get_file_extension(temp_name, TEMP_DIRECTORY_PATH)
    if str(temp_path).endswith(('_TEMP.PNG', '_TEMP.JPG', '_TEMP.JPEG', '_TEMP.TIF', '_TEMP.TIFF')):
        original = temp_name[:-(len(original_extension)+5)] + f'{original_extension}'
        print(original)
    return original
    
def render_or_delete(selected_image):
    while True:
        user_input = input('Render[R] or Delete[D]: ')
        processed_user_input = user_input.upper()
        temp_directory_path = Path(TEMP_DIRECTORY_PATH, selected_image)
        render_directory_path = Path(RENDERS_DIRECTORY_PATH, selected_image)
        trash_directory_path = Path(TRASH_DIRECTORY_PATH, str(time.time()))
        if processed_user_input == 'D':
            os.rename(temp_directory_path, trash_directory_path)
            return
        elif processed_user_input == 'R':
            os.rename(temp_directory_path, render_directory_path)
            return
        else:
            print('Enter R or D')

def print_all_original():
    for _ in sorted(os.listdir(TEMP_ORIGINALS_DIRECTORY_PATH)):
        original_path = Path(TEMP_ORIGINALS_DIRECTORY_PATH, _)
        if original_path.suffix in ACCEPTED_IMAGE_SUFFIX:
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

def view_image(directory_path, selected_image):
    current_os = platform.system()
    image_path = Path(directory_path, selected_image)
    
    if current_os == 'Darwin':
        subprocess.call(['open', image_path])
    elif current_os == 'Windows':
        os.startfile(image_path)
    else:
        print('Unsupported OS')

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

def original_data(selected_original): #function to collate all commonly used original data. contemplate on implementation
    original_path = Path(ORIGINALS_DIRECTORY_PATH, selected_original)
    original = Image.open(original_path)
    original_size = os.path.getsize(original_path)
    original_exif = original.info.get('exif')

    return original, original_path, original_size, original_exif

def compression(selected_original): # done
    original_path = Path(ORIGINALS_DIRECTORY_PATH, selected_original)
    original = Image.open(original_path)
    original_size = os.path.getsize(original_path)
    modified_original_size = '{:.2f}'.format(float(original_size) / 1000000)
    original_exif = original.info.get('exif')
    original_no_extension = Path(original_path).stem.split('.')[0]
    while True:
        target_size = input(f'Original Size: {modified_original_size}MB\nEnter Target Size [MB]: ')
        if target_size.isdigit():
            modified_target_size = (float(target_size) * 1000000)
            for level_of_compression in range(100, 0, -1):
                if float(target_size) >= float(original_size):
                    return
                else:
                    temp_directory_path = Path(TEMP_DIRECTORY_PATH, original_no_extension + '.JPG')
                    render_directory_path = Path(RENDERS_DIRECTORY_PATH, original_no_extension + '.JPG')
                    trash_directory_path = Path(TRASH_DIRECTORY_PATH, str(time.time()))
                    if original_exif is not None:
                        original.save(temp_directory_path, quality = level_of_compression, exif = original_exif)
                    elif original_exif is None:
                        original.save(temp_directory_path, quality = level_of_compression)
                    temp_size = os.path.getsize(temp_directory_path)
                    print(level_of_compression, temp_size)
                    if int(temp_size) <= int(modified_target_size):
                        if os.path.exists(render_directory_path):
                            os.rename(render_directory_path, trash_directory_path)
                        modified_temp_size = '{:.2f}'.format(temp_size / 1000000)
                        os.rename(temp_directory_path, render_directory_path)
                        print(f'Original image has been compressed to {float(modified_temp_size)}MB')
                        return
                    else:
                        os.rename(temp_directory_path, trash_directory_path)
        else:
            print('Enter a Whole Number')

def gaussian_blur(selected_original): # done
    original_path = Path(ORIGINALS_DIRECTORY_PATH, selected_original)
    original = Image.open(original_path)
    original_exif = original.info.get('exif')
    while True:
        blur = input('Enter Gaussian Blur Level [1 - 30]: ')
        temp_directory_path = Path(TEMP_DIRECTORY_PATH, selected_original)
        if blur.isdigit():
            if 1 <= int(blur) <= 30:
                original_blurred = original.filter(ImageFilter.GaussianBlur(int(blur)))
                if original_exif is not None:
                    original_blurred.save(temp_directory_path, quality = 100, exif = original_exif)
                elif original_exif is None:
                    original_blurred.save(temp_directory_path, quality = 100)
                view_image(TEMP_DIRECTORY_PATH, selected_original)
                render_or_delete(selected_original)
                return
            else:
                print('\nEnter a Number [1 - 30]')
        else:
            print('\nEnter a Number [1 - 30]')

def watermark(selected_original):
    original_path = Path(ORIGINALS_DIRECTORY_PATH, selected_original)
    original = Image.open(original_path)
    original_exif = original.info.get('exif')

    original_watermark = original.copy()

    draw = ImageDraw.Draw(original_watermark)

    w,h = original.size
    x, y = int(39/40 * w), int(29/30 * h)
    if x > y:
        font_size = y / 2
    else:
        font_size = x / 2

    custom_font = ImageFont.truetype('custom_font.otf', int(font_size/6))

    draw.text((x, y), 'XXXX', fill = (255, 255, 255), font = custom_font, anchor = 'rb')

    if original_exif is not None:
        original_watermark.save(Path(TEMP_DIRECTORY_PATH, selected_original), quality = 100, exif = original_exif)
    elif original_exif is None:
        original_watermark.save(Path(RENDERS_DIRECTORY_PATH, selected_original), quality = 100)

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

def main_menu():
    menu = {
        1 : check_presence_of_user_input_original_to_open, # what does this do, consider removing it
        2 : view_user_input_original,
        3 : compression,
        4 : gaussian_blur,
        5 : watermark
    }
    originals_format_homogeniser_and_rejector()
    while True:
        user_input = input('\nSelect:\n [1] Choose Image\n [2] View Image\n [3] Compress Image [Note: Images will be exported in .JPG]\n [4] Apply Gaussian Blue  \n [5] Overlay Watermark\n')
        if user_input.isdigit():
            if int(user_input) in range(1, 6):
                print(f'\nSelected {user_input}')
                menu[int(user_input)](check_presence_of_user_input_original_to_open())
                if continue_or_end() == 'N':
                    return
            else:
                print('\nEnter a Number Between 1 and 4')
        else:
            print('\nEnter the Option Number')

def clear_trash(): #check if trash is not empty, if so, run it when quitting programme only
    send2trash.send2trash(TRASH_DIRECTORY_PATH)
    os.mkdir(TRASH_DIRECTORY_PATH)

if __name__ == '__main__':
    watermark('hq720.jpg')
    clear_trash()
    #function to delete all trash immediately after programme runs
    
    pass