from datetime import timedelta, datetime
from typing import Dict, Optional

from memorytrainer import MemoryTrainer, Constant, StatusEnum


class MemoryManager:
    def __init__(self, trainer: MemoryTrainer, rule: Optional[Dict[int, int]] = None) -> None:
        self.rule = rule if rule else {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}
        self.trainer = trainer

    def green(self, _id: str, today: datetime = datetime.now()):
        records = self.trainer.training_log[_id][Constant.RECORDS]

        if records:
            last = self.trainer.training_log[_id][Constant.RECORDS][-1]
            if last[Constant.STATUS] == StatusEnum.DONE:
                return
            if last[Constant.STATUS] == StatusEnum.NOT_STARTED:
                last[Constant.STATUS] = StatusEnum.PASS
                next_level = last[Constant.LEVEL] + 1
                next_date = today + timedelta(days=self.rule[next_level])
                self.trainer.upsert_record(_id, last[Constant.LEVEL] + 1, next_date, StatusEnum.NOT_STARTED)
            else:
                raise ValueError(f"It should not be in status of {last[Constant.STATUS]}")
        else:
            self.trainer.upsert_record(_id, 1, today, StatusEnum.PASS)
            next_date = today + timedelta(days=self.rule[2])
            self.trainer.upsert_record(_id, 2, next_date, StatusEnum.NOT_STARTED)

    def red(self, _id: str, today: datetime = datetime.now()):
        records = self.trainer.training_log[_id][Constant.RECORDS]

        if records:
            last = self.trainer.training_log[_id][Constant.RECORDS][-1]
            if last[Constant.STATUS] == StatusEnum.DONE:
                raise ValueError(f"{_id} is already done, can not apply fail")
            if last[Constant.STATUS] == StatusEnum.NOT_STARTED:
                last[Constant.STATUS] = StatusEnum.FAIL
                next_date = today + timedelta(days=self.rule[1])
                self.trainer.upsert_record(_id, 1, next_date, StatusEnum.NOT_STARTED)
            else:
                raise ValueError(f"It should not be in status of {last[Constant.STATUS]}")
        else:
            self.trainer.upsert_record(_id, 1, today, StatusEnum.FAIL)
            next_date = today + timedelta(days=self.rule[1])
            self.trainer.upsert_record(_id, 1, next_date, StatusEnum.NOT_STARTED)

    def get_question_list(self) -> Dict[str, str]:
        _result = {}
        for _id, question in self.trainer.training_log.items():
            _result[_id] = question[Constant.CONTENT]
        return _result

    def get_today_question_list(self) -> Dict[str, str]:
        _result = {}
        for _id, question in self.trainer.training_log.items():
            if not question[Constant.RECORDS]:
                _result[_id] = question[Constant.CONTENT]
                continue

            last = question[Constant.RECORDS][-1]
            if last[Constant.DATE] == datetime.now().strftime('%Y%m%d') and \
                    last[Constant.STATUS] == StatusEnum.NOT_STARTED:
                _result[_id] = question[Constant.CONTENT]

        return _result

    def get_history(self):
        return self.trainer.training_log

    def persist(self, file):
        self.trainer.persist_record(file)
