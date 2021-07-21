from datetime import datetime
from datetime import timedelta
import pickle
import praw
import pandas as pd
import matplotlib.pyplot as plt
import time

REDDIT_POPULAR = './reddit_popular.csv'
SAVE_FILE = './reddit_popular_data.pkl'
user_data = False


# required installations:
# pandas, matplotlib


def subreddit():
    # TODO: sanitize input, potentially unsafe or unintended access to data user is not suppose to have access to (Do
    # this for all params in all functions
    print("Input which subreddit")
    subreddit_name = input()
    print("Sort by: [hot | new | top]")
    sort_order = input()

    subreddit = reddit.subreddit(subreddit_name)
    if sort_order == 'top':
        submissions = subreddit.top(limit=10)
    elif sort_order == 'new':
        submissions = subreddit.new(limit=10)
    else:
        submissions = subreddit.hot(limit=10)

    for submission in submissions:
        print(submission.title)
        print(submission.score)
        print(submission.id)
        print(submission.url)


def users():
    print("Type username:")
    username = input()
    user = reddit.redditor(username)
    for submission in user.submissions.new():
        print(submission.title)
        print(submission.score)
        print(submission.url)


# TODO: Because this goes through 1000 entries the processing can be slow. Consider doing this multithreaded
def popular():
    new_submissions = dict()
    top_subreddits = dict()
    submissions = reddit.subreddit("popular").hot(limit=1000)
    try:
        [popular_submissions, top_subreddits] = open_file(SAVE_FILE)
        parse_submissions(submissions, new_submissions, popular_submissions, True, top_subreddits)
    # TODO: OSError may be for something other than file not found, be sure to check
    except OSError:
        popular_submissions = dict()
        parse_submissions(submissions, new_submissions, popular_submissions, False, top_subreddits)

    # TODO: Look into storing in a database instead a of pickle file.
    save_file_popular(new_submissions, top_subreddits, SAVE_FILE)
    plot_pie_chart(top_subreddits)


def posts():
    print("Enter ID:")
    s_id = input()
    submission = reddit.submission(s_id)
    score = submission.score
    upvote_ratio = submission.upvote_ratio
    num_comments = submission.num_comments
    print(submission.title + "\nscore: " + str(score) + "\nupvote_ratio: " + str(upvote_ratio) + "\nnum_comments: " +
          str(num_comments))
    return s_id, score, upvote_ratio, num_comments


def retrieve_post_info(s_id):
    submission = reddit.submission(s_id)
    return submission.score, submission.upvote_ratio, submission.num_comments


# https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679
# https://ostechnix.com/a-beginners-guide-to-cron-jobs/
# TODO: Best to try to do this through a virtual environment
# Cron vs timer? which one is better
def track_post():
    s_id, score, upvote_ratio, num_comments = posts()
    print("How long do you want to track this post?: __ minutes")
    track_time = input()
    print("How long do you want the intervals to be between checking the post?: __ minutes")
    interval_length = int(input()) * 60
    curr_date = datetime.now()
    end_time = curr_date + timedelta(minutes=int(track_time))
    file_name = str(s_id) + "_track_post"

    try:
        post_data = open_file(file_name)
        plot_line_chart(post_data)
    except OSError:
        post_data = []

    while curr_date < end_time:
        post_data.append((score, upvote_ratio, num_comments, datetime.now()))
        save_file_track_post(post_data, file_name)
        time.sleep(interval_length)
        curr_date = datetime.now()
        score, upvote_ratio, num_comments = retrieve_post_info(s_id)
        print("\nscore: "+str(score) + "\nupvote_ratio: " + str(upvote_ratio) + "\nnum_comments:" + str(num_comments))

    plot_line_chart(post_data)


def plot_line_chart(data):
    df = pd.DataFrame(data)
    df.columns = ['score', 'upvote_ratio', 'num_comments', 'time']
    print(df)
    df.set_index("time").plot(y=0)
    plt.show()


def plot_pie_chart(new_submissions):
    df = pd.DataFrame(new_submissions, index=[0]).transpose()
    print(df)
    df.plot.pie(y=0)
    plt.show()


# https://stackabuse.com/reading-and-writing-excel-files-in-python-with-the-pandas-library
def open_file(file_name):
    o_file = open(file_name, "rb")
    submissions = pickle.load(o_file)
    return submissions


def save_file_popular(new_submissions, top_submissions, file_name):
    s_file = open(file_name, "wb")
    pickle.dump([new_submissions, top_submissions], s_file)
    df = pd.DataFrame(new_submissions, index=['num', 'ids']).transpose()
    df.to_csv(REDDIT_POPULAR)


def save_file_track_post(post_data, file_name):
    s_file = open(file_name, "wb")
    pickle.dump(post_data, s_file)


def compare_subreddit_val(top_subreddits, new_subreddit):
    num_nposts = new_subreddit[1]
    subreddit_nname = new_subreddit[0]
    tuple_top_subreddits = sorted(top_subreddits.items(), key=lambda x: x[1])

    for (subreddit_name, num_posts) in tuple_top_subreddits:
        if num_posts < num_nposts and subreddit_name != subreddit_nname:
            top_subreddits.pop(subreddit_name)
            top_subreddits[subreddit_nname] = num_nposts
            return top_subreddits


# TODO: A lot of nested if statements try to reduce them to improve readability
def parse_submissions(submissions, new_submissions, popular_submissions, has_dict, top_subreddits):
    for submission in submissions:
        subreddit = submission.subreddit.display_name
        if subreddit in new_submissions.keys():
            if subreddit not in popular_submissions.keys() or submission.id not in popular_submissions[subreddit]['ids']:
                new_submissions[subreddit]['num'] = new_submissions[subreddit]['num'] + 1
                if subreddit in top_subreddits:
                    top_subreddits[subreddit] = new_submissions[subreddit]['num']

            new_submissions[subreddit]['ids'].append(submission.id)
        else:
            new_submissions[subreddit] = dict()
            if has_dict and subreddit in popular_submissions.keys():
                num = popular_submissions[subreddit]['num']
                if subreddit in popular_submissions[subreddit]['ids']:
                    num += 1
                new_submissions[subreddit]['num'] = num
            else:
                new_submissions[subreddit]['num'] = 1

            if len(top_subreddits) < 10:
                top_subreddits[subreddit] = new_submissions[subreddit]['num']
            else:
                new_subreddit = (subreddit, new_submissions[subreddit]['num'])
                if new_subreddit not in top_subreddits:
                    compare_subreddit_val(top_subreddits, new_subreddit)
            new_submissions[subreddit]['ids'] = [submission.id]
    return new_submissions


def input_parsing():
    print("Search through: [subreddit | users | popular | posts | track post]")
    user_input = input()
    if user_input == 'subreddit':
        subreddit()
    elif user_input == 'users':
        users()
    elif user_input == 'posts':
        posts()
    elif user_input == 'track post':
        track_post()
    else:
        popular()


reddit = praw.Reddit(
    client_id='',
    client_secret='',
    user_agent='',
    username='',
    password=''
)
input_parsing()
