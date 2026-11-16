"""
https://docs.telethon.dev/en/stable/concepts/entities.html
shows that each account contains a different 'access_hash'.
Therefore, only account usernames can be used

Limitations: The goal was to check 200 users, but after checking circa 100 users, the FloodWaitErrors occurred.
Therefore, only the results of the circa 100 checked usernames will be analyzed
"""

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.users import GetUsersRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.errors import FloodWaitError, ChannelPrivateError, rpcerrorlist
from telethon.tl import types
import time
import logging
from progress.bar import ChargingBar
import json
import sys
import csv
import asyncio

path = input("Path to the folder where the new file should be saved: ").strip().strip('"')
userlistpath = input("Path of the channel list (csv file): ").strip().strip('"')
analyzeType = input("What is being analyzed? Type '1' for Accounts or '2' for Channels, and start (with 'enter') the script: ")
if analyzeType != "1" or analyzeType != "2":
    print("The selected type does not exist")
    exit()

# initializing the Telegram Client
api_id =    # Integer
api_hash = ""

client = TelegramClient("anon", api_id, api_hash)

channelList = list()

# List of all accounts or channels to be investigated
def readCsvFile():
    with open(userlistpath, "r", encoding="utf-8", newline='') as f:
        read = csv.reader(f)
        for name in read:
            channelList.append(name[0])

# Obtain data via the API and save it in a JSON file
async def download_content_by_name(channelList):

    print('Number of accounts/channels to search: ', len(channelList))

    with ChargingBar('Downloading content', max=len(channelList)) as bar:
        filepath = path + "/collectDataTmp.json"    #File in which the data will be saved
        with open(filepath, "w", encoding="utf-8") as f:
            # Each account/channel is requested separately
            for channel in channelList:
                try:
                    # Returns all relevant data for more requests and also detailed information
                    #about the account/channel. Therefore, information about accounts needs only
                    #this request
                    data = await client.get_entity(channel)
                    if analyzeType == "2":
                        #"get_entity" returns the type of the object. Chats and channels have different types,
                        #whereby different request methods are executable
                        if type(data) is types.Chat:
                            fullData = await client(GetFullChatRequest(data))
                        elif type(data) is types.Channel:
                            fullData = await client(GetFullChannelRequest(data))
                        else: continue
                        
                except FloodWaitError as e:     # Error if the data access is restricted temporarily
                    print('Flood waited for', e.seconds)
                    await asyncio.sleep(e.seconds)
                    bar.next()
                    continue
                except ValueError as e:
                    print("\n", e)
                    bar.next()
                    continue
                except:
                    bar.next()
                    continue

                # Convert the collected data to JSON format and write it to the file
                if fullData:
                    data = fullData.to_dict()
                    f.write(json.dumps(data, ensure_ascii=False, default=str) + "\n")
                if data:
                    data = data.to_dict()
                    f.write(json.dumps(data, ensure_ascii=False, default=str) + "\n")

                await asyncio.sleep(0.2)    #minimize of FloodWaitError
                bar.next()

# Initalize the connection to Telegram
async def main():
    await client.start()
    if not await client.is_user_authorized():
        print("not authorized")
        sys.exit()

    client.flood_sleep_threshold = 60
    readCsvFile()
    if channelList:
        await download_content_by_name(channelList)

with client:
    client.loop.run_until_complete(main())