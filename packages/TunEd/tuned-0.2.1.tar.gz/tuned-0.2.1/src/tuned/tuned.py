"""
Copyright (C) 2025 drd <drd.ltt000@gmail.com>

This file is part of TunEd.

TunEd is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

TunEd is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import random
import sys
from queue import Queue

from tuned.audio_analyzer import AudioAnalyzer


parser = argparse.ArgumentParser(prog='TunEd', description='Command line Tuner', epilog='')
parser.add_argument('--version', action='version', version='%(prog)s 0.2.1')
parser.add_argument('--verbose', '-v', action='count', default=0, help='Set verbosity level.')
parser.add_argument('--frequency', '-f', action='store', default=440, help='Set reference frequency.', type=int)
parser.add_argument('--display', '-d', action='extend', nargs='+', type=str, choices=['tuner', 'precision', 'frequency', 'signal_level', 'execution_time', 'egg'], help='Display detailed information.')

args = parser.parse_args()

VERBOSE = args.verbose
REF_FREQ = args.frequency
DISPLAY = args.display

default_display = ['tuner', 'precision', 'frequency', 'signal_level', 'execution_time']
to_display = DISPLAY if DISPLAY is not None else default_display

bold_char = '\033[1m'
default_color = '\033[0;0m'
color_dark_grey = '\033[38;2;67;70;75m'
color_green = '\033[38;2;0;255;0m'
color_red = '\033[38;2;255;0;0m'

gradients = {
        5: color_green,  # green
        10: '\033[38;2;63;192;0m',
        15: '\033[38;2;127;128;0m',
        20: '\033[38;2;192;63;0m',
        21: color_red  # red
    }

levels = ["▁", "▂", "▃", "▄", "▅", "▇", "█"]


def display_tuner(offset, note, octave):
    """
        ❱ ₋₄₅ │││││││││││┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃ G 1 │││││││││││││││││││││││││││││││││││││││││││││ ₊₄₅ ❰
    """
    abs_offset = abs(offset)

    if 0 <= abs_offset <= 5:
        color = gradients[5]
    elif 6 <= abs_offset <= 10:
        color = gradients[10]
    elif 11 <= abs_offset <= 15:
        color = gradients[15]
    elif 16 <= abs_offset <= 20:
        color = gradients[20]
    else:
        color = gradients[21]

    if abs_offset > 45:
        abs_offset = 45
    add = 45 - abs_offset
    left_offset = right_offset = 0
    right_add = left_add = 45
    l_arrow_color = l_max_color = r_max_color = r_arrow_color = color_dark_grey
    if offset < 0:
        left_offset = abs_offset
        right_offset = 0
        left_add = add
        right_add = 45
        l_arrow_color = color
        if offset >= 45:
            l_max_color = color
    elif offset > 0:
        left_offset = 0
        right_offset = abs_offset
        left_add = 45
        right_add = add
        r_arrow_color = color
        if offset <= -45:
            r_max_color = color

    l_arrow = f"{l_arrow_color}❱{default_color}"
    l_max = f"{l_max_color}₋₄₅{default_color}"

    l_offset = f"{color_dark_grey}{'│'*left_add:{left_add}}{color}{'┃'*left_offset:{left_offset}}{default_color}"
    r_offset = f"{color}{'┃'*right_offset:{right_offset}}{color_dark_grey}{'│'*right_add:{right_add}}{default_color}"

    c_note = f"{color}{note:2}{default_color}"
    c_octave = f"{color}{octave:1}{default_color}"

    r_max = f"{r_max_color}₊₄₅{default_color}"
    r_arrow = f"{r_arrow_color}❰{default_color}"

    d_tuner = f"{l_arrow:1} {l_max:3} {l_offset:45} {c_note:^2}{c_octave:>1} {r_offset:45} {r_max:3} {r_arrow:1}"

    return d_tuner


def display_output(sound):

    # datas
    magnitude = sound['magnitude']
    db = round(sound['magnitude_to_db'], 0)
    frequency = sound['frequency']
    phase = sound['phase']
    note = sound['note']
    octave = str(abs(sound['octave']))
    offset = sound['offset']
    execution_time = sound['execution_time']

    # infos
    d_tuner = f'{display_tuner(offset, note, octave):107}'
    d_precision = f'{offset:+5}¢'
    d_frequency = f'∿ {frequency:6}㎐'
    d_signal_level = f'{levels[int(abs(db//30))]} {db:6}㏈'
    d_phase = f'𝛗 {phase:3}㎭'
    d_exec = f'⧖ {execution_time:8}″'
    d_egg = f"{random.choice(list(gradients.values()))}{random.choice(list('🯅🯆🯇🯈')):^4}{default_color}"

    to_display_dict = {
        'tuner': d_tuner,
        'precision': d_precision,
        'frequency': d_frequency,
        'signal_level': d_signal_level,
        'execution_time': d_exec,
        'egg': d_egg
    }

    output = ""
    for d in to_display:
        output += f"[{to_display_dict[d]}]"

    return output


def tuned():
    try:
        q = Queue()
        aa = AudioAnalyzer(q, REF_FREQ)
        aa.start()
        print(f"{bold_char}@ {REF_FREQ}㎐{default_color}")

        while True:
            print("\r", display_output(q.get()), end='')

    except KeyboardInterrupt:
        print("\nExit.")
        aa.stop()
        aa.join()
        sys.exit()
