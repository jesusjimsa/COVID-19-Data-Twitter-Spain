"""
Create images to add to the tweets.

Created by Jesús Jiménez Sánchez.
"""
import logging
from PIL import Image, ImageFont, ImageDraw

try:
    title_font = ImageFont.truetype('img_twitter/Roboto-Light.ttf', 90)
    title_font_small = ImageFont.truetype('img_twitter/Roboto-Light.ttf', 50)
    title_font_smaller = ImageFont.truetype('img_twitter/Roboto-Light.ttf', 40)
except OSError:
    logging.error("Couldn't open the font file")


def progressBar(img_path, bgcolor, color, x, y, w, h, progress, save_path):
    '''
    Add a progress bar with rounded corners to a given image.

    Parameters
    ----------
    img_path : str
        Path to image.
    bgcolor : str, tuple or hex
        Background color of the progress bar.
    color : str, tuple or hex
        Color of the progress in the bar.
    x : int
        Horizontal position.
    y : int
        Vertical position.
    w : int
        Width.
    h : int
        Height.
    progress : float
        Progress of the bar. Must be between 0 and 1.
    save_path : str
        Path to save the image with the progress bar.
    '''
    im = Image.open(img_path)
    drawObject = ImageDraw.Draw(im)

    # BG
    drawObject.ellipse((x + w, y, x + h + w, y + h), fill=bgcolor)
    drawObject.ellipse((x, y, x + h, y + h), fill=bgcolor)
    drawObject.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=bgcolor)

    # PROGRESS
    if progress <= 0:
        progress = 0.01

    progress = min(progress, 1)

    w = w * progress
    drawObject.ellipse((x + w, y, x + h + w, y + h), fill=color)
    drawObject.ellipse((x, y, x + h, y + h), fill=color)
    drawObject.rectangle((x + (h / 2), y, x + w + (h / 2), y + h), fill=color)

    # SAVE
    im.save(save_path)


def generate_cases_image(cases, deaths):
    '''
    Add text for the cases and deaths image.

    Parameters
    ----------
    cases : str
        Number of cases to write in the image.
    deaths : str
        Number of deaths to write in the image.
    '''
    cases_image = Image.open('img_twitter/cases_template.jpg')

    cases_img_editable = ImageDraw.Draw(cases_image)
    cases_img_editable.text((cases_image.width / 5 - 20, cases_image.height / 2 + 85), cases, (0, 0, 0),
                            font=title_font)
    cases_img_editable.text((cases_image.width / 2 + 190, cases_image.height / 2 + 85), deaths, (0, 0, 0),
                            font=title_font)

    cases_image.save('today_cases.jpg')

    cases_image.close()


def generate_vaccine_image(percentage_first, text_first, percentage_complete, text_complete, percentage_booster,
                           text_booster, date):
    '''
    Add text and progress bars to the vaccines image.

    Parameters
    ----------
    percentage_first : float
        Percentage of people with first dose.
    text_first : str
        Text that includes the number of first doses and the percentage.
    percentage_complete : float
        Percentage of people with both doses.
    text_complete : str
        Text that includes the number of complete doses and the percentage.
    date : str
        Date in text of the current day.
    '''
    progressBar('img_twitter/vaccines_template.jpg', (215, 215, 215), 'orange', 25, 180, 1100, 50,
                percentage_first / 100, 'vaccines_today.jpg')
    progressBar('vaccines_today.jpg', (215, 215, 215), 'orange', 25, 340, 1100, 50,
                percentage_complete / 100, 'vaccines_today.jpg')
    progressBar('vaccines_today.jpg', (215, 215, 215), 'orange', 25, 500, 1100, 50,
                percentage_booster / 100, 'vaccines_today.jpg')

    vaccine_image = Image.open('vaccines_today.jpg')

    vaccine_img_editable = ImageDraw.Draw(vaccine_image)
    vaccine_img_editable.text((vaccine_image.width - 300, 5), date, (0, 0, 0),
                              font=title_font_small)
    vaccine_img_editable.text((vaccine_image.width / 5, vaccine_image.height / 2 - 220), text_first, (0, 0, 0),
                              font=title_font_smaller)
    vaccine_img_editable.text((vaccine_image.width / 4 - 20, vaccine_image.height / 2 - 50), text_complete, (0, 0, 0),
                              font=title_font_smaller)
    vaccine_img_editable.text((vaccine_image.width / 4 - 15, vaccine_image.height / 2 + 115), text_booster, (0, 0, 0),
                              font=title_font_smaller)

    vaccine_image.save('vaccines_today.jpg')

    vaccine_image.close()
