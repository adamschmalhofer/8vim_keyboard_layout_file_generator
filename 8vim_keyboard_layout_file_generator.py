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


# Please change this to the layout you want
# Make the @ character in the same place for the upper and lower case for extra functionality.
#    Circle around the board 1 more time to input your email address.
#    In caps lock mode writing an @ will enter @gmail.com for you
# Make the ! character in the same place for the upper and lower case for extra functionality.
#    Circle around the board 1 more time to write three exclamation marks !!!
new_layout_lower      = "nmpq ecx? rsb! ouvz hlj@ ifw, tyk. adg'"
new_layout_upper      = "NMPQ ECX* RSB! OUVZ HLJ@ IFW_ TYK- ADG\""

# WARNING: Don't change this original string!
# It's not used in the code, but is your reference for what the new layout will look like compared to the old one.
original_layout_lower = "ybpq arx? nmf! ouvw elk@ ihj, tcz. sdg'"
original_layout_upper = "YBPQ ARX* NMF! OUVW ELK@ IHJ_ TCZ- SDG\""

# Put your email address here for it to be added when you go all the way around the board for the @ sign.
your_email_address = "youremailaddress@gmail.com"

# Setup over.
# Please run the script and it will output the keyboard_actions.xml file for you :).

# -------------------
#    Program start
# -------------------

# Passed a string of just letters and will map that to the layout.
# E.g. the original 8pen layout passed like this.
# "ybpqarx?nmf!ouvwelk@ihj,tcz.sdg'"
def print_new_layout( letters, is_lowercase=True, is_compact_layout=False ):
    if is_lowercase == True:
        str_case = "lower"
    else:
        str_case = "upper"

    layout_compact =  f"""
{letters[27]}\{letters[31]}           {letters[3]}/{letters[7]}
 {letters[26]}\{letters[30]}         {letters[2]}/{letters[6]}
  {letters[25]}\{letters[29]}       {letters[1]}/{letters[5]}
   {letters[24]}\{letters[28]}_____{letters[0]}/{letters[4]}
     |{str_case}|
     |case |
   {letters[20]}/{letters[16]}⎺⎺⎺⎺⎺{letters[12]}\{letters[8]}
  {letters[21]}/{letters[17]}       {letters[13]}\{letters[9]}
 {letters[22]}/{letters[18]}         {letters[14]}\{letters[10]}
{letters[23]}/{letters[19]}           {letters[15]}\{letters[11]}
"""

    layout =  f"""
{letters[27]} \ {letters[31]}                 {letters[3]} / {letters[7]}
   \                   / 
  {letters[26]} \ {letters[30]}             {letters[2]} / {letters[6]}
     \               / 
    {letters[25]} \ {letters[29]}         {letters[1]} / {letters[5]}
       \           / 
      {letters[24]} \ {letters[28]}     {letters[0]} / {letters[4]}
         \ _____ / 
          |{str_case}|
          |case |
         / ⎺⎺⎺⎺⎺ \ 
      {letters[20]} / {letters[16]}     {letters[12]} \ {letters[8]}
       /           \ 
    {letters[21]} / {letters[17]}         {letters[13]} \ {letters[9]}
     /               \ 
  {letters[22]} / {letters[18]}             {letters[14]} \ {letters[10]}
   /                   \ 
{letters[23]} / {letters[19]}                 {letters[15]} \ {letters[11]}
"""

    if is_compact_layout:
        print( layout_compact )
    else:
        print( layout )

    return

################
# Main program #
################


DIRECTIONS = ['TOP', 'LEFT', 'BOTTOM', 'RIGHT']


def movement_sequence(start_at, clockwise, steps):
    sequence = [start_at]
    i = DIRECTIONS.index(start_at)
    direction = (-1 if clockwise else 1)
    for circular_distance in steps:
        for sector in range(0, circular_distance):
            i += direction
            sequence.append(DIRECTIONS[i % len(DIRECTIONS)])
        direction *= -1
    return f"        <movementSequence>INSIDE_CIRCLE;{';'.join(sequence)};INSIDE_CIRCLE;</movementSequence>"


# The movements assigned to the original layout.
# We use this to make the new layout 
movement_lower = [
    movement_sequence('TOP', True, [1]),
    movement_sequence('TOP', True, [2]),
    movement_sequence('TOP', True, [3]),
    movement_sequence('TOP', True, [4]),

    movement_sequence('RIGHT', False, [1]),
    movement_sequence('RIGHT', False, [2]),
    movement_sequence('RIGHT', False, [3]),
    movement_sequence('RIGHT', False, [4]),

    movement_sequence('RIGHT', True, [1]),
    movement_sequence('RIGHT', True, [2]),
    movement_sequence('RIGHT', True, [3]),
    movement_sequence('RIGHT', True, [4]),

    movement_sequence('BOTTOM', False, [1]),
    movement_sequence('BOTTOM', False, [2]),
    movement_sequence('BOTTOM', False, [3]),
    movement_sequence('BOTTOM', False, [4]),

    movement_sequence('BOTTOM', True, [1]),
    movement_sequence('BOTTOM', True, [2]),
    movement_sequence('BOTTOM', True, [3]),
    movement_sequence('BOTTOM', True, [4]),

    movement_sequence('LEFT', False, [1]),
    movement_sequence('LEFT', False, [2]),
    movement_sequence('LEFT', False, [3]),
    movement_sequence('LEFT', False, [4]),

    movement_sequence('LEFT', True, [1]),
    movement_sequence('LEFT', True, [2]),
    movement_sequence('LEFT', True, [3]),
    movement_sequence('LEFT', True, [4]),

    movement_sequence('TOP', False, [1]),
    movement_sequence('TOP', False, [2]),
    movement_sequence('TOP', False, [3]),
    movement_sequence('TOP', False, [4]),
]


# The movement for going all the way around the board to capitalize.
movement_upper = [
    movement_sequence('TOP', True, [5]),
    movement_sequence('TOP', True, [6]),
    movement_sequence('TOP', True, [7]),
    movement_sequence('TOP', True, [8]),

    movement_sequence('RIGHT', False, [5]),
    movement_sequence('RIGHT', False, [6]),
    movement_sequence('RIGHT', False, [7]),
    movement_sequence('RIGHT', False, [8]),

    movement_sequence('RIGHT', True, [5]),
    movement_sequence('RIGHT', True, [6]),
    movement_sequence('RIGHT', True, [7]),
    movement_sequence('RIGHT', True, [8]),

    movement_sequence('BOTTOM', False, [5]),
    movement_sequence('BOTTOM', False, [6]),
    movement_sequence('BOTTOM', False, [7]),
    movement_sequence('BOTTOM', False, [8]),

    movement_sequence('BOTTOM', True, [5]),
    movement_sequence('BOTTOM', True, [6]),
    movement_sequence('BOTTOM', True, [7]),
    movement_sequence('BOTTOM', True, [8]),

    movement_sequence('LEFT', False, [5]),
    movement_sequence('LEFT', False, [6]),
    movement_sequence('LEFT', False, [7]),
    movement_sequence('LEFT', False, [8]),

    movement_sequence('LEFT', True, [5]),
    movement_sequence('LEFT', True, [6]),
    movement_sequence('LEFT', True, [7]),
    movement_sequence('LEFT', True, [8]),

    movement_sequence('TOP', False, [5]),
    movement_sequence('TOP', False, [6]),
    movement_sequence('TOP', False, [7]),
    movement_sequence('TOP', False, [8]),
]



# 8VIM uses this string format to display the letters on the keyboard.
original_layout_string_lower = "nomufv!weilhkj@,tscdzg.'yabrpxq?"
original_layout_string_upper = "NOMUFV!WEILHKJ@_TSCDZG-\"YABRPXQ*"

new_layout_string_lower = ""
new_layout_string_upper = ""

# Convert from our nice layout string to the ugly one that 8vim uses.
for i in range(10, 14):
    new_layout_string_lower += new_layout_lower[i]
    new_layout_string_lower += new_layout_lower[i+5]
    new_layout_string_upper += new_layout_upper[i]
    new_layout_string_upper += new_layout_upper[i+5]

for i in range(20, 24):
    new_layout_string_lower += new_layout_lower[i]
    new_layout_string_lower += new_layout_lower[i+5]
    new_layout_string_upper += new_layout_upper[i]
    new_layout_string_upper += new_layout_upper[i+5]

for i in range(30, 34):
    new_layout_string_lower += new_layout_lower[i]
    new_layout_string_lower += new_layout_lower[i+5]
    new_layout_string_upper += new_layout_upper[i]
    new_layout_string_upper += new_layout_upper[i+5]

for i in range(0, 4):
    new_layout_string_lower += new_layout_lower[i]
    new_layout_string_lower += new_layout_lower[i+5]
    new_layout_string_upper += new_layout_upper[i]
    new_layout_string_upper += new_layout_upper[i+5]



###################################################
# Start buliding the keyboard_actions.xml output. #
###################################################

# Used with sending key code
INPUT_KEY_START = """
    <keyboardAction>
        <keyboardActionType>INPUT_KEY</keyboardActionType>
"""
INPUT_KEY_END = """
    </keyboardAction>
"""

# This line is used with capital letters for some reason.
# It's used when we circle around the board to capitalize a letter.
FLAGS = """
        <flags>
            <flag>1</flag>
        </flags>"""

# Inputing text rather than a single keycode.
INPUT_TEXT_START = """
    <keyboardAction>
        <keyboardActionType>INPUT_TEXT</keyboardActionType>
"""

INPUT_TEXT_END = """
    </keyboardAction>
"""

# All lower keys stored in here.
final_output_lower = ""
# All upper keys stored in here.
final_output_upper = ""

new_layout_lower = new_layout_lower.replace(" ", "")
new_layout_upper = new_layout_upper.replace(" ", "")

for i in range( len( new_layout_lower ) ):
    if (new_layout_lower[i] == '@') and (new_layout_upper[i] == '@'):
        # Keep the special functionality to enter your email address.
        input_string_lower = "@"
        input_string_upper = your_email_address
    elif (new_layout_lower[i] == '!') and (new_layout_upper[i] == '!'):
        # Useful exclamation marks
        input_string_lower = "!"
        input_string_upper = "!!!"
    else:
        # It's just a normal special character so just add it.
        input_string_lower = new_layout_lower[i]
        input_string_upper = new_layout_upper[i]

    output_lower = f'{INPUT_TEXT_START}{movement_lower[i]}\n        <inputString>{input_string_lower}</inputString>\n        <inputCapsLockString>{input_string_upper}</inputCapsLockString>{INPUT_TEXT_END}'
    output_upper = f'{INPUT_TEXT_START}{movement_upper[i]}\n        <inputString>{input_string_upper}</inputString>\n        <inputCapsLockString>{input_string_lower}</inputCapsLockString>{INPUT_TEXT_END}'

    final_output_lower += output_lower
    final_output_upper += output_upper



XML_START = """<keyboardActionMap>
    <!-- Keywords for defining the movements -->
    <!--{NO_TOUCH, INSIDE_CIRCLE, TOP, LEFT, BOTTOM, RIGHT}-->

    <!-- ~~~~~~~~~ -->
    <!-- Lowercase -->
    <!-- ~~~~~~~~~ -->"""

CAPITAL = """

    <!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->
    <!-- Capital Characters by going all the way around the board -->
    <!-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ -->"""
final_output_upper

XML_END = """

    <!-- ~~~~~~~~~~~~~~~~~~~~ -->
    <!-- Esperanto Characters -->
    <!-- ~~~~~~~~~~~~~~~~~~~~ -->
    <keyboardAction>
        <keyboardActionType>INPUT_TEXT</keyboardActionType>
        <movementSequence>INSIDE_CIRCLE;LEFT;TOP;RIGHT;TOP;RIGHT;INSIDE_CIRCLE;</movementSequence>
        <inputString>ĉ</inputString>
        <inputCapsLockString>Ĉ</inputCapsLockString>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_TEXT</keyboardActionType>
        <movementSequence>INSIDE_CIRCLE;TOP;LEFT;BOTTOM;RIGHT;BOTTOM;RIGHT;INSIDE_CIRCLE;</movementSequence>
        <inputString>ĝ</inputString>
        <inputCapsLockString>Ĝ</inputCapsLockString>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_TEXT</keyboardActionType>
        <movementSequence>INSIDE_CIRCLE;LEFT;BOTTOM;RIGHT;BOTTOM;RIGHT;INSIDE_CIRCLE;</movementSequence>
        <inputString>ĥ</inputString>
        <inputCapsLockString>Ĥ</inputCapsLockString>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_TEXT</keyboardActionType>
        <movementSequence>INSIDE_CIRCLE;LEFT;BOTTOM;RIGHT;TOP;RIGHT;TOP;INSIDE_CIRCLE;</movementSequence>
        <inputString>ĵ</inputString>
        <inputCapsLockString>Ĵ</inputCapsLockString>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_TEXT</keyboardActionType>
        <movementSequence>INSIDE_CIRCLE;TOP;LEFT;TOP;LEFT;INSIDE_CIRCLE;</movementSequence>
        <inputString>ŝ</inputString>
        <inputCapsLockString>Ŝ</inputCapsLockString>
    </keyboardAction>
    <keyboardAction>
        <keyboardActionType>INPUT_TEXT</keyboardActionType>
        <movementSequence>INSIDE_CIRCLE;BOTTOM;RIGHT;TOP;RIGHT;TOP;INSIDE_CIRCLE;</movementSequence>
        <inputString>ŭ</inputString>
        <inputCapsLockString>Ŭ</inputCapsLockString>
    </keyboardAction>


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

output = XML_START + final_output_lower + CAPITAL + final_output_upper + XML_END
f = open("keyboard_actions.xml", "w")
f.write( output )
f.close()

print_new_layout( new_layout_lower, is_lowercase=True  )
print_new_layout( new_layout_upper, is_lowercase=False )

print()
print("--- Usage Notes ---")
print("Edit this file")
print("8vim/src/main/java/inc/flide/vim8/views/mainKeyboard/XpadView.java)")
print("Change these variables to this:")
print( "String characterSetSmall = \"" + new_layout_string_lower.replace("\"", "\\\"") + "\";" )
print( "String characterSetCaps  = \"" + new_layout_string_upper.replace("\"", "\\\"") + "\";" )
print("")
print("The new keyboard layout has been saved to:")
print("keyboard_actions.xml")
print("Move it to here:")
print("8vim/src/main/res/raw/keyboard_actions.xml")
print("")
print("Rebuild 8vim and send the apk to your phone.")

