from django.test import TestCase

from flags.conditions.registry import (
    DuplicateCondition,
    _conditions,
    get_condition,
    register,
)


class ConditionRegistryTestCase(TestCase):
    def test_register_decorator(self):
        fn = lambda conditional_value: True
        validator = lambda value: True
        register("decorated", validator=validator)(fn)
        self.assertIn("decorated", _conditions)
        self.assertEqual(_conditions["decorated"], fn)
        self.assertEqual(_conditions["decorated"].validate, validator)

    def test_register_fn(self):
        fn = lambda conditional_value: True
        validator = lambda value: True
        register("undecorated", fn=fn, validator=validator)
        self.assertIn("undecorated", _conditions)
        self.assertEqual(_conditions["undecorated"], fn)
        self.assertEqual(_conditions["undecorated"].validate, validator)

    def test_register_dup_condition(self):
        with self.assertRaises(DuplicateCondition):
            register("boolean", fn=lambda value: value)

    def test_register_decorator_dup_condition(self):
        with self.assertRaises(DuplicateCondition):
            register("boolean")(lambda value: value)

    def test_register_required_kwargs(self):
        pass

    def test_get_condition(self):
        fn = lambda conditional_value: True
        register("gettable", fn=fn)
        self.assertEqual(get_condition("gettable"), fn)

    def test_get_condition_none(self):
        self.assertEqual(get_condition("notgettable"), None)
