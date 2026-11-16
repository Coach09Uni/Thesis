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

# initializing the Telegram Client
api_id = 
api_hash = ""

client = TelegramClient("anon", api_id, api_hash)

channelList = list()

def readCsvFile():
    with open(userlistpath, "r", encoding="utf-8", newline='') as f:
        read = csv.reader(f)
        for name in read:
            channelList.append(name[0])


async def download_content_by_name(channelList, limit):

    # Start from the last checkpoint
    print('Number of users to search: ', len(channelList))

    with ChargingBar('Downloading content', max=len(channelList)) as bar:
        for channel in channelList:
            with open(f"{path}/{channel}.jsonl", "w", encoding="utf-8") as f:
                try:
                    entity = await client.get_entity(channel)
                except FloodWaitError as e:
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

                # Collect all obtainable messages from the channel 
                async for message in client.iter_messages(entity, limit=limit, offset_date=channelList[channel]):
                    if message:
                        data = message.to_dict()
                        f.write(json.dumps(data, ensure_ascii=False, default=str) + "\n")

            bar.next()


async def main():
    await client.start()

    if not await client.is_user_authorized():
        print("not authorized")
        sys.exit()

    # readCsvFile()
    client.flood_sleep_threshold = 60

    # Timestamps that specify the time period for data collection
    # In this case, the time period is from the timestamp "offsets" to today or the parameter "limit"
    channelList = {"pjwnews": 1567942333, "PROLIFEGANG": 1567869112, "chileanshitposts": 1567823352,
                   "EcoFascistCentral": 1567964084, "gay_trans_agenda": 1567908474, "radicalagenda": 1567991055}
    if channelList:
        await download_content_by_name(channelList, 1000) # 1000 is the maximum number of collected messages

with client:
    client.loop.run_until_complete(main())