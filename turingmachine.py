import json


class TuringMachine(object):
    def __init__(self, instructions, tape, end_state, current_state):
        self.instructions = instructions
        self.tape = tape
        self.end_state = end_state
        self.current_state = current_state

    def cycle(self):
        i = 0
        while self.current_state != self.end_state:
            if i < len(self.tape):
                current_cell = self.tape[i]
            else:
                current_cell = "B"
                self.tape.append("B")
            self.tape[i] = instructions[self.current_state][current_cell]["write"]
            i += instructions[self.current_state][current_cell]["move"]
            self.current_state = instructions[self.current_state][current_cell]["nextState"]
        return self.tape


if __name__ == '__main__':
    try:
        instructions = json.loads(open('instructions.json').read())
        print(TuringMachine(instructions, list("111"), "q5", "q0").cycle())
    except Exception as e:
        print("Looks like the .json-File is invalid!")

