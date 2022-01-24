
# Global variable for the number of students the instructor would like to have
# "on deck" from the queue at any given time.
NUM_ON_DECK = 4

# Don't insert students back into the queue at a certain percentage of the head.
INSERT_DELAY = 0.35

# We expect the roster to be a tab-separated file. To accept comma-separated
# files, change this to ",".
ROSTER_DELIMITER = "\t"

#### Key bindings
# Change the keys used to control the On-deck window by changing these keys
# The key symbols are detailed in the Tkinter specifications,
# and can be referenced here: https://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.html
# A more human-readable table of common keys and their corresponding
# key symbols is available here:
# https://web.archive.org/web/20190515021108id_/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html


# Move the selection in the on-deck display to the left
MOVE_LEFT_KEY = "Left"  # Left arrow

# Move the selection in the on-deck display to the right
MOVE_RIGHT_KEY = "Right"  # Right arrow

# Remove the selected student from the on-deck display, flagging them
REMOVE_WITH_FLAG_KEY = "Up"  # Up arrow

# Remove the selected student from the on-deck display, without flagging them
REMOVE_WITHOUT_FLAG_KEY = "Down"  # Down arrow
