import json
from datetime import datetime
from enum import Enum
from typing import Dict, List


class Constant:
    ID = 'id'
    CONTENT = 'content'
    RECORDS = 'records'
    LEVEL = 'level'
    DATE = 'date'
    STATUS = 'status'


class StatusEnum(str, Enum):
    NOT_STARTED = 'not started'
    PASS = 'pass'
    FAIL = 'fail'
    DONE = 'done'


class MemoryTrainer:

    def __init__(self) -> None:
        # {1: {'content': '1 + 1', 'records': ['level': 1, 'date': '20190101', 'status': 'pass']]}}
        self._training_log: Dict[str, Dict[str, str or List]] = {}

    @property
    def training_log(self):
        return self._training_log

    @classmethod
    def from_question_dict(cls, question_dict: Dict[str, str]) -> 'MemoryTrainer':
        trainer = cls()
        for _id, question in question_dict.items():
            trainer._training_log[_id] = {Constant.CONTENT: question, Constant.RECORDS: []}
        return trainer

    @classmethod
    def from_json_dump_file(cls, json_dump_file: str) -> 'MemoryTrainer':
        trainer = cls()
        with open(json_dump_file, 'r') as f:
            trainer._training_log = json.load(f)
        return trainer

    def persist_record(self, file: str):
        with open(file, 'w') as f:
            json.dump(self.training_log, f, indent=4)

    def upsert_record(self, _id: str, level: int, date: datetime, status: StatusEnum):
        # no record before
        if not self.training_log[_id][Constant.RECORDS]:
            self.training_log[_id][Constant.RECORDS].append(MemoryTrainer.build_record(level, date, status))
            return

        # already some records there
        data_new = date.strftime('%Y%m%d')
        last_one = self.training_log[_id][Constant.RECORDS][-1]
        if last_one[Constant.DATE] > data_new:
            raise ValueError(
                f"Time never goes back, can not change {data_new} while the last one is {last_one[Constant.DATE]}")

        if last_one[Constant.DATE] == data_new:
            last_one[Constant.LEVEL] = level
            last_one[Constant.STATUS] = status
        else:
            self.training_log[_id][Constant.RECORDS].append(MemoryTrainer.build_record(level, date, status))

    @staticmethod
    def build_record(level: int, date: datetime, status: StatusEnum):
        return {Constant.LEVEL: level, Constant.DATE: date.strftime('%Y%m%d'), Constant.STATUS: status}
