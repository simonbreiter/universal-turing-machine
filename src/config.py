ALLOWED_TAPE_MOVEMENTS = {'right': 1, 'left': -1}
EMPTY_CHARACTER = ' '
VISIBLE_TAPE_LENGTH = 20


class Config:
    @staticmethod
    def allowed_tape_movements():
        return ALLOWED_TAPE_MOVEMENTS.keys()

    @staticmethod
    def tape_movement_for(direction):
        return ALLOWED_TAPE_MOVEMENTS[direction]

    @staticmethod
    def empty_character():
        return EMPTY_CHARACTER

    @staticmethod
    def visible_tape_length():
        return VISIBLE_TAPE_LENGTH
