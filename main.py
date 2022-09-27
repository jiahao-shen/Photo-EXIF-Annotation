from PIL import Image, ExifTags, ImageDraw, ImageFont


def annotation(file_name, bg=(255, 255, 255), show=True, save=False, font_scale=0.2, logo_scale=0.2, **kwargs):
    img = Image.open(file_name)

    img_w = img.width
    img_h = img.height

    blank_w = img_w
    blank_h = int(blank_w * 0.1)

    img_new = Image.new('RGB', (img_w, img_h + blank_h), bg)
    draw = ImageDraw.Draw(img_new)
    
    img_new.paste(img, (0, 0))

    # 全局字体大小
    font_size = 10
    while True:
        font = ImageFont.truetype('Helvetica', font_size)
        _, top, _, bottom = font.getbbox('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        if abs(bottom - top) >= int(blank_h * font_scale):
            break
        else: 
            font_size += 1

    exif = {
        ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in ExifTags.TAGS
    }

    # 间距
    space = int(blank_h * 0.3)

    # Logo
    if 'make' in kwargs:
        make = kwargs['make']
    else:
        make = exif['Make']
    logo = Image.open('assets/{}.png'.format(make))
    logo_h = int(blank_h * logo_scale) 
    logo_w = int(logo.width / logo.height * logo_h)
    logo = logo.resize((logo_w, logo_h))

    # 相机型号
    if 'model' in kwargs:
        model = kwargs['model']
    else:
        model = exif['Model']
    model = model.replace(make, '').lstrip()
    bbox = font.getbbox(str(model))
    # model_w = abs(bbox[2] - bbox[0])

    # 焦距
    focal = '{:d}mm'.format(int(exif['FocalLength']))
    bbox = font.getbbox(str(focal))
    focal_w = abs(bbox[2] - bbox[0])

    # 光圈
    aperture = 'f/{:.1f}'.format(float(exif['FNumber']))
    bbox = font.getbbox(str(aperture))
    aperture_w =  abs(bbox[2] - bbox[0])

     # 快门
    shutter = float(exif['ExposureTime'])
    if shutter >= 1:
        shutter = '{:d}"'.format(int(shutter))
    else:
        shutter = '1/{:d}'.format(int(1 / shutter))
    bbox = font.getbbox(str(shutter))
    shutter_w = abs(bbox[2] - bbox[0])

    # 感光度
    iso = 'ISO {:d}'.format(exif['ISOSpeedRatings'])
    bbox = font.getbbox(str(iso))
    iso_w = abs(bbox[2] - bbox[0])

    # 分割线
    left_w = blank_w - int(focal_w + aperture_w + shutter_w + iso_w + space * 5)

    draw.line((left_w, int(img_h + 0.2 * blank_h), left_w, int(img_h + 0.8 * blank_h)), fill=(200, 200, 200), width=int(blank_w / 500))

    img_new.paste(logo, (left_w - space - logo_w, img_h + int(blank_h * (1 - logo_scale) / 2)), mask=logo)

    draw.text((space, img_h + int(blank_h * 0.4)), model, (0, 0, 0), font=font)
    
    draw.text((left_w + space, img_h + int(blank_h * 0.4)), focal, (0, 0, 0), font=font)
   
    draw.text((left_w + focal_w + 2 * space, img_h + int(blank_h * 0.4)), aperture, (0, 0, 0), font=font) 
   
    draw.text((left_w + focal_w + aperture_w + 3 * space, img_h + int(blank_h * 0.4)), shutter, (0, 0, 0), font=font)

    draw.text((left_w + focal_w + aperture_w + shutter_w + 4 * space, img_h + int(blank_h * 0.4)), iso, (0, 0, 0), font=font)

    # 是否显示
    if show:
        img_new.show()

    # 是否保存
    if save:
        img_new.save('output/' + file_name.split('/')[-1], quality=100, subsampling=0)

if __name__ == '__main__':
    annotation('img/DSC04179.jpg')


