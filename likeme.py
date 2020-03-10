import yaml
import time
import os, sys
from instapy import InstaPy
from instapy import smart_run
from instapy.commenters_util import users_liked
from instapy.commenters_util import get_photo_urls_from_profile
from instapy.commenters_util import click_element
from instapy.commenters_util import web_address_navigator


"""
Loading data
"""
current_path = os.path.abspath(os.path.dirname(__file__))
data = yaml.safe_load(open("%s/data.yaml" % (current_path)))

insta_username = data['username']
insta_password = data['password']


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
photo_url = get_photo_urls_from_profile(
    likers.browser, insta_username, links_to_return_amount=1, randomize=False
)

# only get one url
if isinstance(photo_url, list):
    photo_url = photo_url.pop()

"""
Get likers list i.e. the list of all users who liked your last
post. This list is then used to return the favour
"""
# likers_list = users_liked(likers.browser, photo_url, 75)


# likers.browser.get(photo_url)
web_address_navigator(likers.browser, photo_url)

userid_element = likers.browser.find_elements_by_xpath("//div/article/div[2]/section[2]/div/div/button")[0]
click_element(likers.browser, userid_element)
time.sleep(2)

# here, you can see user list you want.
# you have to scroll down to download more data from instagram server.
# loop until last element with users table view height value.

users = []

height = likers.browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div").value_of_css_property("padding-top")
match = False
while match==False:
    lastHeight = height

    # step 1
    elements = likers.browser.find_elements_by_xpath("//*[@id]/div/a")

    # step 2
    for element in elements:
        if element.get_attribute('title') not in users:
            users.append(element.get_attribute('title'))

    # step 3
    likers.browser.execute_script("return arguments[0].scrollIntoView();", elements[-1])
    time.sleep(1)

    # step 4
    height = likers.browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div").value_of_css_property("padding-top")
    if lastHeight==height:
        match = True


with smart_run(likers):
    print(u'💞 Showing likers some love 💖')
    print(users)
    # likers.set_relationship_bounds(enabled=False)
    # likers.set_skip_users(skip_private=False)
    # likers.set_do_like(True,
    #                     percentage=100)
    # likers.interact_by_users(likers_list,
    #                           amount=2,
    #                           randomize=False)