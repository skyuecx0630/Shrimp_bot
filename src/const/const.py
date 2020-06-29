class Strings:
    OWNERS_ONLY = "이 기능은 봇 관리자만 사용할 수 있습니다!"
    GUILD_ONLY = "이 기능은 서버에서만 사용할 수 있습니다!"
    prefix_list = ["새우야"]


ShortenedAliases = {
    "ping": ["안녕", "ㅎㅇ", "새우야"],
    "hungry": ["배고파", "qorhvk", "hungry", "ㅗㅕㅜㅎ교", "헝그리", "gjdrmfl"],
    "custom_add": ["새커추"],
    "custom_delete": ["새커삭"],
    "custom_list": ["새커목"],
}

Aliases = {
    "ping": ["ping", "안녕", "ㅎㅇ", "새우야"],
    "hungry": ["밥", "배고파", "qorhvk", "hungry", "ㅗㅕㅜㅎ교", "헝그리", "gjdrmfl"],
    "invite_link": ["초대"],
    "help": ["help", "도움말", "명령어"],
    "custom": ["커맨드", "커스텀"],
    "statistic": ["통계"],
    "ban_word": ["금지어"],
    "get_update": ["업데이트"],
    "restart_bot": ["재시작"],
    "get_log": ["로그"],
    "flush_channel": ["밀어버려"],
}

UpdateCommands = [
    ["git", "reset", "--hard", "origin/master"],
    ["git", "pull", "origin", "+master"],
    ["pip3", "install", "-r", "../requirements.txt"],
]
