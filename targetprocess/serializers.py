# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime

import pytz
from six import string_types


class TargetProcessSerializer(object):
    """
    de-serializes raw data.
    For collection removes redundant `Items` key and puts everything into root
    converts weird "json" timestamp format into python datetime object
    """
    @classmethod
    def deserialize(cls, data):
        if isinstance(data, list):
            return [cls.deserialize(item) for item in data]

        if isinstance(data, dict):
            if 'Items' in data:
                return [cls.deserialize(item) for item in data['Items']]

            processed_item = {}
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    processed_item[key] = cls.deserialize(value)
                elif cls._is_date(value):
                    processed_item[key] = cls._json_date_to_datetime(value)
                else:
                    processed_item[key] = value

            return processed_item

        return data

    @staticmethod
    def _is_date(value):
        return isinstance(value, string_types) and value.startswith('/Date')

    @staticmethod
    def _json_date_to_datetime(json_date):
        """
        Returns timestamp for a JSON date format
        """
        sign = json_date[-7]
        if sign not in '-+' or len(json_date) == 13:
            milli_secs = int(json_date[6:-2])
        else:
            milli_secs = int(json_date[6:-7])

        ts = milli_secs / 1000

        d = datetime.fromtimestamp(ts, tz=pytz.UTC)
        return d
