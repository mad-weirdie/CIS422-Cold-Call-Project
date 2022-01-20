"""
01/16/2021

Manages the performance summary.txt and keeps track
of student data
"""
from student import Student
from os.path import exists
from datetime import *
class LogManager():
    """
    Initialized in the main controller, the Log Manager manages log file and performance summary file
    output.
    """

    def __init__(self, filename):
        # filename 
        self.filename = filename

    def write(self, students, called_student: Student, flagged: bool):
        """ 
        Called from the main controller each time a student is cold called, handles file output:

            1.  Overwrites previous summary performance file (if it exists) with updated information
            2.  Writes cold call information to the Daily Log Manager
            
        """
        # open filename in overwrite mode
        summary_file = open(self.filename, "w")

        # header
        summary_file.write("Summary Performance File for Cold Call Assist program\n")
        summary_file.write("|Total Times Called|    |Total Times Flagged|   |First Name|    |Last Name| |UO ID| |Email Address| |Phonetic Spelling| |Reveal Code|   |Dates Called|\n")
        
        # print all student information
        for student in students:
            studentline = f'{len(student.dates_called)}\t{student.total_num_flags}\t{student.first_name}\t{student.UO_ID}\t'
            studentline += f'{student.phonetic_spelling}\t{student.reveal_code}\t'
            for date in student.dates_called:
                studentline += f'{date} '
            studentline += '\n'
            summary_file.write(studentline)
        
        # write to daily log file
        self._write_line(called_student, flagged)
            
    def _write_line(self, student, flagged: bool):
        """
        Writes a line to the daily log file for a cold call for a student,
        where the flagged argument determines whether to flag the cold call
        with an 'X' or not. Creates daily log file if necessary with a heading
        and today's date.
        """
        # get date for creating the file name
        date = datetime.today().strftime('%Y-%m-%d')

        # create the file name
        file_name = f'daily_log--{date}.txt'

        # create the file with heading and date if it doesn't exist
        heading = f"This is the daily log file for the cold-call assist program."
        if not exists(file_name):
            with open(file_name, 'w') as f:
                f.write(heading + '\n')
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
        with open(file_name, 'a') as f:
            f.write(cold_call)

        return


