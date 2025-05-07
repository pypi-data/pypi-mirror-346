from __future__ import annotations

import ctypes
import inspect
import multiprocessing
import threading
import time
import unittest
import unittest.mock
import unittest.mock
from abc import abstractmethod
from multiprocessing import Process, Value
from typing import Optional, Callable

from holytools.devtools.testing.result import SuiteResult, Report, CaseStatus
from .basetest import BaseTest
from .runner import Runner


# ---------------------------------------------------------

class Unittest(BaseTest):
    @classmethod
    def ready(cls) -> Unittest:
        instance = cls()
        instance.setUpClass()
        instance.setUp()
        return instance

    @classmethod
    def execute_all(cls, manual_mode : bool = True, trace_resourcewarning : bool = False):
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = Runner(logger=cls.get_logger(), is_manual=manual_mode, test_name=cls.__name__)
        tracemalloc_depth = 10 if trace_resourcewarning else 0
        results = runner.run(testsuite=suite, tracemalloc_depth=tracemalloc_depth)

        return results

    @classmethod
    def execute_stats(cls, reps : int, min_success_percent : float, test_names : Optional[list[str]] = None):
        if not 0 <= min_success_percent <= 100:
            raise ValueError(f'Min success percent should be in [0,100], got {min_success_percent}')

        test_names = test_names or unittest.TestLoader().getTestCaseNames(cls)
        stat_reports : list[Report] = []
        outcome_map : dict[str, list] = {}

        for tn in test_names:
            report_name = f'{cls.__name__}.{tn}'
            start_time = time.time()
            suite_result = cls._run_several(reps=reps, name=tn)
            runtime = round(time.time() - start_time, 3)

            outcomes = [True if c.status == CaseStatus.SUCCESS else False for c in suite_result.reports]
            outcome_map[report_name] = outcomes
            success_pc = 100*sum(outcomes) / len(outcomes)

            status = CaseStatus.SUCCESS if success_pc >= min_success_percent else CaseStatus.FAIL
            if suite_result.reports[0].status == CaseStatus.ERROR:
                status = CaseStatus.ERROR
            stats_report = Report(name=report_name, status=status, runtime=runtime)
            stat_reports.append(stats_report)

        result = SuiteResult(logger=cls.get_logger(), testsuite_name=cls.__name__)
        spaces = 13
        for c in stat_reports:
            outcomes = outcome_map[c.name]
            num_successful, total = sum(outcomes), len(outcomes)
            
            result.log_test_start(casename=c.name)
            status_arr = ['✓' if o else '✗' for o in outcomes]
            result.log(f'{"Result":<{spaces}}: {status_arr}')
            result.log(f'{"Success rate":<{spaces}}: {num_successful/total*100}%')
            result.log(msg=f'{"Status":<{spaces}}: {c.status}\n', level=c.get_log_level())

        result.reports = stat_reports
        result.log_summary()

    @classmethod
    def _run_several(cls, name : str, reps : int) -> SuiteResult:
        suite = unittest.TestSuite()
        current_case = cls(name)
        for _ in range(reps):
            suite.addTest(current_case)

        runner = Runner(logger=cls.get_logger(), test_name=cls.__name__)
        results = runner.run(testsuite=suite)

        return results

    @staticmethod
    def patch_module(original: type | Callable, replacement: type | Callable):
        module_path = inspect.getmodule(original).__name__
        qualified_name = original.__qualname__
        frame = inspect.currentframe().f_back
        caller_module = inspect.getmodule(frame)

        try:
            # corresponds to "from [caller_module] import [original]
            _ = getattr(caller_module, qualified_name)
            full_path = f"{caller_module.__name__}.{qualified_name}"
        except Exception:
            # corresponds to import [caller_module].[original]
            full_path = f"{module_path}.{qualified_name}"

        # print(f'Full path = {full_path}')
        def decorator(func):
            return unittest.mock.patch(full_path, replacement)(func)

        return decorator


class BlockedTester:
    def __init__(self):
        self.shared_bool = Value(ctypes.c_bool, False)

    def check_ok(self, case : str, delay : float) -> bool:
        def do_run():
            threading.Thread(target=self.blocked).start()
            time.sleep(delay)
            check_thread = threading.Thread(target=self.check_condition, args=(case,))
            check_thread.start()
            check_thread.join()
            q.put('stop')

        q = multiprocessing.Queue()
        process = Process(target=do_run)
        process.start()
        q.get()
        process.terminate()
        return self.shared_bool.value


    @abstractmethod
    def blocked(self):
        pass

    def check_condition(self, case : str):
        self.shared_bool.value = self.perform_check(case=case)

    @abstractmethod
    def perform_check(self, case : str) -> bool:
        pass

