# coding=utf-8
import os
from utils import *


def main():
    app = initialize()
    logo_folder_path = os.path.join(app.config['IMAGE_FOLDER'], 'logos')
    if not os.path.exists(logo_folder_path):
        os.makedirs(logo_folder_path)

    from app.model import brands
    with open('scripts/brands.txt') as f:
        f.readline()
        for l in f.readlines():
            items = l.strip().split('|')
            if brands.find_brand_by_name(items[0]):
                print('%s already exists!' % items[0])
                continue
            img_path = os.path.join(logo_folder_path, items[0]+'.jpg')
            items[2] = download_image(items[2], img_path)
            try:
                brands.add_brand(*items)
            except Exception:
                print('Error occurred when adding %s' % items[0])


if __name__ == '__main__':
    main()
