from datetime import datetime
from unittest import TestCase

from memorytrainer import MemoryTrainer, StatusEnum


class TestMemoryTrainer(TestCase):
    @staticmethod
    def get_test_question_set():
        return {'1 + 1', '2 + 2', '3 + 3'}

    def setUp(self) -> None:
        super().setUp()
        self.question_set = TestMemoryTrainer.get_test_question_set()
        self.trainer = MemoryTrainer.from_question_set(self.question_set)

    def test_build_record(self):
        # given

        # when
        record = MemoryTrainer.build_record(3, datetime(2019, 1, 1), StatusEnum.FAIL)

        # then
        self.assertEqual(record, {'level': 3, 'date': '20190101', 'status': StatusEnum.FAIL})

    def test_from_question_set(self):
        # given
        # when
        # then
        for k in self.question_set:
            self.assertTrue(k in self.trainer.training_log.keys())

    def test_persist_load(self):
        # given
        self.trainer.upsert_record('1 + 1', 1, datetime(2019, 1, 1), StatusEnum.PASS)
        self.trainer.upsert_record('1 + 1', 1, datetime(2019, 1, 4), StatusEnum.NOT_STARTED)
        self.trainer.upsert_record('2 + 2', 1, datetime(2019, 2, 1), StatusEnum.FAIL)

        # when
        self.trainer.persist_record('atest.json')
        trainer2 = MemoryTrainer.from_json_dump_file('atest.json')

        # then
        self.assertDictEqual(self.trainer.training_log, trainer2.training_log)
