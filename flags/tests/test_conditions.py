from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest, QueryDict
from django.test import TestCase

from wagtail.wagtailcore.models import Site

from flags.conditions import (
    CONDITIONS,
    RequiredForCondition,
    register,
    get_condition,
    boolean_condition,
    user_condition,
    anonymous_condition,
    parameter_condition,
    path_condition,
    site_condition,
)


class ConditionRegistryTestCase(TestCase):

    def test_register_decorator(self):
        fn = lambda conditional_value: True
        register('decorated')(fn)
        self.assertIn('decorated', CONDITIONS)
        self.assertEqual(CONDITIONS['decorated'], [fn])

    def test_register_fn(self):
        fn = lambda conditional_value: True
        register('undecorated', fn=fn)
        self.assertIn('undecorated', CONDITIONS)
        self.assertEqual(CONDITIONS['undecorated'], [fn])

    def test_register_required_kwargs(self):
        pass

    def test_get_condition(self):
        fn = lambda conditional_value: True
        register('gettable', fn=fn)
        self.assertEqual(list(get_condition('gettable')), [fn])

    def test_get_condition_none(self):
        self.assertEqual(list(get_condition('notgettable')), [])


class BooleanConditionTestCase(TestCase):

    def test_boolean_condition_valid(self):
        self.assertTrue(boolean_condition(True))

    def test_boolean_condition_invalid(self):
        self.assertFalse(boolean_condition(False))

    def test_boolean_condition_valid_string(self):
        self.assertTrue(boolean_condition('True'))
        self.assertTrue(boolean_condition('true'))

    def test_boolean_condition_invalid_string(self):
        self.assertFalse(boolean_condition('False'))
        self.assertFalse(boolean_condition('false'))


class UserConditionTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='testuser',
                                        email='test@user')
        self.request = HttpRequest()
        self.request.user = user

    def test_user_valid(self):
        self.assertTrue(user_condition('testuser', request=self.request))

    def test_user_invalid(self):
        self.assertFalse(user_condition('nottestuser', request=self.request))

    def test_request_required(self):
        with self.assertRaises(RequiredForCondition):
            user_condition('testuser')


class AnonymousConditionTestCase(TestCase):

    def setUp(self):
        self.request = HttpRequest()

    def test_anonymous_valid(self):
        self.request.user = AnonymousUser()
        self.assertTrue(anonymous_condition(True, request=self.request))

    def test_anonymous_invalid(self):
        user = User.objects.create_user(username='notadminuser',
                                        email='test@user')
        self.request.user = user
        self.assertFalse(anonymous_condition(True, request=self.request))

    def test_request_required(self):
        with self.assertRaises(RequiredForCondition):
            anonymous_condition(True)


class ParameterConditionTestCase(TestCase):

    def setUp(self):
        self.request = HttpRequest()

    def test_parameter_condition_valid(self):
        self.request.GET = QueryDict('query_flag=True')
        self.assertTrue(parameter_condition('query_flag',
                                            request=self.request))

    def test_parameter_condition_invalid(self):
        self.request.GET = QueryDict('query_flag=False')
        self.assertFalse(parameter_condition('query_flag',
                                             request=self.request))

    def test_parameter_condition_non_existent(self):
        self.request.GET = QueryDict('not_query_flag=True')
        self.assertFalse(parameter_condition('query_flag',
                                             request=self.request))

    def test_request_required(self):
        with self.assertRaises(RequiredForCondition):
            parameter_condition('query_flag')


class PathConditionTestCase(TestCase):

    def setUp(self):
        self.request = HttpRequest()

    def test_path_condition_valid_exact(self):
        self.request.path = '/my/path'
        self.assertTrue(path_condition('/my/path', request=self.request))

    def test_path_condition_valid_subpath(self):
        self.request.path = '/my/path/to/somewhere'
        self.assertTrue(path_condition('/my/path', request=self.request))

    def test_path_condition_invalid(self):
        self.request.path = '/not/my/path'
        self.assertFalse(path_condition('/my/path', request=self.request))

    def test_request_required(self):
        with self.assertRaises(RequiredForCondition):
            path_condition('/my/path')


class SiteConditionTestCase(TestCase):

    def setUp(self):
        self.site = Site.objects.get(is_default_site=True)
        self.request = HttpRequest()
        self.request.site = self.site

    def test_site_valid_string(self):
        self.assertTrue(site_condition('localhost:80', request=self.request))

    def test_site_valid_string_no_port(self):
        self.assertTrue(site_condition('localhost', request=self.request))

    def test_site_valid_string_default_port(self):
        self.assertTrue(site_condition('localhost [default]',
                                       request=self.request))

    def test_site_valid_site(self):
        self.assertTrue(site_condition(str(self.site), request=self.request))

    def test_site_invalid_site(self):
        self.assertFalse(site_condition('non.existent.site',
                                        request=self.request))

    def test_request_required(self):
        with self.assertRaises(RequiredForCondition):
            site_condition('localhost:80')
