import json

json_data = open('instructions.json').read()

instructions = json.loads(json_data)

def turingMachine(instructions, tape, endState, currentState):
    i = 0
    #Convert tape to list
    tape = list(tape)
    while currentState != endState:
        if i < len(tape):
            currentCell = tape[i]
        else:
            currentCell = "B"
            tape.append("B")
        tape[i] = instructions[currentState][currentCell]["write"]
        i += instructions[currentState][currentCell]["move"]
        currentState = instructions[currentState][currentCell]["nextState"]
    return tape

print(turingMachine(instructions, "111", "q5", "q0"))

