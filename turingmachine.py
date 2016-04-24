import json

json_data = open('instructions.json').read()

instructions = json.loads(json_data)


def turing_machine(instructions, tape, end_state, current_state):
    i = 0
    while current_state != end_state:
        if i < len(tape):
            current_cell = tape[i]
        else:
            current_cell = "B"
            tape.append("B")
        tape[i] = instructions[current_state][current_cell]["write"]
        i += instructions[current_state][current_cell]["move"]
        current_state = instructions[current_state][current_cell]["nextState"]
    return tape


print(turing_machine(instructions, list("111"), "q5", "q0"))
