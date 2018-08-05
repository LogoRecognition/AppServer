# coding=utf-8
import os
from utils import *
from werkzeug.utils import secure_filename


def main():
    app = initialize()
    goods_folder_path = os.path.join(app.config['IMAGE_FOLDER'], 'goods')
    if not os.path.exists(goods_folder_path):
        os.makedirs(goods_folder_path)

    from app.model import classic_goods
    with open('scripts/goods.txt') as f:
        f.readline()
        for l in f.readlines():
            items = l.strip().split('|')
            if classic_goods.find_classic_goods(items[0], items[1]):
                print('%s already exists!' % items[0])
                continue
            img_path = os.path.join(goods_folder_path, secure_filename(items[1]+'_'+items[0]+'.jpg'))
            items[2] = download_image(items[2], img_path)
            try:
                classic_goods.add_classic_goods(*items)
            except Exception:
                print('Error occurred when adding %s' % items[0])


if __name__ == '__main__':
    main()
