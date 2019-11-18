import json
from enum import Enum
from datetime import datetime
from typing import Set, Dict, List, Any


class Constant:
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
        # {question, ['level', 'date', 'status']}
        self._training_log: Dict[str, List[Dict[str, Any]]] = {}

    @property
    def training_log(self):
        return self._training_log

    @classmethod
    def from_question_set(cls, question_set: Set[str]) -> 'MemoryTrainer':
        trainer = cls()
        for question in question_set:
            trainer._training_log[question] = []
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

    def upsert_record(self, question: str, level: int, date: datetime, status: StatusEnum):
        # no record before
        if not self.training_log[question]:
            self.training_log[question].append(MemoryTrainer.build_record(level, date, status))
            return

        # already some records there
        data_new = date.strftime('%Y%m%d')
        last_one = self.training_log[question][-1]
        if last_one[Constant.DATE] > data_new:
            raise ValueError(
                f"Time never goes back, can not change {data_new} while the last one is {last_one[Constant.DATE]}")

        if last_one[Constant.DATE] == data_new:
            last_one[Constant.LEVEL] = level
            last_one[Constant.STATUS] = status
        else:
            self.training_log[question].append(MemoryTrainer.build_record(level, date, status))

    @staticmethod
    def build_record(level: int, date: datetime, status: StatusEnum):
        return {Constant.LEVEL: level, Constant.DATE: date.strftime('%Y%m%d'), Constant.STATUS: status}
