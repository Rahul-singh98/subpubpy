import re


class RegexDict(dict):
    """Utility class to integrate regular expression."""

    def __init__(self):
        super(RegexDict, self).__init__()

    def __getitem__(self, pattern):
        for k, v in self.items():
            if re.match(pattern, k):
                return v
        return None

    def get(self, pattern):
        return self.__getitem__(pattern)
