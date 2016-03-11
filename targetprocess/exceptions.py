# coding=utf-8


class BadResponseError(Exception):
    def __init__(self, response):
        self.code = response.status_code
        self.content = response.content

    def __str__(self):
        return "Status Code {} \nContent:\n{}".format(self.code, self.content)
