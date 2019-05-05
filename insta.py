# imports
from instapy import InstaPy
from instapy import smart_run

import schedule
import time

# login credentials
insta_username = "user"
insta_password = "pass"

init_job = False

# get an InstaPy session!
# set headless_browser=True to run InstaPy in the background
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True)

def jobInstaPy() :

    with smart_run(session):
        """ Activity flow """
        # general settings
        session.set_relationship_bounds(enabled=True,
                                        delimit_by_numbers=True,
                                        max_followers=40000,
                                        min_followers=70,
                                        min_following=50)



        """ Massive Follow of users followers (I suggest to follow not less than
        3500/4000 users for better results)...
        """

        to_follow = ["publico alvo"
	            ] 
        session.set_skip_users(skip_private=True, private_percentage=40,
                        skip_no_profile_pic=True, no_profile_pic_percentage=100)
	
	amout_follow = 800 / len(to_follow)

        session.follow_user_followers(to_follow, amount=amout_follow,
                                        randomize=False, interact=False, sleep_delay=601)

	time.sleep(7200)

        session.unfollow_users(amount=800, InstapyFollowed=(True, "all"),
                                style="FIFO",
                                unfollow_after=12 * 60 * 60, sleep_delay=601)
        time.sleep(3600)



if (not init_job):
    jobInstaPy()
    init_job = True


schedule.every(24).hours.do(jobInstaPy)
while True:
    schedule.run_pending()
    time.sleep(300)
