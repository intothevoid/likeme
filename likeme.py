import yaml
import time
import os, sys
from instapy import InstaPy
from instapy import smart_run
from instapy.commenters_util import users_liked
from instapy.commenters_util import get_photo_urls_from_profile
from instapy.commenters_util import click_element
from instapy.commenters_util import web_address_navigator
import instaloader


"""
Loading data
"""
current_path = os.path.abspath(os.path.dirname(__file__))
data = yaml.safe_load(open("%s/data.yaml" % (current_path)))

insta_username = data['username']
insta_password = data['password']

def main():

    """
    Like last two posts of those who liked your post.
    Spread the love!
    """
    likers = InstaPy(username=insta_username,
                    password=insta_password,
                    disable_image_load=True,
                    multi_logs=False,
                    headless_browser=True)

    """
    Grab the photo url from our latest post
    """
    # photo_url = get_photo_urls_from_profile(
    #     likers.browser, insta_username, links_to_return_amount=1, randomize=False
    # )

    # # only get one url
    # if isinstance(photo_url, list):
    #     photo_url = photo_url.pop()

    """
    Get likers list i.e. the list of all users who liked your last
    post. This list is then used to return the favour
    """
    # likers_list = users_liked(likers.browser, photo_url, 75)
    likers_list = get_post_likers()

    with smart_run(likers):
        print(u'💞 Showing likers some love 💖')
        likers.set_relationship_bounds(enabled=False)
        likers.set_skip_users(skip_private=False)
        likers.set_do_like(True, percentage=100)
        likers.interact_by_users(likers_list, amount=1, randomize=False)

def get_post_likers():
    likers = list()
    L = instaloader.Instaloader() 

    profile = instaloader.Profile.from_username(L.context, insta_username)

    for post in profile.get_posts():
        post_likes = post.get_likes()

        for likee in post_likes:
            likers.append(likee.username)

        # We return as we only want the likers for our first post
        return likers

if __name__ == "__main__":
    main()