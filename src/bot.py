import discord
import asyncio
import os
from random import choice

from utils import TimeCalc, MenuParser
from const import Constants, Docs, Strings, Settings
from db_manager import DBManager

from models import Custom_commands


weekday_kor = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

def find_command(message, prefixed=True):
    dictionary = getattr(Constants, 'prefixed_command' if prefixed else 'command')

    for command, shorts in dictionary.items():
        if message in shorts:
            return command

def admin_only(func):
    async def wrapper(self, message):
        if message.author.id not in self.admin:
            await message.channel.send(Strings.ADMIN_ONLY)
            return
        else:
            return await func(self, message)
    return wrapper

class ShrimpBot(discord.Client):
    def __init__ (self, admin):
        self.prefix = '새우야'
        self.color = 0xFF421A
        self.admin = admin
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
                return
        
            command = contents[prefixed]

            func = getattr(self, "command_%s" % find_command(command, prefixed=prefixed), None)

            if func:
                await func(message)
            
            else:
                await self.command_custom_show(message)


    async def command_ping(self, message):
        await message.channel.send('안녕! :wave:')


    async def command_help(self, message, command=None):
        await message.channel.trigger_typing()

        msg = "<@!%d>" % message.author.id

        contents = message.content.lower().split()
        title = '새우 봇 도움말'

        if command:
            doc = getattr(Docs, find_command(command), None)
            title += ' - %s' % command
            msg += ' 올바른 명령어가 아닙니다!'

        else:
            try:
                doc = getattr(Docs, find_command(contents[2]), None)
                
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

        await message.channel.send(msg, embed=em)


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

        msg = await message.channel.send(embed=em)
        await asyncio.sleep(15)

        try:
            await msg.edit(content="새우가 도망갔어요!", suppress=True)
        except discord.errors.NotFound:
            pass


    async def command_custom(self, message):
        contents = message.content.split()

        features = {'추가' : '_add', '삭제' : '_delete', '목록' : '_list'}

        try:
            await getattr(self, 'command_custom' + features[contents[2]])(message, prefixed=True)

        except (IndexError, KeyError):
            await self.command_help(message, command='커맨드')


    async def command_custom_add(self, message, prefixed=False):
        contents = message.content.split()
        command_index = 3 if prefixed else 1
        
        try:
            command = contents[command_index]
            output = " ".join(contents[command_index + 1:])
            
            if not output:
                raise IndexError
            
            if find_command(command, prefixed=False):
                await message.add_reaction('\U0001F6AB')
                return

        except IndexError:
            await self.command_help(message, command='커맨드')

        else:
            server = str(message.guild.id)
            author = str(message.author.id)
            custom = Custom_commands(server, author, command, output)

            self.db_manager.insert_row(custom)

            await message.add_reaction("\U0001F44C")


    async def command_custom_show(self, message):
        contents = message.content.split()

        searched = self.db_manager.search_row(Custom_commands, 'command', contents[0])

        server = str(message.guild.id)
        server_commands = [command for command in searched if command.server == server]

        if server_commands:
            selected = choice(server_commands)
        
            await message.channel.send(selected.output)


    async def command_custom_delete(self, message, prefixed=False):
        contents = message.content.split()

        command_index = 3 if prefixed else 1
        try:
            searched = self.db_manager.search_row(Custom_commands, 'command', contents[command_index])
        
        except IndexError:
            await self.command_help(message, command='커맨드')

        else:
            if not searched:
                await message.add_reaction('\U00002753')

            server = str(message.guild.id)
            server_commands = [command for command in searched if command.server == server]

            if server_commands:
                for command in server_commands:
                    self.db_manager.delete_row(command)

                await message.add_reaction("\U0001F44C")


    async def command_custom_list(self, message, prefixed=False):
        await message.channel.trigger_typing()

        server = str(message.guild.id)
        searched = self.db_manager.search_row(Custom_commands, 'server', server)

        if not searched:
            await message.channel.send('이 서버엔 추가된 커맨드가 없네요!')
            return

        command_dict = {}

        for custom in searched:
            if custom.command in command_dict:
                command_dict[custom.command] += 1
            else:
                command_dict[custom.command] = 1
        
        title = "%s의 커맨드 목록" % message.guild.name
        description = "\n".join(["`%s`" % command for command in command_dict])

        em = discord.Embed(
            title=title,
            description=description,
            colour=self.color
        )

        await message.channel.send(embed=em)


    @admin_only
    async def command_system_reboot(self, message):
        await message.channel.send(':ok_hand:')
        
        if os.name == 'posix':
            os.system('sudo reboot')


    @admin_only
    async def command_get_update(self, message):
        if os.name == 'posix':
            os.chdir(Settings.SRC_DIRECTORY)
            data = os.popen('git pull origin master').read()
            
            em = discord.Embed(
                title='명령어 실행 결과!',
                description = data,
                colour = self.color
            )
            
            await message.author.send(embed=em)
    