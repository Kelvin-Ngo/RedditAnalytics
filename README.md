# RedditAnalytics
RedditAnalytics is a python script that does basic data gathering from Reddit.

# Features
* Analyze and find the most popular subreddits and what percentage they make up of traffic on Reddit
* Track popularity of posts over time by observing changes in upvotes and number of comments
<br/><br/>

# How To Use:
You need a Reddit account in order to operate this script.
- 1.)	Using pip, install Pandas and Matplotlib
- 2.) Download the CommandParse script and open it in an IDE, at the bottom of the code are sections asking for a username and password, set those items equal to your reddit username and password. Note that there are still two unused sections, client_id and client_secret. These will be discussed later.
- 3.)	Now you need to create an app in Reddit. Go to this: https://www.reddit.com/prefs/apps/ and login to Reddit. Once you’re logged in, navigate to the “create an app” button and create a new script. Name and description can be anything of your choosing. An about URL is not required but a redirect URL is, use "ht<span>tp://</span>localhost:8888”.
- 4.)	Once the app is created, locate the app’s personal use script and secret id. These are the client_id and client_secret that was mentioned in step 1. Copy these down into the script
- 5.)	The script is now ready for use. Run it through an IDE like PyCharm or through the command line
<br/><br/>

# Explaination on Each Choice in the Script:
#### subreddit ####
- subreddit will look through the specified subreddit and return the top 10 posts based on what the sort order you chosed
#### users ####
- will look through the specified user's account and return the user's submissions
#### popular ####
- Will gather the top 1000 posts in popular and aggregate them into a file. Will track the most popular subreddits on Reddit
#### posts ####
- will asked for an id of a reddit post and return the post's name, number of comments, and like ratio. The id of a reddit post is specified in the URL of that post in the format of:
http://<span></span>www<span></span>.reddit.com<span></span>/r/[subreddit]/comments/[id]/[post title]/
#### track posts ####
- will monitor the specified post's number of comments, number of upvotes, and upvote ratio based on the id entered. You can specifed the interval length it checks and how long to monitor the post
#### plot line graph ####
- if you have used track posts then you will have files in relation to the posts you tracked. plot line graph is used to plot this data onto a line graph.

# Planned Changes:
- Make the script easier to setup. Try to authenticate users without having to setup an app on Reddit
- Store data in a database rather than a pickle file
- For post tracking and monitoring data over time, streamline with Cron
- Automate tracking popular subreddits
<br/><br/>

If you have and suggestions, questions, or comments; please email me at kelvin.programming@gmail.com

