"""
This code is a modified copy of "https://github.com/SystemsLab-Sapienza/TGDataset/blob/main/crawler.py"
The modifications changed the saving of data into a database to a local storage as a JSON file
"""

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.errors import FloodWaitError, ChannelPrivateError, rpcerrorlist
from telethon.tl import types
import time
import datetime
import logging
from progress.bar import ChargingBar
import json
import sys


# Initialize the Telegram Client
api_id = 
api_hash = ""

client = TelegramClient("anon", api_id, api_hash)

path = input("Path to the folder where the new file should be saved: ").strip().strip('"')

# Timestamps that specify the time period for data collection
# In this case, the time period is from today to the timestamp "offsets"
offsets = {"WesternJournal": 1659311560, "weltdergesundheitTV": 1659294102, "wirsindvielmehr": 1652823545,
           "tlgdoc": 1658221905, "tlstunnelinfo": 1658239067, "transfers_live": 1659287201}

# Return the ID type of a peer object
def get_peer_id(peer):
    if type(peer) is types.PeerChannel:
        return peer.channel_id, 'channel'
    if type(peer) is types.PeerUser:
        return peer.user_id, 'user'
    if type(peer) is types.PeerChat:
        return peer.chat_id, 'chat'
    
    return [None, None]


# Download the messages of a channel by username
async def download_content_by_name(channels, limit):

    # Start from the last checkpoint
    print('Number of channels to search: ', len(channels))

    with ChargingBar('Downloading content', max=len(channels)) as bar:
        for channel in channels:
            new_ch = {}     # Dicitonary that saves data temporarily
            offset = offsets[channel]
            # Creating the dataset file
            filepath = path + "/own_" + channel + ".json"
            with open(filepath, "w", encoding="utf-8") as f:

                try:
                    channel_peer = await client.get_input_entity(channel)
                    channel = channel_peer.channel_id
                    channel_connect = await client.get_entity(channel)
                    channel_title = channel_connect.title
                    n_subscribers = channel_connect.participants_count
                    creation_date = datetime.datetime.timestamp(channel_connect.date)
                    description = ''
                    username = ''
                    is_scam = False
                    verified = False

                    if type(channel_connect) is types.Channel:                                   
                        channel_full_info = None
                        try:
                            channel_full_info = await client(GetFullChannelRequest(channel=channel_connect))
                        except FloodWaitError as e:
                            print('Flood waited for', e.seconds)
                        description = channel_full_info.full_chat.about
                        username = channel_full_info.chats[0].username
                        is_scam = channel_full_info.chats[0].scam
                        n_subscribers = channel_full_info.full_chat.participants_count
                        verified = channel_connect.verified
                
                    media = {}
                    messages = {}

                    async for message in client.iter_messages(channel, limit = limit, offset_date=offset):

                        message_date = datetime.datetime.timestamp(message.date)
                        message_author = get_peer_id(message.from_id)[0]

                        is_forwarded = False
                        forwarded_from_id = None
                        forwarded_message_date = None
                        if message.forward: 
                            is_forwarded = True
                            forwarded_from_id = get_peer_id(message.forward.from_id)[0]
                            forwarded_message_date = datetime.datetime.timestamp(message.forward.date)

                        if message.text:
                            messages[message.id] = {'message':message.text, 'date': message_date, 'author': message_author, 
                                'is_forwarded':is_forwarded, 'forwarded_from_id':forwarded_from_id, 
                                'forwarded_message_date':forwarded_message_date}

                            time.sleep(0.00001)

                        if message.media and message.file:  
                            
                            if not (message.gif or message.sticker):
                                title = message.file.name

                                #file_id = message.file.id

                                #https://docs.telethon.dev/en/stable/modules/custom.html#telethon.tl.custom.file.File.id
                                # It no longer works! But .file returns photo or document. Therefore, we can use
                                #constructor "Photo" and "Document"
            
                                try:
                                    file_id = message.photo.id
                                except:
                                    try:
                                        file_id = message.document.id
                                    except: continue

                                file_ext = message.file.ext

                                media[message.id] = {'title': title, 'date': message_date, 'author': message_author, 'extension': file_ext,
                                'is_forwarded':is_forwarded, 'forwarded_from_id':forwarded_from_id, 'media_id':file_id,
                                'forwarded_message_date':forwarded_message_date}

                                time.sleep(0.00001)

                    new_ch = {'creation_date': creation_date, 'username': username, 'title': channel_title, 'description': description, 'scam': is_scam,
                        'text_messages': messages, 'generic_media': media, 'n_subscribers': n_subscribers, 'verified': verified}

                    f.write(json.dumps(new_ch) + "\n")

                    time.sleep(1) # Minimize of FloodWaitError
                                    
                            
                except FloodWaitError as e:
                    print('Flood waited for', e.seconds)
                except ChannelPrivateError:
                    print("Private channel")
                    logging.warning('error with this channel ' + str(channel))

                bar.next()


async def main():
    await client.start()

    if not await client.is_user_authorized():
        print("nicht authorisiert")
        sys.exit()
        """
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))
        """

    client.flood_sleep_threshold = 0

    # Channels that are investigated
    channels_to_find = ["WesternJournal", "weltdergesundheitTV", "wirsindvielmehr", "tlgdoc",
                        "tlstunnelinfo", "transfers_live"]

    if channels_to_find:
        await download_content_by_name(channels_to_find, 10000) # 1000 is number of collected messages

with client:
    client.loop.run_until_complete(main())