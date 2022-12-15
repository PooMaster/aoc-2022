import io
from itertools import dropwhile, pairwise, takewhile
import re
from typing import Iterable, Iterator, NamedTuple, TextIO


class Pos(NamedTuple):
    x: int
    y: int


class Sensor(NamedTuple):
    pos: Pos
    nearest_beacon: Pos


Range = tuple[int, int]


class RangeSet:
    """
    This class maintains a set of ranges. Each range is a contiguous block of
    integers, which are each specified by the first and last integer present in
    that block. The internal
    datastructure is kept simplified.

    For example:
    
    >>> RangeSet([(3, 5), (7, 8)])
    RangeSet([(3, 5), (7, 8)])

    >>> RangeSet([(3, 7), (5, 8)])
    RangeSet([(3, 8)])
    """

    def __init__(self, ranges: Iterable[Range]):
        self.ranges: list[Range] = []
        for r in ranges:
            self.add(r)

    def add(self, range: Range):
        """
        More subranges can be added with the .add() method.
        """
        assert range[0] <= range[1], f"Bad range :( {range}"
        self.ranges.append(range)
        self.ranges = list(self._simplify())

    def __eq__(self, other: "RangeSet"):
        return self.ranges == other.ranges

    def __len__(self) -> int:
        "Return the number of ints represented by this RangeSet"
        return sum(b - a + 1 for a, b in self.ranges)

    def __bool__(self) -> bool:
        return len(self) != 0

    def __iter__(self) -> Iterator[int]:
        for r in self.ranges:
            first, last = r
            yield from range(first, last + 1)

    def _simplify(self) -> Iterable[Range]:
        self.ranges.sort()

        # TODO check case of [1, 5], [1, 3]

        prev_range = self.ranges[0]
        for next_range in self.ranges[1:]:
            if prev_range[1] >= next_range[0] - 1:
                # The end of one range is at least touching the next range, so merge
                prev_range = prev_range[0], max(prev_range[1], next_range[1])
            else:
                # There is a proper gap now, so yield out this range
                yield prev_range
                prev_range = next_range

        yield prev_range

    def inverse_of(self, min_max_range: Range) -> "RangeSet":
        """
        Return the RangeSet that results from removing all of self's ranges from
        the min_max_range.
        """
        def inverse_ranges() -> Iterable[Range]:
            "Generate the ranges that come between all the others"
            if len(self.ranges) == 0:
                return min_max_range

            first_range = self.ranges[0]
            if first_range[0] > min_max_range[0]:
                yield min_max_range[0], min([min_max_range[1], first_range[0]])

            for range, next_range in pairwise(self.ranges):
                yield range[1] + 1, next_range[0] - 1

            last_range = self.ranges[-1]
            if last_range[1] < min_max_range[1]:
                yield max([last_range[1], min_max_range[0]]), min_max_range[1]

        def restrict_ranges(ranges) -> Iterable[Range]:
            def too_far_left(r: Range) -> bool:
                return r[1] < min_max_range[0]
            def not_too_far_right(r: Range) -> bool:
                return r[0] <= min_max_range[1]

            it = iter(ranges)
            unclipped_ranges = list(takewhile(not_too_far_right, dropwhile(too_far_left, it)))
            if not unclipped_ranges:
                return unclipped_ranges

            # Clip first range
            unclipped_ranges[0] = max(unclipped_ranges[0][0], min_max_range[0]), unclipped_ranges[0][1]

            # Clip last range
            unclipped_ranges[-1] = unclipped_ranges[-1][0], min(unclipped_ranges[-1][1], min_max_range[1]), 

            return unclipped_ranges

        return RangeSet(restrict_ranges(inverse_ranges()))


INT = r"-?\d+"
LINE_PATTERN = re.compile(fr"Sensor at x=({INT}), y=({INT}): closest beacon is at x=({INT}), y=({INT})")

def parse_sensors(input: TextIO) -> Iterable[Sensor]:
    for line in input:
        if m := LINE_PATTERN.match(line):
            sensor_x, sensor_y, beacon_x, beacon_y = m.groups()
            yield Sensor(Pos(int(sensor_x), int(sensor_y)), Pos(int(beacon_x), int(beacon_y)))


def manhattan_distance(pos1: Pos, pos2: Pos) -> int:
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)


def get_cover_set(sensors: list[Sensor], row: int):
    cover_set = RangeSet([])
    for sensor in sensors:
        cover_distance = manhattan_distance(sensor.pos, sensor.nearest_beacon)
        row_cover_radius = cover_distance - abs(sensor.pos.y - row)
        if row_cover_radius < 0:
            continue
        row_cover_range = (sensor.pos.x - row_cover_radius, sensor.pos.x + row_cover_radius)
        cover_set.add(row_cover_range)
    return cover_set


def count_covered_locations(sensors: list[Sensor], row: int):
    # For each sensor, find the range that it covered on the given row. Then
    # throw all of those into a RangeSet. Then use the RangeSet to quickly count
    # the number of positions covered by sensors.
    rset = get_cover_set(sensors, row)

    return len(rset)


def find_uncovered_positions(sensors: list[Sensor], x_range: Range, y_range: Range) -> Iterable[Pos]:
    for y in range(y_range[0], y_range[1] + 1):
        if y % 100000 == 0:
            print(y)
        cover_set = get_cover_set(sensors, y)
        uncovered_set = cover_set.inverse_of(x_range)
        for x in uncovered_set:
            yield Pos(x, y)


EXAMPLE_INPUT = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""


def test_part1():
    sensors = list(parse_sensors(io.StringIO(EXAMPLE_INPUT)))
    assert len(sensors) == 14

    assert manhattan_distance(sensors[6].pos, sensors[6].nearest_beacon) == 9

    assert RangeSet([(3, 7), (5, 8)]).ranges == [(3, 8)]
    assert RangeSet([(1, 5), (1, 3)]).ranges == [(1, 5)]

    assert count_covered_locations([Sensor(Pos(8, 7), Pos(2, 10))], 10) == 13


def test_part2():
    sensors = list(parse_sensors(io.StringIO(EXAMPLE_INPUT)))
    for pos in find_uncovered_positions(sensors, (0, 20), (0, 20)):
        print(pos)


def part1(input: TextIO) -> int:
    """
    From the given sensor input text, output the number of positions on row
    y=2000000 where a hidden beacon could possibly be found.
    """
    sensors = list(parse_sensors(input))
    covered_locations = count_covered_locations(sensors, 2000000)
    known_beacons = set(sensor.nearest_beacon for sensor in sensors)
    known_beacons_in_row = sum(1 for beacon in known_beacons if beacon.y == 2000000)
    return covered_locations - known_beacons_in_row


def part2(input: TextIO) -> int:
    """
    From the given sensor input text, output the number of positions on row
    y=2000000 where a hidden beacon could possibly be found.
    """
    frequency = 0
    sensors = list(parse_sensors(input))
    for pos in find_uncovered_positions(sensors, (0, 4000000), (0, 4000000)):
        frequency = pos.x * 4000000 + pos.y
        print(f"Maybe beacon at {pos} with frequency {frequency}")
    return frequency


if __name__ == "__main__":
    # Print out part 1 solution
    # test_part1()
    # test_part2()

    with open("input.txt") as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    with open("input.txt") as puzzle_input:
        print("Part 2:", part2(puzzle_input))
