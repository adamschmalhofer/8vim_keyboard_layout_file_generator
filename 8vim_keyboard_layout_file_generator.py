#!/usr/bin/env python3
# -------------------------------------------
# Copyright (C) <2020> <Simon Slater>
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
# -------------------------------------------


# Please run the script with the first argument being a text file with the layout information and it will output the keyboard_actions.xml file for you :).
# In the first line put your email address and it to be added when you go all the way around the board for the @ sign (for this to work make the @ 
# character in the same place for the upper and lower case). The next line contains the lower case layout; followed by a line with the upper case layout.
# See en_eight_pen_esperanto.txt for an example and the order of the characters as used by 8vim's default keyboard.


# -------------------
#    Program start
# -------------------

import sys
from itertools import chain, zip_longest
from os.path import splitext


def duo_colum(first, seccond, boarder_width=10):
    first_lines = [line.rstrip('\n\r') for line in first.splitlines()]
    seccond_lines = [line.rstrip('\n\r') for line in seccond.splitlines()]
    start_right_colum_at = max(len(line) for line in first_lines) + boarder_width

    for left, right in zip_longest(first_lines, seccond_lines, fillvalue=''):
        yield left.ljust(start_right_colum_at) + right


# Passed a string of just letters and will map that to the layout.
# E.g. the original 8pen layout passed like this.
# "ybpqarx?nmf!ouvwelk@ihj,tcz.sdg'"
def ascii_art( letters, str_case, label, is_compact_layout=False ):
    str_case = str_case[:6].center(5)
    label = label[:6].center(5)
    letters = letters.ljust(39)
    layout_compact =  f"""
{letters[33]}\\{letters[38]}           {letters[3]}/{letters[8]}
 {letters[32]}\\{letters[37]}         {letters[2]}/{letters[7]}
  {letters[31]}\\{letters[36]}       {letters[1]}/{letters[6]}
   {letters[30]}\\{letters[35]}_____{letters[0]}/{letters[5]}
     |{str_case}|
     |{label}|
   {letters[25]}/{letters[20]}⎺⎺⎺⎺⎺{letters[15]}\\{letters[10]}
  {letters[26]}/{letters[21]}       {letters[16]}\\{letters[11]}
 {letters[27]}/{letters[22]}         {letters[17]}\\{letters[12]}
{letters[28]}/{letters[23]}           {letters[18]}\\{letters[13]}
"""

    layout =  f"""
{letters[33]} \\ {letters[38]}                 {letters[3]} / {letters[8]}
   \\                   / 
  {letters[32]} \\ {letters[37]}             {letters[2]} / {letters[7]}
     \\               / 
    {letters[31]} \\ {letters[36]}         {letters[1]} / {letters[6]}
       \\           / 
      {letters[30]} \\ {letters[35]}     {letters[0]} / {letters[5]}
         \\ _____ / 
          |{str_case}|
          |{label}|
         / ⎺⎺⎺⎺⎺ \\ 
      {letters[25]} / {letters[20]}     {letters[15]} \\ {letters[10]}
       /           \\ 
    {letters[26]} / {letters[21]}         {letters[16]} \\ {letters[11]}
     /               \\ 
  {letters[27]} / {letters[22]}             {letters[17]} \\ {letters[12]}
   /                   \\ 
{letters[28]} / {letters[23]}                 {letters[18]} \\ {letters[13]}
"""

    if is_compact_layout:
        return layout_compact
    else:
        return layout


DIRECTIONS = ['TOP', 'LEFT', 'BOTTOM', 'RIGHT']


def movement_sequence(start_at, clockwise, steps):
    yield start_at
    i = DIRECTIONS.index(start_at)
    direction = (-1 if clockwise else 1)
    for circular_distance in steps:
        for sector in range(0, circular_distance):
            i += direction
            yield DIRECTIONS[i % len(DIRECTIONS)]
        direction *= -1


def to_8vim_layout_string(new_layout):
    # 8VIM uses this string format to display the letters on the keyboard.
    # original_layout_string = "nomufv!weilhkj@,tscdzg.'yabrpxq?"
    new_layout_string = ""
    # Convert from our nice layout string to the ugly one that 8vim uses.
    for i in chain(range(10, 14), range(20, 24), range(30, 34), range(0, 4)):
        new_layout_string += new_layout[i] + new_layout[i+5]
    return new_layout_string


def movement_xml_layer(layout_lower, layout_upper, layer, at_sign_upper, layered_movement_sequencer):
    movement_lower = [layered_movement_sequencer(start_at, clockwise, i, layer, False)
                      for start_at in reversed(DIRECTIONS)
                      for clockwise in [False, True]
                      for i in range(1, 5)]
    movement_lower = movement_lower[-4:] + movement_lower[:-4]

    # The movement for going all the way around the board to capitalize.
    movement_upper = [layered_movement_sequencer(start_at, clockwise, i, layer, True)
                      for start_at in reversed(DIRECTIONS)
                      for clockwise in [False, True]
                      for i in range(1, 5)]
    movement_upper = movement_upper[-4:] + movement_upper[:-4]
    # All lower keys stored in here.
    final_output_lower = ""
    # All upper keys stored in here.
    final_output_upper = ""

    # Remove the spaces seperating the arms of the "X"
    layout_lower = ''.join([c for i, c in enumerate(layout_lower) if i % 5 != 4])
    layout_upper = ''.join([c for i, c in enumerate(layout_upper) if i % 5 != 4])

    for lower, upper, lower_movement, upper_movement in zip(layout_lower, layout_upper, movement_lower, movement_upper):
        caps_upper = upper
        caps_lower = lower
        if lower == upper == ' ':
            continue
        elif lower == upper == '@':
            # Keep the special functionality to enter your email address.
            upper = at_sign_upper[0]
            caps_lower = at_sign_upper[1]
            caps_upper = at_sign_upper[2]
        elif lower == upper == '!':
            # Useful exclamation marks
            upper = caps_upper = "!!!"
        elif ' ' == lower != upper:
            lower = caps_lower = upper
        elif ' ' == upper != lower:
            upper = caps_upper = lower
        assert(' ' not in [lower, upper])
        final_output_lower += f"""
    <keyboardAction>
        <keyboardActionType>INPUT_TEXT</keyboardActionType>
        <movementSequence>INSIDE_CIRCLE;{';'.join(lower_movement)};INSIDE_CIRCLE;</movementSequence>
        <inputString>{lower}</inputString>
        <inputCapsLockString>{upper}</inputCapsLockString>
    </keyboardAction>
"""
        final_output_upper += f"""
    <keyboardAction>
        <keyboardActionType>INPUT_TEXT</keyboardActionType>
        <movementSequence>INSIDE_CIRCLE;{';'.join(upper_movement)};INSIDE_CIRCLE;</movementSequence>
        <inputString>{caps_upper}</inputString>
        <inputCapsLockString>{caps_lower}</inputCapsLockString>
    </keyboardAction>
"""
    return f"""
    <!-- ~~~~~~~~~ -->
    <!-- Lowercase -->
    <!-- ~~~~~~~~~ -->{final_output_lower}

    <!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
    <!-- Capital Characters by going all the way around the board -->
    <!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->{final_output_upper}"""


XML_START = """<keyboardActionMap>
    <!-- Keywords for defining the movements -->
    <!--{NO_TOUCH, INSIDE_CIRCLE, TOP, LEFT, BOTTOM, RIGHT}-->
"""

XML_END = """

    <!--Paste Sequence-->
    <keyboardAction>
        <keyboardActionType>INPUT_SPECIAL</keyboardActionType>
        <movementSequence>LEFT;INSIDE_CIRCLE;NO_TOUCH;</movementSequence>
        <inputString>PASTE</inputString>
    </keyboardAction>


    <!--Shift-->
    <keyboardAction>
        <keyboardActionType>INPUT_SPECIAL</keyboardActionType>
        <movementSequence>TOP;NO_TOUCH;</movementSequence>
        <inputString>SHIFT_TOOGLE</inputString>
    </keyboardAction>


    <!-- Switch to Numpad-->
    <keyboardAction>
        <keyboardActionType>INPUT_SPECIAL</keyboardActionType>
        <movementSequence>LEFT;NO_TOUCH;</movementSequence>
        <inputString>SWITCH_TO_NUMBER_PAD</inputString>
    </keyboardAction>


    <!--Selection Mode Sequence-->
    <keyboardAction>
        <keyboardActionType>INPUT_SPECIAL</keyboardActionType>
        <movementSequence>RIGHT;INSIDE_CIRCLE;NO_TOUCH;</movementSequence>
        <inputString>SELECTION_START</inputString>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_SPECIAL</keyboardActionType>
        <movementSequence>RIGHT;INSIDE_CIRCLE;LONG_PRESS;</movementSequence>
        <inputString>SELECTION_START</inputString>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_SPECIAL</keyboardActionType>
        <movementSequence>RIGHT;INSIDE_CIRCLE;LONG_PRESS_END;</movementSequence>
        <inputString>SWITCH_TO_SELECTION_KEYBOARD</inputString>
    </keyboardAction>


    <!--Space-->
    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>INSIDE_CIRCLE;NO_TOUCH;</movementSequence>
        <inputKey>KEYCODE_SPACE</inputKey>
    </keyboardAction>


    <!-- Enter and Delete -->
    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>BOTTOM;NO_TOUCH;</movementSequence>
        <inputKey>KEYCODE_ENTER</inputKey>
    </keyboardAction>

    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>BOTTOM;LONG_PRESS;</movementSequence>
        <inputKey>KEYCODE_ENTER</inputKey>
    </keyboardAction>

    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>RIGHT;NO_TOUCH;</movementSequence>
        <inputKey>KEYCODE_DEL</inputKey>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>RIGHT;LONG_PRESS;</movementSequence>
        <inputKey>KEYCODE_DEL</inputKey>
    </keyboardAction>


    <!--D_Pad key-->
    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>NO_TOUCH;INSIDE_CIRCLE;TOP;NO_TOUCH;</movementSequence>
        <inputKey>KEYCODE_DPAD_UP</inputKey>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>NO_TOUCH;INSIDE_CIRCLE;BOTTOM;NO_TOUCH;</movementSequence>
        <inputKey>KEYCODE_DPAD_DOWN</inputKey>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>NO_TOUCH;INSIDE_CIRCLE;LEFT;NO_TOUCH;</movementSequence>
        <inputKey>KEYCODE_DPAD_LEFT</inputKey>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>NO_TOUCH;INSIDE_CIRCLE;RIGHT;NO_TOUCH;</movementSequence>
        <inputKey>KEYCODE_DPAD_RIGHT</inputKey>
    </keyboardAction>


    <!--Long press configuration-->
    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>NO_TOUCH;INSIDE_CIRCLE;TOP;LONG_PRESS;</movementSequence>
        <inputKey>KEYCODE_DPAD_UP</inputKey>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>NO_TOUCH;INSIDE_CIRCLE;BOTTOM;LONG_PRESS;</movementSequence>
        <inputKey>KEYCODE_DPAD_DOWN</inputKey>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>NO_TOUCH;INSIDE_CIRCLE;LEFT;LONG_PRESS;</movementSequence>
        <inputKey>KEYCODE_DPAD_LEFT</inputKey>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
        <movementSequence>NO_TOUCH;INSIDE_CIRCLE;RIGHT;LONG_PRESS;</movementSequence>
        <inputKey>KEYCODE_DPAD_RIGHT</inputKey>
    </keyboardAction>


    <!-- Hide keyboard -->
    <keyboardAction>
        <keyboardActionType>INPUT_SPECIAL</keyboardActionType>
        <movementSequence>TOP;INSIDE_CIRCLE;NO_TOUCH</movementSequence>
        <inputString>HIDE_KEYBOARD</inputString>
    </keyboardAction>

</keyboardActionMap>"""


class LayeringStrategies:
    def full_circle_to_capitalize(self, num_steps, is_upper):
        return [num_steps + (4 if is_upper else 0)]

    def eight_pen(self, start_at, clockwise, num_steps, layer, is_upper):
        return movement_sequence(start_at, clockwise, self.full_circle_to_capitalize(num_steps, is_upper) + [1, 1]*layer)

    def single_direction_change(self, start_at, clockwise, num_steps, layer, is_upper):
        return movement_sequence(start_at, clockwise, self.full_circle_to_capitalize(num_steps, is_upper) + ([layer] if layer > 0 else []))

    def prefix_eight_pen(self, start_at, clockwise, num_steps, layer, is_upper):
        return movement_sequence(start_at, clockwise, [1, 1]*layer + self.full_circle_to_capitalize(num_steps, is_upper))

    def seperate_letter(self, start_at, clockwise, num_steps, layer, is_upper):
        return ['TOP', 'INSIDE_CIRCLE']*layer + list(movement_sequence(start_at, clockwise, self.full_circle_to_capitalize(num_steps, is_upper)))

    def get_strategy(self, name):
        return self. __getattribute__(name)


################
# Main program #
################

outfile = splitext(sys.argv[1])[0] + '.xml' if len(sys.argv) == 2 else sys.argv[2]

with open(sys.argv[1]) as f:
    lines = [text.rstrip('\n\r') for text in f.readlines()]
layering = LayeringStrategies().get_strategy(lines[0])
at_sign_overloads = lines[1:4]

layers = []
for new_layout_lower, new_layout_upper, layer in [(lower, upper, i // 2) for i, (lower, upper) in enumerate(zip(lines[4:], lines[5:])) if i % 2 == 0]:
    if layer == 0:
        layer0_string_upper = to_8vim_layout_string(new_layout_upper)
        layer0_string_lower = to_8vim_layout_string(new_layout_lower)
    else:
        layers.append(f"""
    <!-- ========= -->
    <!-- Layer {layer}   -->
    <!-- ========= -->""")
    print('\n'.join(duo_colum(ascii_art( new_layout_lower, "lower", f"L {layer}" ), ascii_art( new_layout_upper, "upper", f"L {layer}" ))))
    layers.append(movement_xml_layer(new_layout_lower, new_layout_upper, layer, at_sign_overloads, layering))


with open(outfile, "w") as f:
    f.write( ''.join([XML_START] + layers + [XML_END]) )


print()
print("--- Usage Notes ---")
print("Edit this file")
print("8vim/src/main/java/inc/flide/vim8/views/mainKeyboard/XpadView.java)")
print("Change these variables to this:")
print( "String characterSetSmall = \"" + layer0_string_lower.replace("\"", "\\\"") + "\";" )
print( "String characterSetCaps  = \"" + layer0_string_upper.replace("\"", "\\\"") + "\";" )
print("")
print("The new keyboard layout has been saved to:")
print(outfile)
print("Move it to here:")
print("8vim/src/main/res/raw/keyboard_actions.xml")
print("")
print("Rebuild 8vim and send the apk to your phone.")

