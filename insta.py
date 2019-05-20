from instapy import InstaPy
from instapy import smart_run
import schedule
import time
import datetime

init_job = False
date_job = datetime.datetime.now()
insta_username = "user"
insta_password = "pass"


def job_insta_py():

    if calc_date():
        global date_job
        date_job = datetime.datetime.now()

        session = InstaPy(username=insta_username,
                          password=insta_password,
                          headless_browser=True)

        with smart_run(session):
            print("init schedule")
            session.set_relationship_bounds(enabled=True,
                                            delimit_by_numbers=True,
                                            min_followers=30,
                                            min_following=30)

            to_follow = ['public alvo']

            session.set_skip_users(skip_private=False,
                                   skip_no_profile_pic=True, no_profile_pic_percentage=100)

            session.set_quota_supervisor(enabled=True,
                                         peak_follows=(70, 600),
                                         peak_unfollows=(70, 600))

            amout_follow = int(800 / len(to_follow))
            print(amout_follow)
            session.follow_user_followers(to_follow, amount=amout_follow,
                                          randomize=True, interact=False, sleep_delay=601)

            print("Sleeping")
            time.sleep(18000)

            session.unfollow_users(amount=1000, InstapyFollowed=(True, "all"),
                                   style="FIFO",
                                   unfollow_after=12 * 60 * 60, sleep_delay=601)
            print("Waiting schedule")


def calc_date():
    if not init_job:
        return True
    else:
        return (datetime.datetime.now() - date_job).days > 0

if (not init_job):
    job_insta_py()
    init_job = True

schedule.every().hour.do(job_insta_py)
while True:
    schedule.run_pending()
    time.sleep(600)

