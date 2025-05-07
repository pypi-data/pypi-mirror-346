import linecache
import os
import tracemalloc
import unittest
import unittest.mock
import warnings
from logging import Logger
from unittest import TestSuite

from .result import SuiteResult


# ----------------------------------------------

class Runner(unittest.TextTestRunner):
    def __init__(self, logger : Logger, test_name : str, is_manual : bool = False, mute : bool = False):
        super().__init__(resultclass=None)
        self.logger : Logger = logger
        self.manual_mode : bool = is_manual
        self.test_name : str = test_name
        self.mute : bool = mute

    def run(self, testsuite : TestSuite, tracemalloc_depth : int = 0) -> SuiteResult:
        if tracemalloc_depth > 0:
            tracemalloc.start(tracemalloc_depth)


        with warnings.catch_warnings(record=True) as captured_warnings:
            warnings.simplefilter("ignore")
            warnings.simplefilter("always", ResourceWarning)

            result = SuiteResult(logger=self.logger,
                                 testsuite_name=self.test_name,
                                 stream=self.stream,
                                 descriptions=self.descriptions,
                                 verbosity=2,
                                 manual_mode=self.manual_mode)
            result.startTestRun()
            testsuite(result)
            result.stopTestRun()
            result.printErrors()

        for warning in captured_warnings:
            if tracemalloc_depth > 0:
                print(f'- Unclosed resources:')
                print(Runner.warning_to_str(warning_msg=warning))
            else:
                self.logger.warning(msg=f'[Warning]: Unclosed resource: \"{warning.message}\."'
                                        f'Enable trace_resourcewarning to obtain object trace')

        warnings.simplefilter("ignore", ResourceWarning)
        if tracemalloc_depth > 0:
            tracemalloc.stop()

        return result

    @staticmethod
    def warning_to_str(warning_msg: warnings.WarningMessage) -> str:
        tb = tracemalloc.get_object_traceback(warning_msg.source)
        frames = list(tb)
        frames = [f for f in frames if Runner.is_relevant(frame=f)]

        result = ''
        for f in frames:
            file_path = f.filename
            line_number = f.lineno
            result += (f'File "{file_path}", line {line_number}\n'
                      f'    {linecache.getline(file_path, line_number).strip()}\n')
        return result

    @staticmethod
    def is_relevant(frame):
        not_unittest = not os.path.dirname(unittest.__file__) in frame.filename
        not_custom_unittest = not os.path.dirname(__file__) in frame.filename
        return not_unittest and not_custom_unittest


