# coding=utf-8
from unittest import TestCase

import mock
from requests import ConnectionError

from targetprocess.api import TargetProcessAPIClient
from targetprocess.exceptions import BadResponseError


class TargetProcessAPIClientTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.api = TargetProcessAPIClient('http://tp.api.url/api/v1', 'username', 'password')
        self.do_request_patcher = mock.patch.object(self.api, '_do_request', autospec=True)
        self.do_request_mock = self.do_request_patcher.start()
        self.addCleanup(self.do_request_patcher.stop)

        self.response = {'Items': [{'Id': 1}, {'Id': 2}]}
        self.do_request_mock.return_value = self.response

    def test_get_story_returns_story_by_id(self):
        self.assertEqual(self.api.get_story(8321), self.response)
        self.do_request_mock.assert_called_once_with(
            method='get',
            url="http://tp.api.url/api/v1/UserStories/8321?format=json"
        )

    def test_get_stories(self):
        response = self.api.get_stories(where="Team.Name eq 'Team X'")
        self.assertEqual(response, self.response)
        self.do_request_mock.assert_called_once_with(
            method='get',
            url="http://tp.api.url/api/v1/UserStories/?take=20&where=Team.Name+eq+%27Team+X%27&format=json",
        )

    def test_pagination(self):
        self.do_request_mock.side_effect = [
            {
                'Items': [{'Id': 3}, {'Id': 4}],
                'Next': 'http://tp.api.url/api/v1/UserStories/?take=20&skip=20&format=json'
            },
            self.response,
        ]

        response = self.api.get_stories()
        self.assertEqual(response['Items'], [{'Id': 3}, {'Id': 4}, {'Id': 1}, {'Id': 2}])
        self.assertSequenceEqual(
            self.do_request_mock.mock_calls, [
                mock.call(method='get', url="http://tp.api.url/api/v1/UserStories/?take=20&format=json"),
                mock.call(method='get', url="http://tp.api.url/api/v1/UserStories/?take=20&skip=20&format=json"),
            ]
        )

    def test_nested_pagination(self):
        response_with_next = {
            'Items': [
                {
                    'Id': 1,
                    'Nested': {
                        'Items': [{'Id': 3}],
                        'Next': 'http://tp.api.url/api/v1/UserStories/1/Nested/?take=25&skip=25',
                    }
                },
                {
                    'Id': 2,
                    'Nested': {
                        'Items': [{'Id': 3}],
                        'Next': 'http://tp.api.url/api/v1/UserStories/2/Nested/?take=25&skip=25',
                    }
                }
            ]
        }
        self.do_request_mock.side_effect = [
            response_with_next,
            self.response,
            self.response,
        ]

        response = self.api.get_stories()
        self.assertEqual(response, {
            'Items': [
                {
                    'Id': 1,
                    'Nested': {
                        'Items': [{'Id': 3}, {'Id': 1}, {'Id': 2}],
                        'Next': 'http://tp.api.url/api/v1/UserStories/1/Nested/?take=25&skip=25'
                    },
                },
                {
                    'Id': 2,
                    'Nested': {
                        'Items': [{'Id': 3}, {'Id': 1}, {'Id': 2}],
                        'Next': 'http://tp.api.url/api/v1/UserStories/2/Nested/?take=25&skip=25',
                    }
                },
            ]
        })
        expected_calls = [
            mock.call(method='get', url="http://tp.api.url/api/v1/UserStories/?take=20&format=json"),
            mock.call(method='get', url="http://tp.api.url/api/v1/UserStories/1/Nested/?take=25&skip=25&format=json"),
            mock.call(method='get', url="http://tp.api.url/api/v1/UserStories/2/Nested/?take=25&skip=25&format=json"),
        ]
        self.assertSequenceEqual(self.do_request_mock.mock_calls, expected_calls)

    def test_update_story(self):
        self.assertEqual(self.api.update_story(1234, {'data': 'xxx'}), self.response)
        self.do_request_mock.assert_called_once_with(
            method='post',
            url='http://tp.api.url/api/v1/UserStories/1234?include=%5BId%5D&format=json',
            data='{"data": "xxx"}',
            headers={'Content-type': 'application/json'},
        )


class APIClientDoRequestTest(TestCase):
    def setUp(self):
        self.requests_patcher = mock.patch('targetprocess.api.requests')
        self.requests_mock = self.requests_patcher.start()
        self.addCleanup(self.requests_patcher.stop)

        getattr = self.requests_mock.__getattribute__ = mock.MagicMock()
        self.method = getattr.return_value
        self.response = self.method.return_value
        self.response.status_code = 200
        self.response.json.return_value = {'Items': [{'Id': 1}, {'Id': 2}, {'Id': 3}]}
        self.api = TargetProcessAPIClient('http://tp.api.url/api/v1', 'username', 'password')

    def test_request_retry(self):
        self.method.side_effect = ConnectionError
        self.assertEqual(self.api.get_stories(), {})
        self.assertEqual(self.method.mock_calls, [
            mock.call(url='http://tp.api.url/api/v1/UserStories/?take=20&format=json', auth=self.api.auth),
            mock.call(url='http://tp.api.url/api/v1/UserStories/?take=20&format=json', auth=self.api.auth),
        ])

    def test_do_request_returns_response(self):
        response = self.api.get_stories()
        self.assertEqual(response, {'Items': [{'Id': 1}, {'Id': 2}, {'Id': 3}]})
        self.method.assert_called_once_with(
            url='http://tp.api.url/api/v1/UserStories/?take=20&format=json', auth=self.api.auth
        )

    def test_do_request_raises_bad_response(self):
        self.response.status_code = 400
        with self.assertRaises(BadResponseError):
            self.api.get_stories()

        self.method.assert_called_once_with(
            url='http://tp.api.url/api/v1/UserStories/?take=20&format=json', auth=self.api.auth
        )
