"""
Unit tests for Log Manager module.
"""

from datetime import datetime

import os
import unittest

from student import Student

import log_manager

class TestLogManager(unittest.TestCase):

    def test_daily_log(self):
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
                                      'areichh2@uoregon.edu', 'AY-mee', '')
            logger = LogManager("summary.txt")
            logger.write(example_student, True)

            The above code would result in a file like the following:

            Daily Log for Cold Call Assist Program
            2022-01-16
            X	Amy Reichhold <areichh2@uoegon.edu>
        """
        # get date for creating the file name
        date = datetime.today().strftime('%Y-%m-%d')

        # create the file name and absolute file name the same way that the
        # log manager creates them
        file_name = f'{log_manager.DAILY_LOG_FILE_NAME_PREFIX}--{date}.txt'
        absolute_file_name = os.path.join(
                log_manager.DAILY_LOG_PATH, file_name)

        # testing assumes the file doesn't already exist, so warn if so
        if os.path.exists(absolute_file_name):
            self.skipTest(f'WARNING: {absolute_file_name} exists; please move or'
                    ' remove the file in order to run this test')
            return None

        # create the actual test data and log it
        student = Student('Amy', 'Reichhold', '951000000', 
                          'areichh2@uoregon.edu', 'AY-mee', '')
        logger = log_manager.LogManager("test_summary.txt")
        logger.write_logfile(student, True)

        # check if directory exists
        self.assertTrue(os.path.exists(log_manager.DAILY_LOG_PATH))

        # check if log file exists (TODO: add file_name as member variable?)
        self.assertTrue(os.path.exists(absolute_file_name))

        # create a cold call of the following form:
        # 'X    Fatima Patel <fpatel@uoregon.edu>'
        # (with no quotes)
        cold_call = f'X\tAmy Reichhold <areichh2@uoregon.edu>'

        # open the log file
        with open(absolute_file_name, 'r') as f:
            # read lines
            lines = f.read().splitlines()

            # check if the heading is present
            self.assertEqual(lines[0], log_manager.DAILY_LOG_HEADING)
            
            # check if the date is present
            self.assertEqual(lines[1], date)

            # check if the student is present
            self.assertEqual(lines[2], cold_call)

        return None

if __name__ == '__main__':
    unittest.main()

