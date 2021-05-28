import discord
from discord.ext import commands, tasks
import pymongo
from io import BytesIO
from pymongo import MongoClient


class BackUp(commands.Cog):
    def __init__(self, client):
        self.backupChannel = 847844294542622740
        self.cluster = MongoClient("mongodb+srv://dbBot:samarth1709@cluster0.moyjp.mongodb.net/"
                                   "myFirstDatabase?retryWrites=true&w=majority")
        self.backupCategory = 847064465730961438
        self.memeServer = 847058927341273119
        self.client = client
        self.backUpData.start()

    @tasks.loop(minutes=180)
    async def backUpData(self):
        await self.client.wait_until_ready()
        print("Starting logging.")
        memeServer = self.client.get_guild(self.memeServer)
        backupChannel = self.client.get_channel(self.backupChannel)
        categories = memeServer.categories
        category = None
        items = 0
        collection = self.cluster['MemeBackup']['Backup']
        data = collection.find_one({'_id': 0})
        for category in categories:
            if category.id == self.backupCategory:
                break

        for channel in category.text_channels:
            stopMessage = 0
            if str(channel.id) in data.keys():
                stopMessage = data[str(channel.id)] if data[str(channel.id)] is not None else 0
            msgId = None
            logged = True
            async for message in channel.history(limit=None):
                if logged:
                    msgId = message.id
                    logged = False
                if message.id == stopMessage:
                    print(message.id == stopMessage)
                    break
                if len(message.attachments):
                    for attachment in message.attachments:
                        temp = await attachment.read()
                        temp = BytesIO(temp)
                        file = discord.File(fp=temp, filename=attachment.filename)
                        await backupChannel.send(file=file)
                        items += 1

            data[str(channel.id)] = msgId
            collection.update_one({'_id': 0}, {'$set': {str(channel.id): data[str(channel.id)]}})

        print(f"Logged {items} item(s) successfully")


def setup(client):
    client.add_cog(BackUp(client))
