from typing import Set


def get_question_set() -> Set[str]:
    _result = set()
    for i in range(1, 20):
        for j in range(1, 20):
            if i + j <= 20:
                _result.add(f"{i} + {j}")
            if 0 < i - j < 20:
                _result.add(f"{i} - {j}")
    return _result


if __name__ == '__main__':
    print(get_question_set())
