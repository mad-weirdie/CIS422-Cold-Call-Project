###############################################################################
"""
Script Name:    Constants and Numerical Parameters

Description:    We have located numerical parameters and keystroke/button assignments 
                to this source code file. They are easily changeable by a programmer during 
                development and maintenance of the code.

Authors:        Arden Butterfield, Derek Martin

Last Edited:    1/28/2022
Last Edit By:   Derek Martin
"""
###############################################################################

# Global variable for the number of students the instructor would like to have
# "on deck" from the queue at any given time.
import os.path

# NOTE: If NUM_ON_DECK is >= queue_size, then the # of students on-deck will be set to == queue_size.
#       This is handled in the get_on_deck() function in student_queue.py
NUM_ON_DECK = 4

# Don't insert students back into the queue at a certain percentage of the head.
# NOTE: If the INSERT_DELAY value is such that a student can possibly be reinserted into an on-deck position,
#       (that is, if INSERT_DELAY < (NUM_ON_DECK / queue_size)), then INSERT_DELAY will be set to (NUM_ON_DECK / queue_size).
#       This is handled in the randomized_enqueue() function in student_queue.py
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

LOGS_LOCATION = (os.path.join(os.path.dirname(__file__), "../logs"))
DAILY_LOG_HEADING = "Daily Log File for Cold Call Assist program."
DAILY_LOG_FILE_NAME_PREFIX = "daily_log"

# Locations for internal data storage
INTERNAL_ROSTER_LOCATION = (os.path.join(os.path.dirname(__file__), "student_data/roster.txt"))
INTERNAL_QUEUE_LOCATION = (os.path.join(os.path.dirname(__file__), "student_data/student_queue"))