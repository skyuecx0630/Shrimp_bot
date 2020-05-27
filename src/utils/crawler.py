from schapi import SchoolAPI
from datetime import datetime, timedelta

class TimeCalc:
    @staticmethod
    def get_next_time(now=datetime.now()):
        """다음으로 조회할 급식의 시간을 반환합니다.

        :param now: 조회할 시간
        :type now: datetime
        :return: (year, month, day, time)
        :rtype: tuple
        """
        # 아침, 점심, 저녁 시간
        meal_time = [510, 810, 1170]

        for i in range(len(meal_time)):
            if (now.hour * 60 + now.minute) < meal_time[i]:
                return (now.year, now.month, now.day, now.weekday(), i)
        
        #금요일이면 다음날을 월요일로
        now += timedelta(days=3 if now.weekday==4 else 1)
    
        return (now.year, now.month, now.day, now.weekday(), 0)


class MenuParser:
    def __init__(self):
        self.api = SchoolAPI(SchoolAPI.Region.GWANGJU, 'F100000120')

    async def get_next_meal(self):
        meal = ["breakfast", "lunch", "dinner"]

        year, month, day, weekday, time = TimeCalc.get_next_time()
        menu = getattr((await self.api.get_monthly_menus_async(year, month))[day], meal[time])
        
        if menu:
            result = "\n".join(["- %s" % item for item in menu])
        else:
            result = '급식 정보를 불러올 수 없습니다.'

        return result

if __name__ == '__main__':
    p = MenuParser()
    print(p.get_next_meal())
