import discord

class ShrimpBot(discord.Client):
    def __init__ (self):
        self.prefix = '새우야'

        super().__init__()

    async def on_ready(self):
        activity = discord.Activity(name='명령어: 새우야', type=discord.ActivityType.playing)
        await self.change_presence(activity=activity)
        print('Bot Started!')
    
    async def on_message(self, message):
        await self.wait_until_ready()

        if not message.author.bot:

            command = message.content.lower()
            if command.startswith('새우야'):
                await message.channel.send('안녕!')