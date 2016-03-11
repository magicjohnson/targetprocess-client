# coding=utf-8
from datetime import datetime
import pytz


class TargetProcessSerializer(object):
    @classmethod
    def deserialize(cls, data):
        if isinstance(data, list):
            return [cls.deserialize(item) for item in data]

        if isinstance(data, dict):
            if 'Items' in data:
                return [cls.deserialize(item) for item in data['Items']]

            processed_item = {}
            for key, value in data.iteritems():
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
        return isinstance(value, basestring) and value.startswith('/Date')

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
