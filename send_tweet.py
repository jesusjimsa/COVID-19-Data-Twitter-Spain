import logging
from twython import Twython
from twython import TwythonError
from auth import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET_KEY

logging.basicConfig(filename='covid.log', level=logging.DEBUG)

twitter = Twython(
    API_KEY,
    API_SECRET_KEY,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)


def send_tweet(tweet_text, image_path):
    """
    Function to send the tweets with an image.

    Parameters
    ----------
    tweet_text : str
        Text that will be sent in the tweet.
    image_path : str
        Path to the image to be uploaded.
    """
    try:
        cases_image = open(image_path, 'rb')
        image_ids = twitter.upload_media(media=cases_image)
        cases_image.close()
        twitter.update_status(status=tweet_text, media_ids=image_ids['media_id'])
    except OSError:
        logging.error("Couldn't open the image")
    except TwythonError as e:
        logging.error("Couldn't send the tweet: %s", e)
    else:
        logging.debug("Tweet sent succesfully")
