from PIL import Image, ImageFont, ImageDraw
import logging

try:
    title_font = ImageFont.truetype('img_twitter/Roboto-Light.ttf', 90)
except OSError:
    logging.error("Couldn't open the font file")


def generate_cases_image(cases, deaths):
    cases_image = Image.open('img_twitter/cases_template.jpg')

    cases_img_editable = ImageDraw.Draw(cases_image)
    cases_img_editable.text((cases_image.width / 5 - 20, cases_image.height / 2 + 85), cases, (0, 0, 0),
                            font=title_font)
    cases_img_editable.text((cases_image.width / 2 + 190, cases_image.height / 2 + 85), deaths, (0, 0, 0),
                            font=title_font)

    cases_image.save('today_cases.jpg')

    cases_image.close()
