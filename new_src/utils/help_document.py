from const import Docs


class HelpDocument:
    def __init__(self, command_finder, keyword):
        self.command_finder = command_finder
        self.keyword = keyword

    def __str__(self):
        return self.get_help_document()

    def get_help_document(self):
        command = self.get_command_by_keyword()
        try:
            help_document = getattr(Docs, command)
        except (TypeError, AttributeError):
            help_document = "그런 커맨드는 없네요 :("

        return help_document

    def get_command_by_keyword(self):
        if self.keyword is None:
            return "default"

        return self.command_finder.get_command(self.keyword, True)
