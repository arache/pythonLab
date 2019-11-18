from datetime import datetime
from unittest import TestCase

from tests.test_memoryTrainer import TestMemoryTrainer

from memorytrainer import MemoryTrainer, StatusEnum
from memorymanager import MemoryManager


class TestMemoryManager(TestCase):
    def test_green(self):
        # given
        training_set = TestMemoryTrainer.get_test_training_set()
        trainer = MemoryTrainer.from_training_set(training_set)

        # when
        trainer.upsert_record('1 + 1', 1, datetime(2019, 1, 1), StatusEnum.PASS)
        trainer.upsert_record('1 + 1', 2, datetime(2019, 1, 4), StatusEnum.NOT_STARTED)

        manager = MemoryManager(trainer)
        manager.green('1 + 1', today=datetime(2019, 3, 1))
        manager.green('2 + 2', today=datetime(2019, 2, 1))

        # then
        last1 = trainer.training_log['1 + 1'][-1]
        last2 = trainer.training_log['1 + 1'][-2]
        self.assertDictEqual(last1, {'level': 3, 'date': '20190308', 'status': StatusEnum.NOT_STARTED})
        self.assertDictEqual(last2, {'level': 2, 'date': '20190104', 'status': StatusEnum.PASS})

        last1 = trainer.training_log['2 + 2'][-1]
        last2 = trainer.training_log['2 + 2'][-2]
        self.assertDictEqual(last1, {'level': 2, 'date': '20190204', 'status': StatusEnum.NOT_STARTED})
        self.assertDictEqual(last2, {'level': 1, 'date': '20190201', 'status': StatusEnum.PASS})

    def test_red(self):
        # given
        training_set = TestMemoryTrainer.get_test_training_set()
        trainer = MemoryTrainer.from_training_set(training_set)

        # when
        trainer.upsert_record('1 + 1', 1, datetime(2019, 1, 1), StatusEnum.PASS)
        trainer.upsert_record('1 + 1', 2, datetime(2019, 1, 4), StatusEnum.NOT_STARTED)

        manager = MemoryManager(trainer)
        manager.red('1 + 1', today=datetime(2019, 3, 1))
        manager.red('2 + 2', today=datetime(2019, 2, 1))

        # then
        last1 = trainer.training_log['1 + 1'][-1]
        last2 = trainer.training_log['1 + 1'][-2]
        self.assertDictEqual(last1, {'level': 1, 'date': '20190302', 'status': StatusEnum.NOT_STARTED})
        self.assertDictEqual(last2, {'level': 2, 'date': '20190104', 'status': StatusEnum.FAIL})

        last1 = trainer.training_log['2 + 2'][-1]
        last2 = trainer.training_log['2 + 2'][-2]
        self.assertDictEqual(last1, {'level': 1, 'date': '20190202', 'status': StatusEnum.NOT_STARTED})
        self.assertDictEqual(last2, {'level': 1, 'date': '20190201', 'status': StatusEnum.FAIL})

