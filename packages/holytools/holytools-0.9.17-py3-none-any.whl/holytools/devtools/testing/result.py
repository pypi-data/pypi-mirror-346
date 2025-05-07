from __future__ import annotations
from __future__ import annotations

import linecache
import logging
import os
import time
import traceback
import unittest
from dataclasses import dataclass
from typing import Optional
from unittest import TestCase, TestResult

from holytools.devtools.testing.basetest import BaseTest

# ---------------------------------------------------------

class SuiteResult(TestResult):
    test_spaces = 50
    status_spaces = 10
    runtime_space = 10

    def __init__(self, logger : logging.Logger,
                 testsuite_name: str,
                 manual_mode : bool = False,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.reports : list[Report] = []
        self.start_times : dict[str, float] = {}
        self.is_manual : bool = manual_mode
        self.testsuite_name = testsuite_name

    def startTestRun(self):
        super().startTestRun()
        self.log(self.get_header(f'  Test suite: \"{self.testsuite_name}\"  '))

    def startTest(self, case : BaseTest):
        super().startTest(case)
        self.on_case_start(case=case)

    def stopTestRun(self):
        self.log_summary()
        super().stopTestRun()

    # noinspection PyTypeChecker
    def addSuccess(self, case : BaseTest):
        super().addSuccess(case)
        self.on_case_finish(case, CaseStatus.SUCCESS)

    # noinspection PyTypeChecker
    def addError(self, case : BaseTest, err):
        super().addError(case, err)
        self.on_case_finish(case, CaseStatus.ERROR, err)

    # noinspection PyTypeChecker
    def addFailure(self, case : BaseTest, err):
        super().addFailure(case, err)
        self.on_case_finish(case, CaseStatus.FAIL, err)

    # noinspection
    def addSkip(self, case : BaseTest, reason):
        super().addSkip(case, reason)
        self.on_case_finish(case, CaseStatus.SKIPPED)

    # ---------------------------------------------------------
    # case reports

    def on_case_start(self, case : BaseTest):
        if self.is_manual:
            case.set_is_manual()
        self.log_test_start(casename=case.get_name())
        self.start_times[case.id()] = time.time()

    def on_case_finish(self, case : BaseTest, status: str, err : Optional[tuple] = None):
        report = Report(name=case.get_name(), status=status, runtime=self._get_runtime(case), err=err)
        self.log(msg=report.get_view(), level=report.get_log_level())
        self.reports.append(report)


    def _get_runtime(self, test : TestCase) -> Optional[float]:
        test_id = test.id()
        if test_id in self.start_times:
            time_in_sec =  time.time() - self.start_times[test_id]
            return round(time_in_sec, 3)
        else:
            self.log(msg=f'Couldnt find start time of test {test_id}. Current start_times : {self.start_times}',
                     level=logging.ERROR)

    # ---------------------------------------------------------
    # logging

    def log_summary(self):
        self.log(self.get_header(msg=' Summary ', seperator='-'))
        for case in self.reports:
            level = case.get_log_level()
            name_msg = f'{case.name[:self.test_spaces - 4]:<{self.test_spaces}}'
            status_msg = f'{case.status:<{self.status_spaces}}'
            runtime_str = f'{case.runtime}s'
            runtime_msg = f'{runtime_str:^{self.runtime_space}}'

            self.log(msg=f'{name_msg}{status_msg}{runtime_msg}', level=level)
        self.log(self.get_final_status())
        self.log(self.get_header(msg=''))


    def get_header(self, msg: str, seperator : str = '=') -> str:
        total_len = self.test_spaces + self.status_spaces
        total_len += self.runtime_space
        line_len = max(total_len- len(msg), 0)
        lines = seperator * int(line_len / 2.)
        return f'{lines}{msg}{lines}'


    def get_final_status(self) -> str:
        num_total = len(self.reports)
        unsuccessful_cases = [c for c in self.reports if c.status != CaseStatus.SUCCESS]
        num_unsuccessful = len(unsuccessful_cases)

        RED = '\033[91m'
        GREEN = '\033[92m'
        RESET = '\033[0m'
        CHECKMARK = '✓'
        CROSS = '❌'

        if num_unsuccessful == 0:
            final_status = f"{GREEN}\n{CHECKMARK} {num_total}/{num_total} tests ran successfully!{RESET}"
        else:
            final_status = f"{RED}\n{CROSS} {num_unsuccessful}/{num_total} tests had errors or failures!{RESET}"

        return final_status

    def log_test_start(self, casename : str):
        self.log(msg=f'------> {casename[:self.test_spaces]} ', level=logging.INFO)

    def log(self, msg : str, level : int = logging.INFO):
        self.logger.log(msg=msg, level=level)


@dataclass
class Report:
    runtime : float
    name : str
    status : str
    err : Optional[Exception] = None

    def get_log_level(self) -> int:
        status_to_logging : dict[str, int] = {
            CaseStatus.SUCCESS: logging.INFO,
            CaseStatus.ERROR: logging.CRITICAL,
            CaseStatus.FAIL: logging.ERROR,
            CaseStatus.SKIPPED : logging.INFO
        }
        return status_to_logging[self.status]


    def get_view(self) -> str:
        conditional_err_msg = f'\n{self._get_err_details(self.err)}' if self.err else ''
        return f'Status: {self.status}{conditional_err_msg}\n'


    @staticmethod
    def _get_err_details(err) -> str:
        err_class, err_instance, err_traceback = err
        tb_list = traceback.extract_tb(err_traceback)

        def is_relevant(tb):
            not_unittest = not os.path.dirname(unittest.__file__) in tb.filename
            not_custom_unittest = not os.path.dirname(__file__) in tb.filename
            return not_unittest and not_custom_unittest

        user_tb = [tb for tb in tb_list if is_relevant(tb)]

        result = ''
        relevant_tb = user_tb if not len(user_tb) == 0 else tb_list
        for frame in relevant_tb:
            file_path = frame.filename
            line_number = frame.lineno
            tb_str = (f'File "{file_path}", line {line_number}, in {frame.name}\n'
                      f'    {linecache.getline(file_path, line_number).strip()}')
            result += f'{err_class.__name__}: {err_instance}\n{tb_str}'
        return result


class CaseStatus:
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'
    FAIL = 'FAIL'
    SKIPPED = 'SKIPPED'
