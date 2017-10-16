[![License](http://img.shields.io/:license-mit-blue.svg?style=flat)](LICENSE.md)

# Universal Turing Machine

A universal Turing machine (UTM) implementation in Python.

![Turing Machine Example](assets/img/turing.png)

## Video Example

[![asciicast](https://asciinema.org/a/8W5NtwgDWm9oS0muFXu39kxWJ.png)](assets/img/video_example.gif)

## Usage
The machine reads a JSON file as instruction and processes the input accordingly.

```sh
# Multiplication

# 2 * 3
./universal_turing_machine --instructions assets/instructions/multiplication.json \
    --tape "00 000" \
    --render \
    --speed 0.01
  
# 17 * 0
./universal_turing_machine --instructions assets/instructions/multiplication.json \
    --tape "00000000000000000" \
    --render \
    --speed 0.01

# 25 * 1
./universal_turing_machine --instructions assets/instructions/multiplication.json \
    --tape "0000000000000000000000000 0" \
    --render \
    --speed 0.01

# 13 * 24
./universal_turing_machine --instructions assets/instructions/multiplication.json \
    --tape "0000000000000 000000000000000000000000" \
    --render \
    --speed 0.01
```

## JSON Definition

### How it works

1. The JSON is read and converted into a Python dict containing all possible states and instructions.
2. The Python dict is validated and an exception is thrown, should the definition contain any errors (i.e. a state is referenced but never defined).
3. The Python dict is used ad-hoc to find out the following:

- What should be written on the tape (can be any character)
- Which direction the tape should move (right or left)
- What state the machine should switch to (any state as defined in the JSON)

### Structure

```json
{
    "<state-name>": {
        "<character-action>": {
            "write": "<character-to-write>",
            "move": "<right|left>",
            "nextState": "<next-state-name>"
        }
    }
}
```

### Structure Legend

* state-name: Any state name, usually q0, q1, etc.
* character-action: Define action if Turing machine reads this character
* character-to-write: ONE character to write at current index
* right|left: Which direction to move
* next-state-name: The state to use next

### Example

```json
{
    "q0": {
        " ": {
            "write": "1",
            "move": "right",
            "nextState": "q1"
        }
    },
    "q1": {
        " ": {
            "write": "0",
            "move": "left",
            "nextState": "q1"
        },
        "1": {
            "write": "0",
            "move": "left",
            "nextState": "qdone"
        }
    }
}
```

### Example Explanation

Assumptions: Initial state is q0 and end state is q1 (can be defined via program arguments)

If q0 detects an empty character it will write a one at its position, move to the right and switch to state q1.  
If q1 detects an empty character it will write a zero at its position, move to the left and switch to state q1.  
If q1 detects a one it will write a zero at its position, move to the left and switch to state qdone.  

Try it yourself!

```bash
./universal_turing_machine --instructions assets/instructions/readme_example.json \
    --begin q0 \
    --end qdone \
    --tape " " \
    --render \
    --speed 1
```

## Universal Turing Machine Explanation

The configuration `universal.json` allows you to input any other configuration directly on the tape.

### About the machine

The machine uses one tape where you need to put the configuration of your machine and the inputs for your machine. Input consists only of (0,1,' ')\* where the universal machine itself does use internally (0,1,a,b,c,d,e,' ',x,#)\*. This is mostly due to simplicity, the alpahbet could 'easily' be reduced to (0,1)\*.

### Restrictions

1. Your machine should not move more to the left then the initial input was. Otherwise you will overwrite your own configuraion, which is not somethingyou you would want to do!
    - This could be fixed by changing the configuration of `universal.json` to shift the output to the right if you get too close to the configuration.
    - Another fix would be to add a second tape, which only contains the input of your machine. This is a very common way to implement the universal Turing machine as it allows for more speed.
2. The machine is not foolproof. It's actually only tested with the following example and some very simple other machines.

### Configuration to put on the tape

1. The input is designed to be as simple as possible. I assume you have named all your states with integers >=1 and the transitions look something like this:

```javascript
"q1": {
    " ": {
        "write": " ",
        "move": "right",
        "nextState": "q1"
    },
    "0": {
        "write": " ",
        "move": "right",
        "nextState": "q2"
    }
}
```

2. Split the config so you have every transition on it's own

```javascript
"q1": {
    " ": {
        "write": " ",
        "move": "right",
        "nextState": "q1"
    }
},
"q1": {
    "0": {
        "write": " ",
        "move": "right",
        "nextState": "q2"
    }
}
```

3. Convert all values to the following values:
        
    | Rule | Example |
    | --- | --- |
    | `qX -> 0{X}` | `(q1 -> 0, q3 -> 000)`|
    |`'0' -> 0`||
    |`'1' -> 00`||
    |`' ' -> 000`||
    |`right -> 00`||
    |`left -> 0`||

    Note: if you use q0 as a valid state, you need to change from `qX -> 0{X}` to `qX -> 0{X+1}` otherwise the machine will not run!

4. Put the converted values together in the following order use `1` as separator:
    - Actual State
    - Symbol on the tape
    - New State
    - Symbol to write on the tape
    - Direction to move

```javascript
"q1": {
    " ": {
        "write": " ",
        "move": "right",
        "nextState": "q1"
    }
}
```
    will result in `01000101000100`

5. Concat all converted states using `11` as separator
6. Add `111` to the end of the configuration
7. Add your custom Input at the end
8. Let the machine run. (it may take a while to run)

## Multiplication Example Configuration for Universal Turing Machine

```bash
./universal_turing_machine --instructions assets/instructions/universal.json \
    --tape "010001001000100110101000100010011001000100000000000000010001001100101000100010011000100010000100010011000101000101001100001000100000000000000001000101100001010000010001001100000100010000001000100110000010100000101001100000010001000000010101100000010100000010100110000000100010000000010001011000000010100000001010110000000010001000000000010101100000000101000000000101011000000000100010000101001100000000010100000000010101100000000001000100000000000100010110000000000101000000000010101100000000000100010000000000000100010011000000000001010000000000001010110000000000001000101000100110000000000001010000000000001010110000000000000100010000000000000100010011000000000000010100000000000000100010011000000000000001010000000000000010001001100000000000000010100000000000000010001001100000000000000001000100000000000000000100010110000000000000000101000000000000000010001011000000000000000001010000000000000000010001011100 00" \
    --begin q1 \
    --end q82 \
    --render \
    --speed 0.01
```

## Author(s)

[Simon Breiter](mailto:hello@simonbreiter.com)    
[Emanuele Mazzotta](mailto:hello@mazzotta.me)  
Dave Moser  

## Credits
[Swizec Teller](http://swizec.com/blog/a-turing-machine-in-133-bytes-of-javascript/swizec/3069)
