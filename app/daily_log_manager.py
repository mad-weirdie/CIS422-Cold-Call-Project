"""
Daily Log Manager data structure: Appends a cold call to the daily log file
with the student's information.
"""

from datetime import datetime
from os.path import exists

heading = 'Daily Log for Cold Call Assist Program'

class DailyLogManager:
    def __init__(self):
        # doesn't need to store anything
        pass

    def write_line(self, student, flagged: bool):
        """
        Writes a line to the daily log file for a cold call for a student,
        where the flagged argument determines whether to flag the cold call
        with an 'X' or not. Creates daily log file if necessary with a heading
        and today's date.

        Args:
            student: An instance of the Student class.
            flagged: A boolean which if True places an 'X' next to the student
                     name.

        Returns: 
            None

        Example:
            example_student = Student('Amy', 'Reichhold', '951000000', 
                                      'areichh2@uoegon.edu', 'AY-mee', '')
            log = DailyLogManager()
            log.write_line(example_student, True)

            The above code would result in a file like the following:

            Daily Log for Cold Call Assist Program
            2022-01-16
            X	Amy Reichhold <areichh2@uoegon.edu>
        """
        # get date for creating the file name
        date = datetime.today().strftime('%Y-%m-%d')

        # create the file name
        file_name = f'daily_log--{date}.txt'

        # create the file with heading and date if it doesn't exist
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
