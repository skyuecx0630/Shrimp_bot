import os
import importlib
import discord

from const import Aliases, ShortenedAliases, Strings

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def get_class_name_by_file_name(file_name):
    file_name = "".join(file_name.split(".")[:-1])  # 확장자 지우기
    tokens = [token.capitalize() for token in file_name.split("_")]
    return "".join(tokens)


class CommandFinder:
    def __init__(self):
        self.prefix_list = Strings.prefix_list
        self.extensions = self.get_extensions()

    def get_extensions(self):
        extensions = os.listdir(os.path.join(BASE_DIR, "extensions"))

        extension_list = []

        for extension in extensions:
            if extension.endswith(".py"):
                module = importlib.import_module(
                    "extensions." + extension[:-3], "extensions"
                )

                try:
                    extension_list.append(
                        getattr(module, get_class_name_by_file_name(extension))
                    )
                except AttributeError:
                    continue
        return extension_list

    def get_command(self, keyword: str, prefixed: bool) -> (str):
        """키워드로 커맨드의 이름을 찾습니다

        Args:
            keyword (str): 커맨드를 찾을 키워드
            prefixed (bool): 커맨드 접두사 여부

        Returns:
            command (str): 키워드로 찾은 커맨드
            command (None): 키워드를 찾지 못했을 경우
        """
        dictionary = Aliases if prefixed else ShortenedAliases

        for key, value in dictionary.items():
            if keyword in value:
                return key

        return None

    def get_function(self, keyword: str, prefixed: bool = False):
        command = self.get_command(keyword, prefixed)

        for extension in self.extensions:
            try:
                func = getattr(extension, command)
            except (TypeError, AttributeError):
                continue
            return func

        return None

    def get_function_by_message(self, message: discord.Message):
        contents = message.content.lower().split()

        try:
            prefixed = contents[0] in self.prefix_list and len(contents) > 1
        except IndexError:
            # 이미지는 메시지로 인식하지 않음
            return

        keyword = contents[prefixed]

        return self.get_function(keyword, prefixed)
