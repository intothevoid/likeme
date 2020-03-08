import yaml
import os
from instapy import InstaPy
from instapy import smart_run


"""
Loading data
"""
current_path = os.path.abspath(os.path.dirname(__file__))
data = yaml.safe_load(open("%s/data.yaml" % (current_path)))

insta_username = data['username']
insta_password = data['password']

"""
Get likers list i.e. the list of all users who liked your last
post. This list is then used to return the favour
"""
likers_list = ["urmillakadam"]

"""
Like last two posts of those who liked your post.
Spread the love!
"""
likers = InstaPy(username=insta_username,
                  password=insta_password,
                  disable_image_load=True,
                  multi_logs=False)

with smart_run(likers):
    print(u'💞 Showing likers some love 💖')
    likers.set_relationship_bounds(enabled=False)
    likers.set_skip_users(skip_private=False)
    likers.set_do_like(True,
                        percentage=100)
    likers.interact_by_users(likers_list,
                              amount=2,
                              randomize=False)