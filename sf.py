
import praw
import time
import os
import re
import config

#Dict scraped from College Pandas Website 
mathDict = {0:800,1:790,2:780,3:770,4:750,5:740,6:730,7:720,8:710,9:710,10:700,11:690,12:670,13:660,14:660,15:650,16:640,17:630,18:620,19:610,20:600,21:590,22:590,23:580,24:570,25:560,26:550,27:540,28:530,29:530,30:520,31:510,32:510,33:510,34:500,35:490,36:480,37:470,38:460,39:450,40:440,41:420,42:410,43:400,44:390,45:3700,46:360,47:340,48:330,49:320,50:320,51:290,52:280,53:260,54:250,55:230,56:210,57:200,58:200}
englishDict = {0:40,1:39,2:38,3:37,4:36,5:35,6:34,7:34,8:33,9:32,10:32,11:31,12:30,13:30,14:29,15:28,16:28,17:27,18:26,19:26,20:26,21:25,22:25,23:24,24:23,25:23,26:22,27:21,28:21,29:20,30:19,31:19,32:18,33:17,34:16,35:16,36:16,37:15,38:14,39:13,40:13,41:12,42:11,43:10,44:10}
readingDict = {0:40,1:39,2:39,3:38,4:38,5:37,6:37,7:36,8:36,9:35,10:35,11:34,12:33,13:33,14:32,15:32,16:31,17:31,18:30,19:30,20:29,21:28,22:28,23:27,24:26,25:26,26:25,27:25,28:24,29:24,30:23,31:23,32:22,33:22,34:21,35:21,36:20,37:20,38:19,39:19,40:18,41:17,42:17,43:16,44:15,45:15,46:14,47:13,48:12,49:11,50:10,51:10,52:10}
def bot_login():
	print ("Loggin in...")
	r = praw.Reddit(client_id = config.clientID , 
			client_secret = config.client_secret, 
			username = config.username, 
			password = config.password, 
			user_agent = config.user_agent)
	print ("Logged in!")

	return r

def run_bot(r, comments_replied_to):

	for comment in r.subreddit('sat').comments():
		num_in_string = [int(s) for s in comment.body.split() if s.isdigit()]
		length_of_string = len(num_in_string)
			
		if length_of_string == 3:
			readingWrong = num_in_string[0]
			writingWrong = num_in_string[1]
			mathWrong = num_in_string[2]

			if "Predict my score" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me() and mathWrong <= 58 and writingWrong <= 44 and readingWrong <=52:
				print ("String with \"Predict\" found in comment " + comment.id)
				math_score =(mathDict[mathWrong])
				writing_score = (englishDict[writingWrong])
				reading_score = (readingDict[readingWrong])
				total_score = math_score + ((writing_score + reading_score) * 10)
				comment.reply("Your predicted score will be " + str(total_score) + " | Evidence-Based Reading and Writing:" + str(((writing_score + reading_score) * 10)) + " | Math:" + str(math_score))
				print ("Replied to comment " + comment.id)	
				comments_replied_to.append(comment.id)
			else:
				comments_replied_to.append(comment.id)

				
			with open ("comments_replied_to.txt", "a") as f:
				f.write(comment.id + "\n")		



	print ("Sleeping for 5 seconds...")
	#Sleep for 10 seconds...
	time.sleep(5)




def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = list(filter(None, comments_replied_to))

	return comments_replied_to

comments_replied_to = get_saved_comments()
print (comments_replied_to)

while True:
	r = bot_login()
	run_bot(r, comments_replied_to)
	#Logging in each time to prevent request timeout






