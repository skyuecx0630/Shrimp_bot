import discord
from discord.ext import commands
import asyncio

from const import Docs
from utils import TimeCalc


weekday_kor = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]


class Basics:
    @staticmethod
    async def ping(message):
        await message.channel.send("안녕! :wave:")

    @staticmethod
    async def hungry(message):
        async with message.channel.typing():
            year, month, day, weekday, time = TimeCalc.get_next_time()
            meal_time = ["아침", "점심", "저녁"][time]

            title = f"{year}년 {month}월 {day}일 {weekday_kor[weekday]} {meal_time}밥"

            menu = self.meal_parser.get_next_meal()

            em = discord.Embed(title=title, description=menu, colour=self.color)

            await message.channel.send(embed=em)

    @staticmethod
    async def invite_link(message):
        async with message.channel.typing():
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
            pass
