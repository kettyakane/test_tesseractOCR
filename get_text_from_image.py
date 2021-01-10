import csv
import re
import sys

from PIL import Image
import pyocr.builders


# OCR精度を上げるために画像ファイルのコントラストを加工
def edit_Image(im):
    im = im.point(lambda x: x * 1.2)
    im = im.convert("L")
    return im


# OCRで読みこんだテキストのゴミを取り除く
def edit_Text(str):
    str = str.replace('.', '')
    str = str.replace(',', '')
    str = str.replace(' ', '')
    str = str.replace('\n\n', '\n')
    return str


def get_Num(str):
    str = re.search(r'\d+', str)
    return str


def get_text_from_image():

    # OCRでテキストに起こす
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)

    tool = tools[0]
    print("Will use tool '%s'" % (tool.get_name()))

    im_ori = Image.open("給与test.png")

    im_payment = edit_Image(im_ori.crop((1030, 260, 1770, 1055)))
    txt_payment = edit_Text(tool.image_to_string(
        im_payment,
        lang="jpn",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    ))

    im_deduction = edit_Image(im_ori.crop((1820, 260, 2525, 1055)))
    txt_deduction = edit_Text(tool.image_to_string(
        im_deduction,
        lang="jpn",
        builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    ))

    # リストに格納
    list_payment = [re.sub('[^0-9]', '', s) for s in txt_payment.split('\n')]
    list_deduction = [re.sub('[^0-9]', '', s)
                      for s in txt_deduction.split('\n')]

    list_payment.extend(list_deduction)
    print(list_payment)

    with open('payment.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(list_payment)


if __name__ == "__main__":
    get_text_from_image()
