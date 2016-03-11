# coding=utf-8
from datetime import datetime
from unittest import TestCase

from pytz import UTC

from targetprocess.serializers import TargetProcessSerializer


class TargetProcessSerializerTest(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_deserialize_dict(self):
        data = {
            u'EndDate': u'/Date(1441596445000-0500)/',
            u'Effort': 0.0,
            u'ResourceType': u'UserStory',
            u'Team': {
                u'Id': 298,
                u'Name': u'DevOps',
            },
            u'LastCommentDate': None,
            u'CustomFields': [
                {
                    u'Name': u'UI Spec',
                    u'Type': u'RichText',
                    u'Value': None
                },
                {
                    u'Name': u'Date',
                    u'Type': u'DropDown',
                    u'Value': u'/Date(1441596445000-0500)/'
                },
            ]
        }

        expected = {
            u'EndDate': datetime(2015, 9, 7, 3, 27, 25, tzinfo=UTC),
            u'Effort': 0.0,
            u'ResourceType': u'UserStory',
            u'Team': {
                u'Id': 298,
                u'Name': u'DevOps',
            },
            u'LastCommentDate': None,
            u'CustomFields': [
                {
                    u'Name': u'UI Spec',
                    u'Type': u'RichText',
                    u'Value': None
                },
                {
                    u'Name': u'Date',
                    u'Type': u'DropDown',
                    u'Value': datetime(2015, 9, 7, 3, 27, 25, tzinfo=UTC)
                },
            ]
        }
        result = TargetProcessSerializer().deserialize(data)
        self.assertEquals(result, expected)

    def test_deserialize_dict_with_items(self):
        data = {
            u'Items': [
                {
                    u'Date': u'/Date(1441596445000-0500)/',
                    u'NoneField': None,
                    u'TextField': u'Text',
                    u'NestedDict': {'Field': 'Value'},
                    u'NestedList': [{'Field': 'Value'}]
                }
            ]
        }
        expected = [
            {
                u'Date': datetime(2015, 9, 7, 3, 27, 25, tzinfo=UTC),
                u'NoneField': None,
                u'TextField': u'Text',
                u'NestedDict': {'Field': 'Value'},
                u'NestedList': [{'Field': 'Value'}]
            }
        ]

        result = TargetProcessSerializer().deserialize(data)
        self.assertEquals(result, expected)
