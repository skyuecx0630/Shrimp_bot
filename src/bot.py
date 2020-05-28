import discord
import asyncio

from utils import TimeCalc, MenuParser
from const import Constants, Docs
from db_manager import DBManager

from models import Custom_commands


weekday_kor = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

def find_command(message, prefixed=True):
    dictionary = getattr(Constants, 'prefixed_command' if prefixed else 'command')

    for command, shorts in dictionary.items():
        if message in shorts:
            return command


class ShrimpBot(discord.Client):
    def __init__ (self):
        self.prefix = '새우야'
        self.color = 0xFF421A
        self.meal_parser = MenuParser()
        self.db_manager = DBManager()

        super().__init__()


    async def on_ready(self):
        activity = discord.Activity(name='명령어: 새우야', type=discord.ActivityType.playing)
        await self.change_presence(activity=activity)
        print('Bot Started!')
    

    async def on_message(self, message):
        await self.wait_until_ready()

        if not message.author.bot:
            contents = message.content.lower().split()

            try:
                prefixed = 1 if contents[0]==self.prefix and len(contents) > 1 else 0
            except IndexError:
                #이미지는 메시지로 인식하지 않음
                func = None
            else:
                command = contents[prefixed]

                func = getattr(self, "command_%s" % find_command(command, prefixed=prefixed), None)

            if func:
                await func(message)


    async def command_ping(self, message):
        await message.channel.send('안녕! :wave:')


    async def command_help(self, message):
        await message.channel.trigger_typing()

        contents = message.content.lower().split()
        title = '새우 봇 도움말'

        try:
            doc = getattr(Docs, "%s" % find_command(contents[2]), None)
            
            if doc:
                title += ' - %s' % contents[2]

            else:
                doc = '그런 명령어는 없네요 :('

        except IndexError:
            doc = getattr(Docs, 'helps')

        em = discord.Embed(
            title=title,
            description=doc,
            colour=self.color
        )

        await message.channel.send(embed=em)


    async def command_hungry(self, message):
        await message.channel.trigger_typing()
                
        year, month, day, weekday, time = TimeCalc.get_next_time()

        title = "%s년 %s월 %s일 %s %s밥" % (
            year, month, day, weekday_kor[weekday],
            ['아침', '점심', '저녁'][time]
        )

        menu = self.meal_parser.get_next_meal()

        em = discord.Embed(
            title=title,
            description=menu,
            colour=self.color
        )

        await message.channel.send(embed=em)


    async def command_invite_link(self, message):
        await message.channel.trigger_typing()

        link = discord.utils.oauth_url(
            (await self.application_info()).id,
            permissions=discord.Permissions(8)
        )

        em = discord.Embed(
            title="§§§ 새우 봇 초대 링크 §§§",
            description="새우 봇을 초대해 보세요!",
            url=link,
            colour=self.color
        )

        content = await message.channel.send(embed=em)
        await asyncio.sleep(15)

        try:
            await content.delete()
            await message.channel.send("새우가 도망갔어요!")
        except discord.errors.NotFound:
            pass


    async def command_custom(self, message):
        contents = message.content.split()

        features = {'추가' : '_add', '삭제' : '_delete'}

        try:
            getattr(self, 'custom' + features[contents[2]])(message)

        except IndexError:
            doc = getattr(Docs, 'custom')

            em = discord.Embed(
                title='새우 봇 도움말 - 커스텀',
                description=doc,
                colour=self.color
            )
            
            await message.channel.send('올바른 명령어가 아닙니다!', embed=em)


    async def command_custom_add(self, message, prefixed=False):
        await message.channel.trigger_typing()

        contents = message.content.split()
        command_index = 3 if prefixed else 1
        
        try:
            command = contents[command_index]
            output = " ".join(contents[command_index + 1:])
        
        except IndexError:
            doc = getattr(Docs, 'custom')

            em = discord.Embed(
                title='새우 봇 도움말 - 커스텀',
                description=doc,
                colour=self.color
            )
            
            await message.channel.send('올바른 명령어가 아닙니다!', embed=em)
        
        else:
            server = str(message.guild.id)
            author = str(message.author.id)
            custom = Custom_commands(server, author, command, output)

            self.db_manager.insert_row(custom)

            await message.channel.send('알겠습니다! :ok_hand:')
