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


def send_tweet(tweet_text, image_path='', in_reply_to_id=None):
    """
    Function to send the tweets with an image.

    Parameters
    ----------
    tweet_text : str
        Text that will be sent in the tweet.
    image_path : str
        Path to the image to be uploaded. Default `''`
    in_reply_to_id : str
        ID of the tweet to reply to. Default `None`

    Returns
    -------
    response : dict
        Response from the Twitter API with info about the published tweet.
    """
    try:
        if in_reply_to_id is None:
            cases_image = open(image_path, 'rb')
            image_ids = twitter.upload_media(media=cases_image)
            cases_image.close()
            return twitter.update_status(status=tweet_text, media_ids=image_ids['media_id'])
        else:
            return twitter.update_status(status=tweet_text, in_reply_to_status_id=in_reply_to_id)
    except OSError:
        logging.error("Couldn't open the image")
    except TwythonError as e:
        logging.error("Couldn't send the tweet: %s", e)
    else:
        logging.debug("Tweet sent succesfully")
