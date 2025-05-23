from PIL import Image


def StoreFrame(img: Image.Image, folder: str, i: int):
    if i < 10:
        img.save(f'{folder}/frame00{str(i)}.jpg')
    elif i < 100:
        img.save(f'{folder}/frame0{str(i)}.jpg')
    else:
        img.save(f'{folder}/frame{str(i)}.jpg')
