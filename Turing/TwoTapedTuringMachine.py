from Direction import *

BLANKS_TO_APPEND = 50


class TuringMachine2Tapes:
    """Store 2 tapes, first will hold the input, second is "empty"
    Delta here is of the form delta(q, a, b) = (q', a', d1, b', d2)"""
    tape1: list or None
    tape2: list or None

    def __init__(self, alphabet, states, start_state,
                 acc, rej, delta, tape_alphabet, blank):
        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.acc = acc
        self.rej = rej
        self.delta = delta
        self.tape_alphabet = tape_alphabet
        self.blank = blank
        self.tape_in = False
        self.verbose = False

    def __str__(self):
        return f"{self.alphabet=}, {self.states}, {self.start_state}," \
               f" {self.acc}, {self.rej}, {self.delta}," \
               f" {self.tape_alphabet}, {self.blank}"

    def place_tape(self, tape: list):
        self.tape1 = tape
        self.tape2 = [self.blank] * 2 * BLANKS_TO_APPEND
        self.tape_in = True

    def remove_tape(self):
        self.tape1 = None
        self.tape2 = None
        self.tape_in = False

    def set_verbose_output(self, boolean: bool):
        self.verbose = boolean

    def move_head(self, old_head_position: int, direction: Direction, which_head):
        # edge cases
        if old_head_position == 0 and direction == Direction.LEFT:
            # stay
            return old_head_position
        if old_head_position == len(self.tape1 if which_head == 1 else self.tape2) - 1 and direction == Direction.RIGHT:
            # pump with blanks
            if which_head == 1:
                self.tape1 = self.tape1 + [b] * BLANKS_TO_APPEND
            else:
                self.tape2 = self.tape2 + [b] * BLANKS_TO_APPEND

            # and allow movement
            return old_head_position + 1
        # regular cases
        if direction == Direction.RIGHT:
            return old_head_position + 1
        if direction == Direction.LEFT:
            return old_head_position - 1
        if direction == Direction.STAY:
            return old_head_position

    """Move both heads"""

    def move_heads(self, old1: int, d1: Direction, old2: int, d2: Direction):
        if self.tape_in:
            p1 = self.move_head(old1, d1, 1)
            p2 = self.move_head(old2, d2, 2)
            return p1, p2

        else:
            raise Exception("Turing machine failed to read (no tape).")

    def traverse_contained_tape(self):
        # set header to the first element in the tape:
        head1 = head2 = 0
        state = self.start_state
        # while
        while state not in {self.acc, self.rej}:
            if self.verbose:
                print(f"Reading: index(head1)={head1}, head1 ->"
                      f" {self.tape1[head1]}, index(head2)={head2}, head2 ->{self.tape2[head2]}, "
                      f"state = {('acc' if state == self.acc else 'rej' if state==self.rej else state)}")
            # perform op
            new_state, l1, d1, l2, d2 = self.turing_iteration(state, head1, head2)
            if self.verbose:
                print(f"Machine changed state to "
                      f"{('acc' if new_state == self.acc else 'rej' if new_state==self.rej else new_state)}")
                print(f"Head1: Changing letter to:"
                      f" {l1 = }, Moving: {d1}")
                print(f"Head2: Changing letter to:"
                      f" {l2 = }, Moving: {d2}\n")
            # replace tape letter with l
            self.tape1[head1] = l1
            self.tape2[head2] = l2
            # move header
            head1, head2 = self.move_heads(head1, d1, head2, d2)
            # change state
            state = new_state
        return state == self.acc

    def traverse_tape(self, tape: list, remove_tape_later=True):
        self.place_tape(tape)
        ret = self.traverse_contained_tape()
        if remove_tape_later:
            self.remove_tape()
        return ret

    def turing_iteration(self, state, head1, head2):
        # get letter at head
        letter1 = self.tape1[head1]
        letter2 = self.tape2[head2]
        # use delta
        s, l1, d1, l2, d2 = self.delta[state, letter1, letter2]
        # should really be LSD
        return s, l1, d1, l2, d2


if __name__ == '__main__':
    # the basic example I saw when I first learned about these (also, lol)
    # A two taped Turing machine that accepts palindromes
    S = Direction.STAY
    L = Direction.LEFT
    R = Direction.RIGHT
    lang = {'a', 'b'}
    states = {0, 1, 2, 3, 4, 5}
    rej = 4
    acc = 5
    start = 0
    b = ' '
    tape_lang = {'a', 'b', b, '#'}
    # man did it ever?
    delta = {
        (0, b, b): (acc, 'a', S, b, S),
        (0, 'a', b): (1, 'a', S, '#', R),
        (0, 'b', b): (1, 'b', S, '#', R),

        (1, 'a', b): (1, 'a', R, 'a', R),
        (1, 'b', b): (1, 'b', R, 'b', R),
        (1, b, b): (2, b, L, b, L),

        (2, 'a', 'a'): (2, 'a', S, 'a', L),
        (2, 'a', 'b'): (2, 'a', S, 'b', L),
        (2, 'b', 'a'): (2, 'b', S, 'a', L),
        (2, 'b', 'b'): (2, 'b', S, 'b', L),

        (2, 'a', '#'): (3, 'a', S, '#', R),
        (2, 'b', '#'): (3, 'b', S, '#', R),

        (3, 'a', 'a'): (3, 'a', L, 'a', R),
        (3, 'b', 'b'): (3, 'b', L, 'b', R),

        (3, 'b', 'a'): (rej, 'b', S, 'a', S),
        (3, 'a', 'b'): (rej, 'a', S, 'b', S),

        (3, 'a', b): (acc, 'a', S, b, S),
        (3, 'b', b): (acc, 'b', S, b, S),

    }

    m = TuringMachine2Tapes(lang, states, start, acc, rej, delta, tape_lang, b)
    word = 'aabbbaaa'
    m.set_verbose_output(True)
    x = m.traverse_tape([*word], remove_tape_later=False)
    print(f"Tapes after run: 1:"
          f" {''.join(m.tape1).strip(' ')}{''.join(['_']*3)},"
          f" 2: "
          f"{''.join(m.tape2).strip(' ')}{''.join(['_']*3)}")
    print(x)
