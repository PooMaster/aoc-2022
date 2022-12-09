"""
### Part 1:

--- Day 2: Rock Paper Scissors ---

The Elves begin to set up camp on the beach. To decide whose tent gets to be
closest to the snack storage, a giant Rock Paper Scissors tournament is already
in progress.
"""

from enum import Enum
from typing import NamedTuple, TextIO

# Rock Paper Scissors is a game between two players. Each game contains many
# rounds; in each round, the players each simultaneously choose one of Rock,
# Paper, or Scissors using a hand shape.


class Move(Enum):
    rock = 1
    paper = 2
    scissors = 3


class Round(NamedTuple):
    my_move: Move
    their_move: Move


# Then, a winner for that round is
# selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats
# Rock. If both players choose the same shape, the round instead ends in a draw.

winning_combos = {
    (Move.rock, Move.scissors),
    (Move.scissors, Move.paper),
    (Move.paper, Move.rock),
}

# Appreciative of your help yesterday, one Elf gives you an **encrypted strategy
# guide** (your puzzle input) that they say will be sure to help you win. "The
# first column is what your opponent is going to play: `A` for Rock, `B` for
# Paper, and `C` for Scissors. The second column--" Suddenly, the Elf is called
# away to help with someone's tent.

their_move_decode = {
    "A": Move.rock,
    "B": Move.paper,
    "C": Move.scissors,
}

# The second column, you reason, must be what you should play in response: `X`
# for Rock, `Y` for Paper, and `Z` for Scissors. Winning every time would be
# suspicious, so the responses must have been carefully chosen.

my_move_decode = {
    "X": Move.rock,
    "Y": Move.paper,
    "Z": Move.scissors,
}

# The winner of the whole tournament is the player with the highest score. Your
# **total score** is the sum of your scores for each round. The score for a
# single round is the score for the **shape you selected** (1 for Rock, 2 for
# Paper, and 3 for Scissors) plus the score for the **outcome of the round** (0
# if you lost, 3 if the round was a draw, and 6 if you won).


class RoundResult(Enum):
    loss = 0
    draw = 3
    win = 6


# Since you can't be sure if the Elf is trying to help you or trick you, you
# should calculate the score you would get if you were to follow the strategy
# guide.


def test_part1() -> None:
    """
    For example, suppose you were given the following strategy guide:

        A Y
        B X
        C Z

    This strategy guide predicts and recommends the following:
    """

    # > In the first round, your opponent will choose Rock (A), and you should
    #   choose Paper (Y). This ends in a win for you with a score of 8 (2
    #   because you chose Paper + 6 because you won).
    assert score_round(decode_round("A Y")) == 8

    # > In the second round, your opponent will choose Paper (B), and you should
    #   choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
    assert score_round(decode_round("B X")) == 1

    # > The third round is a draw with both players choosing Scissors, giving
    #   you a score of 3 + 3 = 6.
    assert score_round(decode_round("C Z")) == 6


"""
In this example, if you were to follow the strategy guide, you would get a total
score of `15` (8 + 1 + 6).

**What would your total score be if everything goes exactly according to your
strategy guide?**
"""

# === Part 1 Solution: ===


MoveDecoder = dict[str, Move]


def decode_round(
    round_str: str,
    their_move_decode: MoveDecoder = their_move_decode,
    my_move_decode: MoveDecoder = my_move_decode,
) -> Round:
    """
    Parse and decode the round info from a strategy guide line using the given
    move decoder tables.

        >>> decode_round("A Y")
        Round(my_move=<Move.paper: 2>, their_move=<Move.rock: 1>)
    """
    their_move_str, my_move_str = round_str.split()
    return Round(
        my_move=my_move_decode[my_move_str],
        their_move=their_move_decode[their_move_str],
    )


def decide_round(round: Round) -> RoundResult:
    """
    Return the result of the given RPS round.

        >>> decide_round(Round(their_move=Move.rock, my_move=Move.paper))
        <RoundResult.win: 6>
    """
    if (round.my_move, round.their_move) in winning_combos:
        return RoundResult.win

    if (round.their_move, round.my_move) in winning_combos:
        return RoundResult.loss

    return RoundResult.draw


def score_round(round: Round) -> int:
    """Return the total score given by this round."""
    return round.my_move.value + decide_round(round).value


def part1(input: TextIO) -> int:
    """
    Calculate the total score that would result if the given strategy guide
    was accurate.
    """
    return sum(score_round(decode_round(line.strip())) for line in input)


"""
### Part 2:

The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the
second column says how the round needs to end: `X` means you need to lose, `Y`
means you need to end the round in a draw, and `Z` means you need to win. Good
luck!"
"""

intended_result_decode = {
    "X": RoundResult.loss,
    "Y": RoundResult.draw,
    "Z": RoundResult.win,
}

"""
The total score is still calculated in the same way, but now you need to figure
out what shape to choose so the round ends as indicated.
"""


def test_part2() -> None:
    """The example above now goes like this:"""

    # > In the first round, your opponent will choose Rock (`A`), and you need
    #   the round to end in a draw (`Y`), so you also choose Rock. This gives
    #   you a score of 1 + 3 = **4**.
    assert score_round(decode_round_with_result("A Y")) == 4

    # > In the second round, your opponent will choose Paper (`B`), and you
    #   choose Rock so you lose (`X`) with a score of 1 + 0 = **1**.
    assert score_round(decode_round_with_result("B X")) == 1

    # > In the third round, you will defeat your opponent's Scissors with Rock
    #   for a score of 1 + 6 = **7**.
    assert score_round(decode_round_with_result("C Z")) == 7


"""
Now that you're correctly decrypting the ultra top secret strategy guide, you
would get a total score of **12**.

Following the Elf's instructions for the second column, **what would your total
score be if everything goes exactly according to your strategy guide?**
"""

# === Part 2 Solution: ===

"""
I decided to solve part 2 in a way that maximizes the reuse of work from part 1.
The parsing function knows the round result but throws it away since part 1's
round scoring function has to determine it anyway.
"""

ResultDecoder = dict[str, RoundResult]


def decode_round_with_result(
    strat_str: str,
    their_move_decode: MoveDecoder = their_move_decode,
    intended_result_decode: ResultDecoder = intended_result_decode,
) -> Round:
    """
    Parse and decode the move and result info from a strategy guide line and
    return the round that produces the intended result.
    """
    their_move_str, intended_result_str = strat_str.split()
    their_move = their_move_decode[their_move_str]
    intended_result = intended_result_decode[intended_result_str]

    # Consider every possible move and see which one achieves the intended
    # result
    for my_move in Move:
        considered_round = Round(my_move=my_move, their_move=their_move)
        if decide_round(considered_round) is intended_result:
            return considered_round

    raise RuntimeError("No moves lead to the intended result")


def part2(input: TextIO) -> int:
    """
    Calculate the total score that would result if the strategy guide was
    followed using the new interpretation.
    """
    return sum(score_round(decode_round_with_result(line.strip())) for line in input)


if __name__ == "__main__":
    # Print out part 1 solution
    with open("input.txt") as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with open("input.txt") as puzzle_input:
        print("Part 2:", part2(puzzle_input))
