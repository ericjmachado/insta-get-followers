# imports
from instapy import InstaPy
from instapy import smart_run

import schedule
import time

# login credentials
insta_username = "login"
insta_password = "senha"

init_job = False

# get an InstaPy session!
# set headless_browser=True to run InstaPy in the background
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True)

with smart_run(session):
    """ Activity flow """
    # general settings
    def jobInstaPy() :
        session.set_relationship_bounds(enabled=True,
                                        delimit_by_numbers=True,
                                        max_followers=40000,
                                        min_followers=70,
                                        min_following=50)



        """ Massive Follow of users followers (I suggest to follow not less than
        3500/4000 users for better results)...
        """

        to_follow = ["Publico alvo",
                    ]
        session.set_skip_users(skip_private=True, private_percentage=100,
        			 skip_no_profile_pic=True, no_profile_pic_percentage=100)

        session.follow_user_followers(to_follow, amount=800,
                                     randomize=False, interact=False)

        """ First step of Unfollow action - Unfollow not follower users...
        """
        session.unfollow_users(amount=800, InstapyFollowed=(True, "nonfollowers"),
                               style="FIFO",
                               unfollow_after=16 * 60 * 60, sleep_delay=601)
        

        """ Second step of Massive Follow...
        """
        session.follow_user_followers(to_follow, amount=800,
                                    randomize=False, interact=False)

        """ Clean all followed user - Unfollow all users followed by InstaPy...
        """
        session.unfollow_users(amount=800, InstapyFollowed=(True, "all"),
                            style="FIFO", unfollow_after = 32 * 60 * 60,
                            sleep_delay=601)
        time.sleep(10800)



if (not init_job):
    jobInstaPy()
    init_job = True

schedule.every().second.do(jobInstaPy)

while True:
    schedule.run_pending()
    time.sleep(300)
