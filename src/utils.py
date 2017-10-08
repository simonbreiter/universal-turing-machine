from config import Config


def list_to_string(to_stringify):
    return str.join('', to_stringify)


def pipeify(string):
    return '|'.join(string[i:i + 1] for i in range(0, len(string)))


def next_index(index, direction):
    return index + Config.tape_movement_for(direction) if direction in Config.allowed_tape_movements() else index


def remove_empty_character(dirty_list):
    return [character for character in dirty_list if character != Config.empty_character()]


def count_occurrences(in_list):
    clean_list = remove_empty_character(in_list)
    occurrences = {character: 0 for character in clean_list}
    for character in clean_list:
        occurrences[character] += 1
    return occurrences
