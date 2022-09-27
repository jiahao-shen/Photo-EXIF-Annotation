from PIL import Image, ExifTags, ImageDraw, ImageFont


def annotation(file_name, bg=(255, 255, 255), show=True, save=False, **kwargs):
    img = Image.open(file_name)

    img_w = img.width
    img_h = img.height

    blank_w = img_w
    blank_h = int(blank_w * 0.1)

    img_new = Image.new('RGB', (img_w, img_h + blank_h), bg)
    draw = ImageDraw.Draw(img_new)
    
    img_new.paste(img, (0, 0))

    exif = {
        ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in ExifTags.TAGS
    }

    make = exif['Make'].lower()
    model = kwargs['model'] if 'model' in kwargs else exif['Model']
    focal = '{:d}mm'.format(int(exif['FocalLength']))
    aperture = 'f/{:.1f}'.format(float(exif['FNumber']))
    shutter = float(exif['ExposureTime'])
    if shutter >= 1:
        shutter = '{:d}sec'.format(shutter)
    else:
        shutter = '1/{:d}'.format(int(1 / shutter))
    iso = 'ISO {:d}'.format(exif['ISOSpeedRatings'])

    font_size = 10
    while True:
        font = ImageFont.truetype('Helvetica', font_size)
        _, top, _, bottom = font.getbbox('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        if abs(bottom - top) >= int(blank_h * 0.2):
            break
        else: 
            font_size += 1

    # 相机名称
    draw.text((int(blank_h * 0.4), img_h + int(blank_h * 0.4)), model, (0, 0, 0), font=font)

    # 分割线
    draw.line((int(blank_w * 0.55), int(img_h + 0.1 * blank_h), int(blank_w * 0.55), int(img_h + 0.9 * blank_h)), fill=(200, 200, 200), width=3)

    if make == 'sony':
        logo = Image.open('assets/Sony.png')
    elif make == 'canon':
        logo = Image.open('assets/Canon.png')
    elif make == 'hasselblad':
        logo = Image.open('assets/Hasselblad.png')
    
    logo_h = int(blank_h * kwargs['logo_scale']) 
    logo_w = int(logo.width / logo.height * logo_h)
    logo = logo.resize((logo_w, logo_h))

    # 厂商Logo
    img_new.paste(logo, (int(blank_w * 0.53 - logo_w), img_h + int(blank_h * (1 - kwargs['logo_scale']) / 2)), mask=logo)

    # 焦距
    draw.text((int(blank_w * 0.57), img_h + int(blank_h * 0.4)), focal, (0, 0, 0), font=font)

    # 光圈
    bbox = font.getbbox(str(focal))
    focal_w = abs(bbox[2] - bbox[0])
    draw.text((int(blank_w * 0.60 + focal_w), img_h + int(blank_h * 0.4)), aperture, (0, 0, 0), font=font)

    # 快门
    bbox = font.getbbox(str(aperture))
    aperture_w =  abs(bbox[2] - bbox[0])
    draw.text((int(blank_w * 0.63 + focal_w + aperture_w), img_h + int(blank_h * 0.4)), shutter, (0, 0, 0), font=font)

    # ISO
    bbox = font.getbbox(str(shutter))
    shutter_w = abs(bbox[2] - bbox[0])
    draw.text((int(blank_w * 0.66 + focal_w + aperture_w + shutter_w), img_h + int(blank_h * 0.4)), iso, (0, 0, 0), font=font)

    # 是否显示
    if show:
        img_new.show()

    # 是否保存
    if save:
        img_new.save('output/' + file_name.split('/')[-1], quality=100, subsampling=0)

if __name__ == '__main__':
    annotation('img/DSC02889.jpg', logo_scale=0.2)

    annotation('img/DJI_0398.jpg', logo_scale=0.4, model='DJI Mavic2 Pro')

    annotation('img/IMG_00038.jpg', logo_scale=0.2)
