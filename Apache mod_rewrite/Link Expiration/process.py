#!/usr/bin/python
import sys
import os
import time
import datetime
import shutil

# the number of times to allow a token through before expiring
valid_count=1

# this file is the list of approved tokens
authorized_user_file = '/var/expire/authusers.txt'

# visited 
spent_id_file = '/var/expire/used_ids.txt'

#log file
log_file = '/var/expire/process_log.txt'

auth_dict={}
spent_dict={}

#timestamp
def timestamp():
	ts =str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S%Z'))
	return ts

def filewrite(texttowrite,filetowriteto,mode):
	f = open(filetowriteto, mode)
	f.write(texttowrite)
	f.close()

#initialize the dictionaries for authorized and spent tokens and create the log if it doesn't exist
def initializeScript():
	#start log file if none, otherwise log start
	if os.path.isfile(log_file): 
		filewrite('[+] '+timestamp()+' - Processing script started.\n',log_file,"a")
	else: 
		filewrite('[+] '+timestamp()+' - Processing script started.\n',log_file,"w")	

	# open authorized_user_file and remove IDs that have already visited the link
	with open(authorized_user_file) as f:
	    authorized_tokens = f.read().splitlines()
	    for each in authorized_tokens:
	    	auth_dict[each]=0
	    filewrite('[*] '+timestamp()+' - Parsed the following authorized tokens from '+authorized_user_file+': '+str(authorized_tokens)+'\n',log_file,"a")

	if os.path.isfile(spent_id_file): 
		with open(spent_id_file) as f1:
			spent_id_lines = f1.read().splitlines()
			for each in spent_id_lines:
				spent_dict[each.split('\t')[0]]=each.split('\t')[1]
			filewrite('[*] '+timestamp()+' - Parsed the following spent token counts from '+spent_id_file+': '+str(spent_dict)+'\n',log_file,"a")
	else:
		filewrite('',spent_id_file,"w")
		filewrite('[*] '+timestamp()+' - No spent tokens found in '+spent_id_file+'\n',log_file,"a")

	# update authorized tokens with counts from spent ids
	for eachitem in authorized_tokens:
		if eachitem in spent_dict:
			auth_dict[eachitem]=int(spent_dict[eachitem])

#update the spent token file 
def updateSpent():
	#backup old file
	shutil.move(spent_id_file,spent_id_file+'~')

	#write new content
	filewrite('',spent_id_file,'w')
	for each in auth_dict.keys():
		filewrite(each+'\t'+str(auth_dict[each])+'\n',spent_id_file,'a')

	#delete backup
	os.remove(spent_id_file+'~')

# function to process the id token, returns "nftoken" if no match
def getRedirect(token):
	lookup_result = 'nftoken'
	if token not in auth_dict:
		filewrite('[*] '+timestamp()+' - Invalid token attempted: '+token+'\n',log_file,"a")
	elif auth_dict[token] < valid_count:
		lookup_result = token
		auth_dict[token] += 1
		updateSpent()
		filewrite('[+] '+timestamp()+' - Valid token used: '+token+' (access count: '+str(auth_dict[token])+')\n',log_file,"a")
		if auth_dict[token] >= valid_count:
			filewrite('[!] '+timestamp()+' - Token reached access limit: '+token+' (access count: '+str(auth_dict[token])+')\n',log_file,"a")
	elif auth_dict[token] >= valid_count:
		filewrite('[*] '+timestamp()+' - Spent token attempted: '+token+'\n',log_file,"a")
	return lookup_result


initializeScript()


#main function
while True:
	request = sys.stdin.readline().strip()
	response = getRedirect(request)
	if response:
		sys.stdout.write(response + '\n')
	else:
		sys.stdout.write('\n')
	sys.stdout.flush()

