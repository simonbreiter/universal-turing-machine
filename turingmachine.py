import json
import argparse
import time
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description='Implementation of an universal Turing Machine.')
    requiredArguments = parser.add_argument_group('required arguments')
    requiredArguments.add_argument('-i', '--instructions', type=str, action="store", default=False, required=True, help='Instructions, as JSON file')
    requiredArguments.add_argument('-t', '--input', type=str, action="store", default=False, required=True, help='Input tape')
    parser.add_argument('-b', '--initial', type=str, action="store", default="q0", help='Initial state to begin')
    parser.add_argument('-r', '--render', action="store_true", default=False, help='Render turing machine')
    requiredArguments.add_argument('-e', '--end', type=str, action="store", default=False, required=True, help='End state')
    args = parser.parse_args()
    return args


class TuringMachine(object):
    def __init__(self, instructions, tape, start_state, end_state, render):
        self.instructions = instructions
        self.tape = list(tape)
        self.state = start_state
        self.end_state = end_state
        self.render = render

    def renderScreen(self, index):
        os.system('clear')
        print(str.join('', self.tape))
        print(''.ljust(index - 1, ' ') + '^')
        time.sleep(1)

    def validate_instruction(self):
        try:
            pass
        except Exception as e:
            print("The configuration you passed, contains invalid states")

    def run(self):
        self.validate_instruction()
        index = 0
        while self.state != self.end_state:
            if index < len(self.tape):
                cell = self.tape[index]
            else:
                cell = "B"
                self.tape.append("B")
            self.tape[index] = self.instructions[self.state][cell]["write"]
            index += self.instructions[self.state][cell]["move"]
            self.state = self.instructions[self.state][cell]["nextState"]
            if(self.render):
                self.renderScreen(index)
        return str.join('', self.tape)


def main():
    args = parse_arguments()
    instructions = json.loads(open(args.instructions).read())
    try:
        print("Input: {} \nOutput: {}".format(args.input, TuringMachine(instructions, args.input, args.initial, args.end, args.render).run()))
    except Exception as e:
        print("Looks like the .json-File is invalid!")


if __name__ == '__main__':
    main()
