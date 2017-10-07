# Universal Turing Machine

Implementation of an universal turing machine in python.

![](turing.png)

## Usage
The machine reads a JSON file as instruction and processes the input accordingly.

```sh
# Multiplication
./turingmachine --instructions multiplication.json --input "00 000" -r -s .01
./turingmachine --instructions multiplication.json --input "00000000000000000" -r -s .01
./turingmachine --instructions multiplication.json --input "0000000000000000000000000 0" -r -s .01
./turingmachine --instructions multiplication.json --input "0000000000000 000000000000000000000000" -r -s .01
```

## JSON Encoding

### Interpretation

In a first step the JSON is read and converted into a Python dictionary containing all possible states and it’s corresponding instructions.
In a second step the Python dictionary (based on the JSON file) is validated and an exception is thrown, should the definition contain any errors (i.e. a state is referenced but never defined in the JSON).
In a third step the Python dictionary is used ad-hoc to find out (depending on the current state and the character at the current index of the Turing Machine):
* What should be written on the tape (can be any character)
* Which direction the tape should move (right or left)
* What new state the machine will be in (any state as defined in the JSON)

### Structure

```json
{
    "<state-name>": {
        "<character-action>": {
            "write": "<character-to-write>",
            "move": "<right|left>",
          	"nextState": "<state-name>"
        }
    }
}
```

## Author(s)

[Simon Breiter](mailto:hello@simonbreiter.com)  
[Emanuele Mazzotta](mailto:hello@mazzotta.me)

## Credits
[Swizec Teller](http://swizec.com/blog/a-turing-machine-in-133-bytes-of-javascript/swizec/3069)

## License

[MIT License](LICENSE.md) © Simon Breiter, Emanuele Mazzotta

