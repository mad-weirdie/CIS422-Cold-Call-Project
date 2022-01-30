#!/usr/bin/env python3

###############################################################################
"""
Script Name:    CoolCall Application Start Up 

Description:    Run this script at the command line to start the application.
                This file calls the Instructor Interaction Model which is the
                main controller for the CoolCall program.

Author:         Arden Butterfield

Last Edited:    1/30/2022
Last Edit By:   Arden Butterfield
"""
###############################################################################
from instructor_interaction_model import InstructorInteractionModel
###############################################################################

def main():
    InstructorInteractionModel()

if __name__ == "__main__":
    main()

