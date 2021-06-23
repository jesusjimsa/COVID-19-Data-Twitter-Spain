from PIL import Image, ImageFont, ImageDraw
import logging

try:
    title_font = ImageFont.truetype('img_twitter/Roboto-Light.ttf', 90)
except OSError:
    logging.error("Couldn't open the font file")


def progressBar(img_path, bgcolor, color, x, y, w, h, progress, save_path):
    im = Image.open(img_path)
    drawObject = ImageDraw.Draw(im)

    '''BG'''
    drawObject.ellipse((x + w, y, x + h + w, y + h), fill=bgcolor)
    drawObject.ellipse((x, y, x + h, y + h), fill=bgcolor)
    drawObject.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=bgcolor)

    '''PROGRESS'''
    if(progress <= 0):
        progress = 0.01

    if(progress > 1):
        progress = 1

    w = w * progress
    drawObject.ellipse((x + w, y, x + h + w, y + h), fill=color)
    drawObject.ellipse((x, y, x + h, y + h), fill=color)
    drawObject.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=color)

    '''SAVE'''
    im.save(save_path)


def generate_cases_image(cases, deaths):
    cases_image = Image.open('img_twitter/cases_template.jpg')

    cases_img_editable = ImageDraw.Draw(cases_image)
    cases_img_editable.text((cases_image.width / 5 - 20, cases_image.height / 2 + 85), cases, (0, 0, 0),
                            font=title_font)
    cases_img_editable.text((cases_image.width / 2 + 190, cases_image.height / 2 + 85), deaths, (0, 0, 0),
                            font=title_font)

    cases_image.save('today_cases.jpg')

    cases_image.close()


def generate_vaccine_image(porcentaje_administradas, porcentaje_completas):
    progressBar('img_twitter/vaccines_template.jpg', (215, 215, 215), 'orange', 25, 190, 1100, 50,
                porcentaje_administradas / 100, 'vaccines_today.jpg')
    progressBar('img_twitter/vaccines_template.jpg', (215, 215, 215), 'orange', 25, 400, 1100, 50,
                porcentaje_completas / 100, 'vaccines_today.jpg')
