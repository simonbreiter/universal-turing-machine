#!/usr/bin/env python3
# coding=utf-8

import json
import argparse

import time
import os

from config import Config
from utils import get_next_index, list_to_string, remove_empty_character, insert_pipes_between_characters


def parse_arguments():
    parser = argparse.ArgumentParser(description='A universal Turing machine (UTM) implementation in Python.')
    parser.add_argument('-b', '--begin', type=str, action='store', default='q0', help='Begin state')
    parser.add_argument('-e', '--end', type=str, action='store', default='qdone', help='End state')
    parser.add_argument('-s', '--speed', type=float, action='store', default=.3, help='Rendering speed in seconds')
    parser.add_argument('-r', '--render', action='store_true', default=False, help='Render turing machine')
    parser.add_argument('-a', '--interactive', action='store_true', default=False, help='Interactive mode.')
    required_arguments = parser.add_argument_group('required arguments')
    required_arguments.add_argument('-i', '--instructions', type=str, action='store', default=False, required=True, help='Instructions, as JSON file')
    required_arguments.add_argument('-t', '--tape', type=str, action='store', default=False, required=True, help='Input tape')
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
        steps_counter = 0
        index = 0

        self.render(index, steps_counter, render_override=True)

        while self.state != self.end_state:
            if index == -1:
                self.tape.insert(0, Config.empty_character())
                index = 0
            if index == len(self.tape):
                self.tape.append(Config.empty_character())

            steps_counter += 1
            cell = self.tape[index]
            action = self.instructions[self.state][cell]

            self.tape[index], self.state, index = (
                action['write'],
                action['nextState'],
                get_next_index(index, action['move'])
            )

            self.render(index, steps_counter)

        self.render(index, steps_counter, render_override=True)
        return list_to_string(remove_empty_character(self.tape))

    def render(self, index, steps_counter, render_override=False):
        if self.activate_render or self.activate_interactive or render_override:
            length = len(self.tape)
            padding_start = Config.visible_tape_length() - index
            padding_end = Config.visible_tape_length() - (length - (index + 1))
            dynamic_start = index - Config.visible_tape_length() if index >= Config.visible_tape_length() else 0
            dynamic_end = length - (
            length - index - Config.visible_tape_length()) if length - index > Config.visible_tape_length() else length
            os.system('clear')
            print('Steps Counter {}'.format(str(steps_counter).rjust(7)))
            print('Current State {}'.format(self.state.rjust(7)))
            print('Tape Index {} '.format(str(index).rjust(10)))
            print('Render Mode')
            print('[{}] Automatic'.format('X' if self.activate_render and not self.activate_interactive else ' '))
            print('[{}] Interactive (Press enter to render next step...)'.format(
                'X' if self.activate_interactive else ' '))
            print('[{}] None (Please wait for results...)'.format(
                'X' if not self.activate_interactive and not self.activate_render else ' '))
            print(Config.visible_tape_length() * 2 * '=' + '▼' + Config.visible_tape_length() * 2 * '=')
            print(insert_pipes_between_characters(padding_start * ' ' + list_to_string(self.tape)[dynamic_start:dynamic_end] + padding_end * ' '))
            print(Config.visible_tape_length() * 2 * '=' + '▲' + Config.visible_tape_length() * 2 * '=')
            print('Character Counter')
            for character, occurrence in self.get_character_occurrences(self.tape).items():
                print('{}x: {}'.format(occurrence, character))
            print()
            if self.activate_interactive:
                input()
            if self.speed:
                time.sleep(self.speed)

    @staticmethod
    def get_character_occurrences(tape):
        clean_tape = remove_empty_character(tape)
        occurrences = {character: 0 for character in clean_tape}
        for character in clean_tape:
            occurrences[character] += 1
        return occurrences

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
        print('Input: {}'.format(args.tape))
        print('Output: {}'.format(result))
    except Exception as e:
        print('Something went wrong! Issue: {}'.format(e))


if __name__ == '__main__':
    main()
