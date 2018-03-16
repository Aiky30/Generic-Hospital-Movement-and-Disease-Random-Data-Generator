from config import *

import random
import csv
import radar
import math

from models import *


def random_date(start, stop):
    return radar.random_date(
        start=start,
        stop=stop
    )

class Movement:

    def __init__(self):

        self.individual_list = []

        # Generate individuals
        self.generate_individuals()

        self.create_output_file()

    #def __del__(self):

    def add_individual(self, individual):
        self.individual_list.append(individual)

    def generate_individuals(self):

        for individual_id in IN_PATIENT_LIST:

            individual = Individual(individual_id)
            self.add_individual(individual)

    def create_output_file(self):

        # Open file for writing
        try:
            # Open the file with option 'rU' Enable Universal newline support
            with open(OUTPUT_MOVEMENT_FILENAME, 'w') as csvfile:

                writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_MOVEMENT_HEADINGS)
                writer.writeheader()

                self.generate_movement(writer)

        except IOError as err:

            print("Error in file writing", err)
            exit(1)

    def generate_movement(self, writer):

        ###############
        # Individual
        ###############

        """
        for entry in xrange(0, INDIVIDUAL_COUNT):
        # FIXME: Exclude individuals already chosen!!
        # Choose a random individual
        random_individual_list = random.choice(INDIVIDUAL_LIST)
        """

        # Shuffle the list to mix the id's around a little
        #random.shuffle(INDIVIDUAL_LIST)

        output = []

        for individual in self.individual_list:

            individual_id = individual.id

            ###############
            # Admissions
            ###############

            # Number of admissions
            admission = self.generate_random_admission(MOVEMENT_DATE_START, MOVEMENT_DATE_END, ADMISSION_AVG_DURATION)

            admission_start_date = admission['start']
            admission_end_date = admission['end']

            ###############
            # LOCATIONS
            ###############

            # Calculate number of movements
            location_count = self.generate_location_count(admission_start_date, admission_end_date, LOCATION_DURATION_PER_COUNT, LOCATION_AVG_COUNT)

            # Generate a random date between the admission start and end date
            # Organise the randomly selected dates into the admission
            location_dates = self.generate_movement_list_dates(admission['start'], admission['end'], location_count)

            for i, locations_preselected in enumerate(range(0, location_count)):

                location_start_date = location_dates[i]['start']
                location_end_date = location_dates[i]['end']

                location_selected = random.choice(LOCATION_LIST)

                # Write the entry to the output file
                writer.writerow({
                    'EpisodeAdmissionDate': location_start_date.strftime(DATE_FORMAT),
                    'EpisodeDischargeDate': location_end_date.strftime(DATE_FORMAT),
                    'SpellDischargeDate': admission_end_date.strftime(DATE_FORMAT),
                    'SpellAdmissionDate': admission_start_date.strftime(DATE_FORMAT),
                    'Ward': location_selected,
                    'AnonPtNo': individual_id,
                    'Hospital': 'AddiesWards'
                })

                generated_location = Location(location_selected, location_start_date, location_end_date)
                individual.add_location(generated_location)

            generated_admission = Admission(admission_start_date, admission_end_date)
            individual.add_admission(generated_admission)

    # #http://www.caijournal.com/viewimage.asp?img=CommunityAcquirInfect_2015_2_1_13_153857_b2.jpg
    def generate_random_admission(self, master_start_date, master_end_date, master_duration):
        """

        :param start: Date
        :param end: Date
        :param duration: Int
        :return: Dict: { start: Date, end: Date }
        """
        duration = random.choice(master_duration)

        # Generate a random date between the specified time period
        start_date = random_date(
            start=master_start_date,
            stop=master_end_date
        )

        end_date = start_date + timedelta(minutes=duration)

        return {
            'start': start_date,
            'end': end_date
        }

    def generate_location_count(self, master_start_date, master_end_date, location_duration_per_count, location_average_count):

        # Dictate how many locations the admission should have
        location_count = random.choice(location_average_count)

        # how many days is the admission
        duration = master_end_date - master_start_date

        blocks = int(math.ceil(duration.days / location_duration_per_count))

        if blocks > 1:
            location_count *= blocks

        return location_count

    def generate_movement_list_dates(self, master_start_date, master_end_date, location_count):
        """
        :return: array [{
            start: Date,
            end: Date
        }]
        """

        if location_count == 1:
            return [{
                'start': master_start_date,
                'end': master_end_date
            }]


        dates = []

        for location in range(location_count - 1):

            random_date = radar.random_date(
                start=master_start_date,
                stop=master_end_date
            )

            dates.append(random_date)

        # Sort the dates into ascending order
        dates.sort()

        # FIXME: location count is 1???

        # first loop set the start to be admission start, end to be random date 1
        dates_out = [{
            'start': master_start_date,
            'end': dates[0]
        }]

        # continuous loops start is last loops value, end is current loops value
        for i, date in enumerate(dates):

            # last loop start is current value, last is admission
            if len(dates) - 1 > i:
                end = dates[i + 1]
            else:
                end = master_end_date

            dates_out.append({
                'start': date,
                'end': end
            })

        return dates_out
