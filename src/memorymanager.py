from datetime import timedelta, datetime
from typing import Dict, Optional

from memorytrainer import MemoryTrainer, Constant, StatusEnum


class MemoryManager:
    def __init__(self, trainer: MemoryTrainer, rule: Optional[Dict[int, int]] = None) -> None:
        self.rule = rule if rule else {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}
        self.trainer = trainer

    def green(self, question: str, today: datetime = datetime.now()):
        records = self.trainer.training_log[question]

        if records:
            last = self.trainer.training_log[question][-1]
            if last[Constant.STATUS] == StatusEnum.DONE:
                return
            if last[Constant.STATUS] == StatusEnum.NOT_STARTED:
                last[Constant.STATUS] = StatusEnum.PASS
                next_level = last[Constant.LEVEL] + 1
                next_date = today + timedelta(days=self.rule[next_level])
                self.trainer.upsert_record(question, last[Constant.LEVEL] + 1, next_date, StatusEnum.NOT_STARTED)
            else:
                raise ValueError(f"It should not be in status of {last[Constant.STATUS]}")
        else:
            self.trainer.upsert_record(question, 1, today, StatusEnum.PASS)
            next_date = today + timedelta(days=self.rule[2])
            self.trainer.upsert_record(question, 2, next_date, StatusEnum.NOT_STARTED)

    def red(self, question: str, today: datetime = datetime.now()):
        records = self.trainer.training_log[question]

        if records:
            last = self.trainer.training_log[question][-1]
            if last[Constant.STATUS] == StatusEnum.DONE:
                raise ValueError(f"{question} is already done, can not apply fail")
            if last[Constant.STATUS] == StatusEnum.NOT_STARTED:
                last[Constant.STATUS] = StatusEnum.FAIL
                next_date = today + timedelta(days=self.rule[1])
                self.trainer.upsert_record(question, 1, next_date, StatusEnum.NOT_STARTED)
            else:
                raise ValueError(f"It should not be in status of {last[Constant.STATUS]}")
        else:
            self.trainer.upsert_record(question, 1, today, StatusEnum.FAIL)
            next_date = today + timedelta(days=self.rule[1])
            self.trainer.upsert_record(question, 1, next_date, StatusEnum.NOT_STARTED)
