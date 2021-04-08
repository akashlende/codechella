# Deepfake Video Analysis and Reporting

Built a solution for classifying deepfake videos and presented it at <a href="https://codechella.splashthat.com/">#Codechella 2019</a>; 
a hackathon hosted by the twitter university. 

Deepfakes have garnered widespread attention for their uses in celebrity pornographic videos, revenge porn, fake news, hoaxes, and financial fraud. This has elicited responses from both industry and government to detect and limit their use. In the recent elections in the states, deepfake videos were spread on the social media which confused the thought process of common people. People viewing the posts/tweets on the social media deserve to know whether the information is true or false.

## What it does?

Our application classifies the videos in the tweets as deepfake or not.


## Screenshots of working demo

<img src="https://github.com/akashlende/DeepFake-Recognition-React/blob/master/readme/tweet_comment.png" width="45%" alt="Classification result comment" />


## How we built it?

1. Fetch the tweets using the Twitter API every 10-15 minutes.
2. Search and get the tweets that have video content.
3. Check if this tweet has already been analyzed by our bot.
4. If no, process the video using machine learning .
5. Return the result in the comments section of the Tweet using Twitter API.


## Technology Stack

1. Python
2. Data store
3. Twitter API
3. Machine Learning
4. EfficientNet B7


## Team Members

<a href="http://github.com/akashlende">Akash Lende</a>
<a href="http://github.com/rahulgrover99">Rahul Grover</a>
<a href="https://github.com/aSquare14">Atibhi Agrawal</a>

