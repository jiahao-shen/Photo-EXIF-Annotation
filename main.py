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

    # 全局字体大小
    font_size = 10
    while True:
        font = ImageFont.truetype('Helvetica', font_size)
        _, top, _, bottom = font.getbbox('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        if abs(bottom - top) >= int(blank_h * 0.2):
            break
        else: 
            font_size += 1

    exif = {
        ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in ExifTags.TAGS
    }

    # 品牌Logo
    if 'make' in kwargs:
        make = kwargs['make']
    else:
        make = exif['Make']
    
    logo = Image.open('assets/{}.png'.format(make))
    logo_h = int(blank_h * kwargs['logo_scale']) 
    logo_w = int(logo.width / logo.height * logo_h)
    logo = logo.resize((logo_w, logo_h))

    img_new.paste(logo, (int(blank_h * 0.3), img_h + int(blank_h * (1 - kwargs['logo_scale']) / 2)), mask=logo)

    # 相机型号
    if 'model' in kwargs:
        model = kwargs['model']
    else:
        model = exif['Model']
    model = model.replace(make, '').lstrip()

    draw.text((int(blank_h * 0.6 + logo_w), img_h + int(blank_h * 0.4)), model, (0, 0, 0), font=font)

    # 镜头Logo
    if 'lens_model' in kwargs:
        lens_logo = Image.open('assets/{}.png'.format(kwargs['lens_model']))
        lens_logo_h = int(blank_h * kwargs['logo_scale']) 
        lens_logo_w = int(lens_logo.width / lens_logo.height * lens_logo_h)
        lens_logo = lens_logo.resize((lens_logo_w, lens_logo_h))

        img_new.paste(lens_logo, (int(blank_w * 0.53 - lens_logo_w), img_h + int(blank_h * (1 - kwargs['logo_scale']) / 2)), mask=lens_logo)

    # 分割线
    draw.line((int(blank_w * 0.55), int(img_h + 0.2 * blank_h), int(blank_w * 0.55), int(img_h + 0.8 * blank_h)), fill=(200, 200, 200), width=int(blank_w / 500))

    # 焦距
    focal = '{:d}mm'.format(int(exif['FocalLength']))
    draw.text((int(blank_w * 0.57), img_h + int(blank_h * 0.4)), focal, (0, 0, 0), font=font)
    
    # 光圈
    aperture = 'f/{:.1f}'.format(float(exif['FNumber']))
    bbox = font.getbbox(str(focal))
    focal_w = abs(bbox[2] - bbox[0])
    draw.text((int(blank_w * 0.60 + focal_w), img_h + int(blank_h * 0.4)), aperture, (0, 0, 0), font=font) 

    # 快门
    shutter = float(exif['ExposureTime'])
    if shutter >= 1:
        shutter = '{:d}"'.format(int(shutter))
    else:
        shutter = '1/{:d}'.format(int(1 / shutter))
    
    bbox = font.getbbox(str(aperture))
    aperture_w =  abs(bbox[2] - bbox[0])
    draw.text((int(blank_w * 0.63 + focal_w + aperture_w), img_h + int(blank_h * 0.4)), shutter, (0, 0, 0), font=font)


    # 感光度
    iso = 'ISO {:d}'.format(exif['ISOSpeedRatings'])
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
    annotation('img/DSC04887.jpg', logo_scale=0.2, lens_model='GMaster')

    annotation('img/DSC02889.jpg', logo_scale=0.2)

    annotation('img/DJI_0398.jpg', logo_scale=0.4, make='DJI', model='Mavic2 Pro', lens_model='Hasselblad')

    annotation('img/IMG_00038.jpg', logo_scale=0.2)
