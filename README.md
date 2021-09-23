# RedditAnalytics
RedditAnalysis is a python script that does basic data gathering from Reddit.

# Features
* Analyze and find the most popular subreddits and what percentage they make up of traffic on Reddit
* Track popularity of posts over time by observing changes in upvotes and number of comments
<br/><br/>

# How To Use:
You need a Reddit account in order to operate this script.
- 1.)	Using pip, install Pandas and Matplotlib
- 2.) Download the CommandParse script and open it in an IDE, at the bottom of the code are sections asking for a username and password, set those items equal to your reddit username and password. Note that there are still two unused sections, client_id and client_secret. These will be discussed later.
- 3.)	Now you need to create an app in Reddit. Login to Reddit and then go to this link:https://www.reddit.com/prefs/apps/. Once you’re logged in, navigate to the “create an app” button and create a new script. Name and description can be anything of your choosing. An about URL is not required but a redirect URL is, use "ht<span>tp://</span>localhost:8888”.
- 4.)	Once the app is created, locate the app’s personal use script and secret id. These are the client_id and client_secret that was mentioned in step 1. Copy these down into the script
- 5.)	The script is now ready for use. Run it through an IDE like PyCharm or through the command line
<br/><br/>

# Planned Changes:
- Make the script easier to setup. Try to authenticate users without having to setup an app on Reddit
- Store data in a database rather than a pickle file
- For post tracking and monitoring data over time, streamline with Cron
- Automate tracking popular subreddits
<br/><br/>

If you have and suggestions, questions, or comments; please email me at kelvin.programming@gmail.com

