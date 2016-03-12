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
            'EndDate': '/Date(1441596445000-0500)/',
            'Effort': 0.0,
            'ResourceType': 'UserStory',
            'Team': {
                'Id': 298,
                'Name': 'DevOps',
            },
            'LastCommentDate': None,
            'CustomFields': [
                {
                    'Name': 'UI Spec',
                    'Type': 'RichText',
                    'Value': None
                },
                {
                    'Name': 'Date',
                    'Type': 'DropDown',
                    'Value': '/Date(1441596445000-0500)/'
                },
            ]
        }

        expected = {
            'EndDate': datetime(2015, 9, 7, 3, 27, 25, tzinfo=UTC),
            'Effort': 0.0,
            'ResourceType': 'UserStory',
            'Team': {
                'Id': 298,
                'Name': 'DevOps',
            },
            'LastCommentDate': None,
            'CustomFields': [
                {
                    'Name': 'UI Spec',
                    'Type': 'RichText',
                    'Value': None
                },
                {
                    'Name': 'Date',
                    'Type': 'DropDown',
                    'Value': datetime(2015, 9, 7, 3, 27, 25, tzinfo=UTC)
                },
            ]
        }
        result = TargetProcessSerializer().deserialize(data)
        self.assertEqual(result, expected)

    def test_deserialize_dict_with_items(self):
        data = {
            'Items': [
                {
                    'Date': '/Date(1441596445000-0500)/',
                    'NoneField': None,
                    'TextField': 'Text',
                    'NestedDict': {'Field': 'Value'},
                    'NestedList': [{'Field': 'Value'}]
                }
            ]
        }
        expected = [
            {
                'Date': datetime(2015, 9, 7, 3, 27, 25, tzinfo=UTC),
                'NoneField': None,
                'TextField': 'Text',
                'NestedDict': {'Field': 'Value'},
                'NestedList': [{'Field': 'Value'}]
            }
        ]

        result = TargetProcessSerializer().deserialize(data)
        self.assertEqual(result, expected)
