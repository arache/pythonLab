import json
from abc import ABC
from typing import Dict

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

from memorymanager import MemoryManager
from memorytrainer import MemoryTrainer


def get_question_dict() -> Dict[str, str]:
    _result = {}
    count = 1
    for i in range(1, 20):
        for j in range(1, 20):
            if i + j <= 20:
                _result[str(count)] = f"{i} + {j}"
                count += 1
            if 0 < i - j < 20:
                _result[str(count)] = f"{i} - {j}"
                count += 1
    return _result


file = 'addition.json'

trainer = MemoryTrainer.from_json_dump_file(file)
manager = MemoryManager(trainer)


class BaseHandler(RequestHandler, ABC):

    def set_default_headers(self) -> None:
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


class QuestionHandler(BaseHandler, ABC):
    def get(self):
        path = self.request.path
        if path == "/questions/get":
            self.no_param()
        elif path == "/questions/today/get":
            self.today()
        elif path.startswith("/questions/green"):
            question = path.split('/')[-1]
            self.green(question)
        elif path.startswith("/questions/red"):
            question = path.split('/')[-1]
            self.red(question)

    def no_param(self):
        self.write(json.dumps(manager.get_question_list()))

    def today(self):
        self.write(json.dumps(manager.get_today_question_list()))

    def green(self, question):
        manager.green(question)
        manager.persist(file)
        self.write(f"green {question} OK")

    def red(self, question):
        manager.green(question)
        manager.persist(file)
        self.write(f"red {question} OK")


class HistoryHandler(BaseHandler, ABC):
    def get(self):
        self.write(json.dumps(manager.get_history()))


class NewHandler(BaseHandler, ABC):
    def get(self):
        global trainer, manager
        trainer = MemoryTrainer.from_question_dict(get_question_dict())
        manager = MemoryManager(trainer)
        manager.persist(file)
        self.write(manager.get_history())


if __name__ == '__main__':
    application = Application([
        (r'/questions/.*', QuestionHandler),
        (r'/history/get', HistoryHandler),
        (r'/new', NewHandler),
    ])
    application.listen(8888)
    IOLoop.current().start()
