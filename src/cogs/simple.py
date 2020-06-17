import discord
from discord.ext import commands


class Simple(commands.Cog):
    @commands.command()
    async def ping(self, message):
        await message.channel.send("안녕! :wave:")

    """@command
    async def command_help(self, message, command=None):
        await message.channel.trigger_typing()

        msg = f"<@!{message.author.id}>"

        contents = message.content.lower().split()
        title = "새우 봇 도움말"

        if command:
            doc = getattr(Docs, find_command(command), None)
            title += f" - {command}"
            msg += " 올바른 명령어가 아닙니다!"

        else:
            try:
                doc = getattr(Docs, find_command(contents[2]), None)

                if doc:
                    title += f" - {contents[2]}"

                else:
                    doc = "그런 명령어는 없네요 :("

            except IndexError:
                doc = getattr(Docs, "helps")

        em = discord.Embed(title=title, description=doc, colour=self.color)

        await message.channel.send(msg, embed=em)

    async def command_hungry(self, message):
        await message.channel.trigger_typing()

        year, month, day, weekday, time = TimeCalc.get_next_time()
        meal_time = ["아침", "점심", "저녁"][time]

        title = f"{year}년 {month}월 {day}일 {weekday_kor[weekday]} {meal_time}밥"

        menu = self.meal_parser.get_next_meal()

        em = discord.Embed(title=title, description=menu, colour=self.color)

        await message.channel.send(embed=em)

    async def command_invite_link(self, message):
        await message.channel.trigger_typing()

        link = discord.utils.oauth_url(
            (await self.application_info()).id, permissions=discord.Permissions(8)
        )

        em = discord.Embed(
            title="§§§ 새우 봇 초대 링크 §§§",
            description="새우 봇을 초대해 보세요!",
            url=link,
            colour=self.color,
        )

        msg = await message.channel.send(embed=em)
        await asyncio.sleep(15)

        try:
            await msg.edit(content="새우가 도망갔어요!", suppress=True)
        except discord.errors.NotFound:
            pass"""


def setup(bot):
    bot.add_cog(Simple(bot))
