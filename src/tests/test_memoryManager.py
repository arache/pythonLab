from datetime import datetime
from unittest import TestCase

from memorymanager import MemoryManager
from memorytrainer import MemoryTrainer, StatusEnum
from tests.test_memoryTrainer import TestMemoryTrainer


class TestMemoryManager(TestCase):

    def setUp(self) -> None:
        self.question_dict = TestMemoryTrainer.get_test_question_dict()
        self.trainer = MemoryTrainer.from_question_dict(self.question_dict)

    def test_green(self):
        # given
        # when
        self.trainer.upsert_record('1', 1, datetime(2019, 1, 1), StatusEnum.PASS)
        self.trainer.upsert_record('1', 2, datetime(2019, 1, 4), StatusEnum.NOT_STARTED)

        manager = MemoryManager(self.trainer)
        manager.green('1', today=datetime(2019, 3, 1))
        manager.green('2', today=datetime(2019, 2, 1))

        # then
        last1 = self.trainer.training_log['1']['records'][-1]
        last2 = self.trainer.training_log['1']['records'][-2]
        self.assertDictEqual(last1, {'level': 3, 'date': '20190308', 'status': StatusEnum.NOT_STARTED})
        self.assertDictEqual(last2, {'level': 2, 'date': '20190104', 'status': StatusEnum.PASS})

        last1 = self.trainer.training_log['2']['records'][-1]
        last2 = self.trainer.training_log['2']['records'][-2]
        self.assertDictEqual(last1, {'level': 2, 'date': '20190204', 'status': StatusEnum.NOT_STARTED})
        self.assertDictEqual(last2, {'level': 1, 'date': '20190201', 'status': StatusEnum.PASS})

    def test_red(self):
        # given
        # when
        self.trainer.upsert_record('1', 1, datetime(2019, 1, 1), StatusEnum.PASS)
        self.trainer.upsert_record('1', 2, datetime(2019, 1, 4), StatusEnum.NOT_STARTED)

        manager = MemoryManager(self.trainer)
        manager.red('1', today=datetime(2019, 3, 1))
        manager.red('2', today=datetime(2019, 2, 1))

        # then
        last1 = self.trainer.training_log['1']['records'][-1]
        last2 = self.trainer.training_log['1']['records'][-2]
        self.assertDictEqual(last1, {'level': 1, 'date': '20190302', 'status': StatusEnum.NOT_STARTED})
        self.assertDictEqual(last2, {'level': 2, 'date': '20190104', 'status': StatusEnum.FAIL})

        last1 = self.trainer.training_log['2']['records'][-1]
        last2 = self.trainer.training_log['2']['records'][-2]
        self.assertDictEqual(last1, {'level': 1, 'date': '20190202', 'status': StatusEnum.NOT_STARTED})
        self.assertDictEqual(last2, {'level': 1, 'date': '20190201', 'status': StatusEnum.FAIL})

    def test_question_list(self):
        # given
        # when
        manager = MemoryManager(self.trainer)
        q_list = manager.get_question_list()

        # then
        self.assertDictEqual(q_list, self.question_dict)

    def test_today_list(self):
        # given
        # when
        self.trainer.upsert_record('1', 1, datetime(2019, 1, 1), StatusEnum.PASS)
        self.trainer.upsert_record('1', 2, datetime(2019, 1, 4), StatusEnum.NOT_STARTED)

        manager = MemoryManager(self.trainer)
        q_list = manager.get_today_question_list()

        # then
        target_list = {'2': '2 + 2', '3': '3 + 3'}

    def test_history(self):
        # given
        # when
        self.trainer.upsert_record('1', 1, datetime(2019, 1, 1), StatusEnum.PASS)
        self.trainer.upsert_record('1', 2, datetime(2019, 1, 4), StatusEnum.NOT_STARTED)

        manager = MemoryManager(self.trainer)
        history = manager.get_history()

        # then
        target_dict = {'1': {'content': '1 + 1',
                             'records': [{'level': 1, 'date': '20190101', 'status': StatusEnum.PASS},
                                         {'level': 2, 'date': '20190104', 'status': StatusEnum.NOT_STARTED}]},
                       '2': {'content': '2 + 2', 'records': []},
                       '3': {'content': '3 + 3', 'records': []}}
        self.assertDictEqual(history, target_dict)
