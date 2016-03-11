# coding=utf-8


class BadResponseError(Exception):
    """Exception that is supposed to be raised in case TP API returns anything except 200 response"""
    def __init__(self, response):
        self.code = response.status_code
        self.content = response.content

    def __str__(self):
        return "Status Code {} \nContent:\n{}".format(self.code, self.content)
