#!/usr/bin/env python3
# coding=utf-8

import json
import argparse

import time
import os

from config import Config
from utils import next_index, list_to_string, remove_empty_character, pipeify, count_occurrences


def parse_arguments():
    parser = argparse.ArgumentParser(description='A universal Turing machine (UTM) implementation in Python.')
    parser.add_argument('-b', '--begin', type=str, action='store', default='q0', help='Begin state')
    parser.add_argument('-e', '--end', type=str, action='store', default='qdone', help='End state')
    parser.add_argument('-s', '--speed', type=float, action='store', default=.3, help='Rendering speed in seconds')
    parser.add_argument('-r', '--render', action='store_true', default=False, help='Render turing machine')
    parser.add_argument('-a', '--interactive', action='store_true', default=False, help='Interactive mode.')
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-i', '--instructions', type=str, action='store', default=False, required=True, help='Instructions, as JSON file')
    required_args.add_argument('-t', '--tape', type=str, action='store', default=False, required=True, help='Input tape')
    return parser.parse_args()


class TuringMachine(object):
    def __init__(self, instructions, tape, start_state, end_state, render, speed, interactive):
        self.instructions = instructions
        self.tape = list(tape)
        self.state = start_state
        self.end_state = end_state
        self.activate_interactive = interactive
        self.activate_render = render
        self.speed = speed
        self.validate_instruction(self.instructions, self.end_state)

    def run(self):
        tape_index = 0
        steps_counter = 0
        self.render(tape_index, steps_counter, force_render=True)
        while self.state != self.end_state:
            steps_counter += 1
            tape_index = self.calculate_next_state(tape_index)
            self.render(tape_index, steps_counter)
        self.render(tape_index, steps_counter, force_render=True)
        return list_to_string(remove_empty_character(self.tape))

    def calculate_next_state(self, tape_index):
        if tape_index == -1:
            self.tape.insert(0, Config.empty_character())
            tape_index = 0
        if tape_index == len(self.tape):
            self.tape.append(Config.empty_character())
        action_for_current_state_and_cell = self.instructions[self.state][self.tape[tape_index]]
        self.tape[tape_index] = action_for_current_state_and_cell['write']
        self.state = action_for_current_state_and_cell['nextState']
        tape_index = next_index(tape_index, action_for_current_state_and_cell['move'])
        return tape_index

    def render(self, index, steps_counter, force_render=False):
        if self.should_render(force_render):
            empty, padding_end, padding_start, visible_length, visible_tape_section = self.tape_format_calc(index)
            self.print_system_clear()
            self.print_statistics(index, steps_counter)
            self.print_render_mode_information()
            self.print_tape(empty, padding_end, padding_start, visible_length, visible_tape_section)
            self.print_sign_occurrences()
            if self.activate_interactive:
                input()
            if self.speed:
                time.sleep(self.speed)

    def should_render(self, force_render):
        return self.activate_render or self.activate_interactive or force_render

    def print_system_clear(self):
        os.system('clear')

    def tape_format_calc(self, index):
        length = len(self.tape)
        visible_length = Config.visible_tape_length()
        empty = Config.empty_character()
        padding_start = visible_length - index
        padding_end = visible_length - (length - (index + 1))
        dynamic_start = index - visible_length if index >= visible_length else 0
        dynamic_end = length - (length - index - visible_length) if length - index > visible_length else length
        visible_tape_section = list_to_string(self.tape)[dynamic_start:dynamic_end]
        return empty, padding_end, padding_start, visible_length, visible_tape_section

    def print_sign_occurrences(self):
        print('Character Counter')
        for character, occurrence in count_occurrences(self.tape).items():
            print('{}x: {}'.format(occurrence, character))

    def print_tape(self, empty, padding_end, padding_start, visible_length, visible_tape_section):
        padding_icons = visible_length * 2 * '='
        print(padding_icons + '▼' + padding_icons)
        print(pipeify(padding_start * empty + visible_tape_section + padding_end * empty))
        print(padding_icons + '▲' + padding_icons)

    def print_render_mode_information(self):
        print('Render Mode')
        text_for_automatic_mode = 'X' if self.activate_render and not self.activate_interactive else ' '
        show_for_interactive_mode = ('X', '(Press enter to render next step...)')
        text_for_interactive_mode = (show_for_interactive_mode if self.activate_interactive else (' ', ' '))
        none_render_activated = not self.activate_interactive and not self.activate_render
        show_for_none_mode = ('X', '(Please wait for results...)')
        text_for_none_mode = (show_for_none_mode if none_render_activated else (' ', ' '))
        print('[{}] Automatic'.format(text_for_automatic_mode))
        print('[{}] Interactive {}'.format(text_for_interactive_mode[0], text_for_interactive_mode[1]))
        print('[{}] None {}'.format(text_for_none_mode[0], text_for_none_mode[1]))

    def print_statistics(self, index, steps_counter):
        print('Steps Counter {}'.format(str(steps_counter).rjust(7)))
        print('Current State {}'.format(self.state.rjust(7)))
        print('Tape Index {} '.format(str(index).rjust(10)))

    @staticmethod
    def validate_instruction(instructions, end_state):
        for instruction in instructions:
            for case in instructions[instruction]:
                action = instructions[instruction][case]
                if len(action['write']) != 1:
                    raise Exception('Invalid config! Use ONE character, instead of "{}"!'.format(action['write']))
                if action['move'] not in Config.allowed_tape_movements():
                    raise Exception('Invalid config! Use "right" or "left", not "{}"!'.format(action['move']))
                if action['nextState'] not in instructions and action['nextState'] != end_state:
                    raise Exception('Invalid config! State "{}" needs to be defined!'.format(action['nextState']))


def main():
    args = parse_arguments()
    try:
        instructions = json.loads(open(args.instructions).read())
        result = TuringMachine(instructions,
                               args.tape,
                               args.begin,
                               args.end,
                               args.render,
                               args.speed,
                               args.interactive).run()
        print()
        print('Input: {}'.format(args.tape))
        print('Output: {}'.format(result))
    except Exception as e:
        print('Something went wrong! Issue: {}'.format(e))


if __name__ == '__main__':
    main()
