#!/usr/bin/env python3

###############################################################################
"""
Script Name:    Log Manager

Description:    The LogManager Class for the CoolCall Program.
                Initialized in the Instructor Interaction Model, the Log Manager
                manages log and performance summary file output.

Authors:        Arden Butterfield, Quinn Fetrow, Derek Martin, Amy Reichhold, 
                Madison Werries

Last Edited:    1/30/2022
Last Edit By:   Amy Reichold
"""
###############################################################################
from student import Student
from datetime import datetime
from constants import *
import os
###############################################################################

class LogManager():
    """
    A class for managing output files.

    Attributes
    =======================================================================
    filename
        The name of the output file to write to

    Methods
    =======================================================================
    write(students, called_student, flagged)
        Called from the Instructor Interaction Model each time a student is
        cold called. 

    write_logfile(student, flagged)

    """

    def __init__(self, filename):
        # filename 
        self.filename = filename

    def write(self, students, called_student: Student, flagged: bool):
        """ 
        Overwrites previous summary performance file (if it exists) with updated information.
        Writes cold call information to the Daily Log Manager.
            
        students: (list) a list of Student objects
        called_student: (Student) a specific Student that has been cold called
        flagged: (boolean) has a flag been set for this cold call?
        """

        # create the file name and absolute file name
        summary_filename = LOGS_LOCATION + "/summary.txt"

        # open filename in overwrite mode
        summary_file = open(summary_filename, "w")


        # header
        summary_file.write("Summary Performance File for Cold Call Assist program\n")
        summary_file.write("|Total Times Called|    |Total Times Flagged|   |First Name|    |Last Name| |UO ID| |Email Address| |Phonetic Spelling| |Reveal Code|   |Dates Called|\n")
        
        # print all student information
        for student in students:
            studentline = f'{len(student.dates_called)}\t{student.total_num_flags}\t{student.first_name}\t{student.last_name}\t{student.UO_ID}\t{student.email_address}\t'
            studentline += f'{student.phonetic_spelling}\t{student.reveal_code}\t'
            for date in student.dates_called:
                studentline += f'{date} '
            studentline += '\n'
            summary_file.write(studentline)

        # closing file
        summary_file.close()
        
        # write to daily log file
        self.write_logfile(called_student, flagged)
            
    def write_logfile(self, student, flagged: bool):
        """
        Writes a line to the daily log file, recording a cold call.
        The flagged argument determines whether to flag the cold call
        with an 'X' or not.Creates daily log file if necessary with a heading
        and today's date.

        student: (Student) a specific Student that has been cold called
        flagged: (boolean) has a flag been set for this cold call?
        """
        # get date for creating the file name
        date = datetime.today().strftime('%Y-%m-%d')

        # create the file name and absolute file name
        log_file_name = f'{LOGS_LOCATION}/{DAILY_LOG_FILE_NAME_PREFIX}--{date}.txt'

        # this code has been commented out
        """# check if directory exists
        if not os.path.exists(DAILY_LOG_PATH):
            os.makedirs(DAILY_LOG_PATH)
        else:
            # DAILY_LOG_PATH exists
            pass"""
        
        # create the file with heading and date if it doesn't exist
        if not os.path.exists(log_file_name):
            with open(log_file_name, 'w') as f:
                f.write(DAILY_LOG_HEADING + '\n')
                f.write(date + '\n')

        # form the response code
        response_code = ''
        if flagged:
            response_code = 'X'

        # append the cold call to the file, of this form:
        # 'X    Fatima Patel <fpatel@uoregon.edu>'
        # (with no quotes)
        cold_call = f'{response_code}\t'
        cold_call += f'{student.first_name} {student.last_name}'
        cold_call += f' <{student.email_address}>\n'
        with open(log_file_name, 'a') as f:
            f.write(cold_call)

        return


