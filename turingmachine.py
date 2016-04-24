import json


class TuringMachine(object):
    def __init__(self, instructions, tape, end_state, start_state):
        self.instructions = instructions
        self.tape = tape
        self.end_state = end_state
        self.state = start_state

    def validate_instruction(self):
        for instruction in instructions:
            for case in instructions[instruction]:
                state_to_check = instructions[instruction][case]['nextState']
                if state_to_check not in instructions and state_to_check != self.end_state:
                    raise Exception("Invalid configuration, missing states")

    def run(self):
        self.validate_instruction()
        i = 0
        while self.state != self.end_state:
            if i < len(self.tape):
                cell = self.tape[i]
            else:
                cell = "B"
                self.tape.append("B")
            self.tape[i] = self.instructions[self.state][cell]["write"]
            i += self.instructions[self.state][cell]["move"]
            self.state = self.instructions[self.state][cell]["nextState"]
        return self.tape


if __name__ == '__main__':
    try:
        instructions = json.loads(open('instructions.json').read())
        print(TuringMachine(instructions, list("111"), "q5", "q0").run())
    except Exception as e:
        print("Looks like something went wrong! - %s" % e.message)
