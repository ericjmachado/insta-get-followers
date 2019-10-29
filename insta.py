from instapy import InstaPy
from instapy import smart_run
import schedule
import time
import datetime
import random

init_job = False
date_job = datetime.datetime.now()
insta_username = ""
insta_password = ""


def job_insta_py():
    if calc_date():
        global date_job
        date_job = datetime.datetime.now()

        session = InstaPy(username=insta_username,
                          password=insta_password,
                          headless_browser=True)

        to_follow_original = ['maisgoias']

        with smart_run(session):
            print("init schedule")
            session.set_relationship_bounds(enabled=True,
                                            delimit_by_numbers=True,
                                            min_followers=50,
                                            min_following=50)

            list_count = len(to_follow_original)
            list_index = random.sample(range(list_count), list_count)
            to_follow = sort_list(to_follow_original, list_index)

            session.set_skip_users(skip_private=False,
                                   skip_no_profile_pic=True, no_profile_pic_percentage=100)

            session.set_quota_supervisor(enabled=True,
                                         sleep_after=["follows_h", "unfollows_h", "server_calls_h"],
                                         sleepyhead=True,
                                         stochastic_flow=True,
                                         peak_follows_hourly=40,
                                         peak_follows_daily=600,
                                         peak_unfollows_hourly=40,
                                         peak_unfollows_daily=600,
                                         peak_server_calls_hourly=170,
                                         peak_server_calls_daily=4000)

            amout_follow = 2000
            session.follow_user_followers(to_follow, amount=amout_follow,
                                          randomize=True, interact=False, sleep_delay=601)

            print("Sleeping")
            time.sleep(18000)

            session.unfollow_users(amount=1000, InstapyFollowed=(True, "all"),
                                   style="FIFO",
                                   unfollow_after=24 * 60 * 60, sleep_delay=601)
            print("Waiting schedule")


def calc_date():
    if not init_job:
        return True
    else:
        return (datetime.datetime.now() - date_job).days > 0


def sort_list(list1, list2):
    zipped_pairs = zip(list2, list1)

    z = [x for _, x in sorted(zipped_pairs)]

    return z


if not init_job:
    job_insta_py()
    init_job = True

schedule.every().hour.do(job_insta_py)
while True:
    schedule.run_pending()
    time.sleep(600)
