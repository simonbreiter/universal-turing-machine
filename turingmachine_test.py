from unittest import TestCase


class TuringMachineTest(TestCase):
    def test_that_invalid_configurations_are_caught(self):
        pass


invalid_conf = '''
    "q0": {
        "1": {
            "write": "B",
            "move": 1,
            "nextState": "q1"
        }
    },
'''
