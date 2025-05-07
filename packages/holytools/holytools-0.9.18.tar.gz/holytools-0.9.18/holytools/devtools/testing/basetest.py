from __future__ import annotations

import logging
import unittest.mock
from typing import Optional

from holytools.logging import LoggerFactory


class BaseTest(unittest.TestCase):
    _logger: logging.Logger = None

    def __init__(self, *args):
        super().__init__(*args)
        self.is_manual_mode : bool = False

    def set_is_manual(self):
        self.is_manual_mode = True

    def get_is_manual(self):
        return self.is_manual_mode

    def get_name(self) -> str:
        full_test_name = self.id()
        parts = full_test_name.split('.')
        last_parts = parts[-2:]
        test_name = '.'.join(last_parts)
        return test_name

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if not cls._logger:
            cls._logger = LoggerFactory.get_logger(include_location=False, include_timestamp=False, name=cls.__name__, use_stdout=True, log_fpath=cls.log_fpath())
        return cls._logger


    @classmethod
    def log_fpath(cls) -> Optional[str]:
        return None

    @classmethod
    def log(cls, msg : str, level : int = logging.INFO):
        cls.get_logger().log(msg=f'{msg}', level=level)

    @classmethod
    def warning(cls, msg : str, *args, **kwargs):
        kwargs['level'] = logging.WARNING
        cls._logger.log(msg=msg, *args, **kwargs)

    @classmethod
    def error(cls, msg : str, *args, **kwargs):
        kwargs['level'] = logging.ERROR
        cls._logger.log(msg=msg, *args, **kwargs)

    @classmethod
    def critical(cls, msg : str, *args, **kwargs):
        kwargs['level'] = logging.CRITICAL
        cls._logger.log(msg=msg, *args, **kwargs)

    @classmethod
    def info(cls, msg : str, *args, **kwargs):
        kwargs['level'] = logging.INFO
        cls._logger.log(msg=msg, *args, **kwargs)


    # ---------------------------------------------------------
    # assertions

    def assertEqual(self, first : object, second : object, msg : Optional[str] = None):
        if not first == second:
            first_str = str(first).__repr__()
            second_str = str(second).__repr__()
            if msg is None:
                msg = (f'Tested expressions should match:'
                       f'\nFirst : {first_str} ({type(first)})'
                       f'\nSecond: {second_str} ({type(second)})')
            raise AssertionError(msg)

    def assertSame(self, first : dict, second : dict, msg : Optional[str] = None):
        """Checks whether contents of dicts first and second are the same"""
        for key in first:
            first_obj = first[key]
            second_obj = second[key]
            self.assertSameElementary(type(first_obj), type(second_obj))
            if isinstance(first_obj, dict):
                self.assertSame(first_obj, second_obj, msg=msg)
            elif isinstance(first_obj, list):
                for i in range(len(first_obj)):
                    self.assertSameElementary(first_obj[i], second_obj[i])
            else:
                self.assertSameElementary(first_obj, second_obj)

    def assertSameElementary(self, first : object, second : object):
        if isinstance(first, float) and isinstance(second, float):
            self.assertSameFloat(first, second)
        else:
            self.assertEqual(first, second)

    @staticmethod
    def assertSameFloat(first : float, second : float, msg : Optional[str] = None):
        if first != first:
            same_float = second != second
        else:
            same_float = first == second
        if not same_float:
            first_str = str(first).__repr__()
            second_str = str(second).__repr__()
            if msg is None:
                msg = (f'Tested floats should match:'
                       f'\nFirst : {first_str} ({type(first)})'
                       f'\nSecond: {second_str} ({type(second)})')
            raise AssertionError(msg)


    def assertIn(self, member : object, container, msg : Optional[str] = None):
        if not member in container:
            member_str = str(member).__repr__()
            container_str = str(container).__repr__()
            if msg is None:
                msg = f'{member_str} not in {container_str}'
            raise AssertionError(msg)


    def assertIsInstance(self, obj : object, cls : type, msg : Optional[str] = None):
        if not isinstance(obj, cls):
            obj_str = str(obj).__repr__()
            cls_str = str(cls).__repr__()
            if msg is None:
                msg = f'{obj_str} not an instance of {cls_str}'
            raise AssertionError(msg)


    def assertTrue(self, expr : bool, msg : Optional[str] = None):
        if not expr:
            if msg is None:
                msg = f'Tested expression should be true'
            raise AssertionError(msg)


    def assertFalse(self, expr : bool, msg : Optional[str] = None):
        if expr:
            if msg is None:
                msg = f'Tested expression should be false'
            raise AssertionError(msg)

