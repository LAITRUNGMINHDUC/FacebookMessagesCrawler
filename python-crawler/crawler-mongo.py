# Step 1:  
# Before running this script, please install 2 library
# pip install fbchat --- this is Facebook crawler - https://github.com/carpedm20/fbchat/
# pip install pymongo --- this is MongoDb driver

# Step 2: 
# Change the connection string of MongoDb at line 30 - You can use MongoDb for Free on Mlab.com

# Step 3: 
# Get ThreadId - Follow instruction in here: https://minhduclaitrung.files.wordpress.com/2018/03/getthreadid.png

# Step 4: Run it: python crawler-mongo.py <email> <password> <threadId>
# Example: python crawler-mongo.py laitrungminhduc@gmail.com Abc@123 1000011454789

import sys
import time
import re

from fbchat import Client
from fbchat.models import *
from pymongo import MongoClient


# Authenticate with Facebook
email = sys.argv[1]
password = sys.argv[2]
client = Client(email, password)

# Initialize MongoClient
clientMongo = MongoClient('<ConnectionString>')
dbMongo = clientMongo.facebook

threadId = sys.argv[3]

# Param: 
# - threadId: ThreadId that get from step 3
# - beforeTime: Get All messages from the past to beforeTime var
def getMessages(threadId, beforeTime=None): 

  messages = client.fetchThreadMessages(thread_id=threadId, limit=2000, before=beforeTime)
  beforeTime = int(messages[len(messages) - 1].timestamp)    
    
  editedArr = []

  # model of Message, you can see here: https://github.com/carpedm20/fbchat/blob/master/fbchat/models.py
  # View class Message:

  for message in messages: 
    editedArr.append({        
        "text": message.text,
        "timestamp": int(message.timestamp),        
        "author": message.author,
        "threadId": threadId      
      })         
            
  result = dbMongo.messages.insert(editedArr)  
  print str(dbMongo.messages.count({"threadId": threadId})) + " | " + str(beforeTime)  + ' | ' + messages[0].text           
  
  if (beforeTime > 0 and len(messages) > 1):
    getMessages(threadId, beforeTime)

getMessages(threadId)
client.logout()