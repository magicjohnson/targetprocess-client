# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class BadResponseError(Exception):
    """Exception that is supposed to be raised in case TP API returns anything except 200 response"""
    def __init__(self, response):
        self.code = response.status_code
        self.content = response.content

    def __str__(self):
        return "Status Code {} \nContent:\n{}".format(self.code, self.content)
