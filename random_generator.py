from config import *

import sys
import random
import csv
import radar
import math

"""
Generic Hospital Movement and Disease Random Data Generator (GHMDRDG)
===================================================

Running: ~/virtual_environments/development/movement-and-disease-random-generator/bin/python2.7 ./random_generator.py

locations list (read from file)

TODO: Going to get overlaps so need to see if an individual has been admitted on a certain date which woudl cause clash

Metrics are on:
 - Patient count
 - Admission count
 - Location count
 - Antibiogram count
"""

# TODO: To keep the dates in check, minus the longet admission duration from the last date then the end date can't conflict with it.

# IDEA: Min, Max and avrg could be the algorithm for random
# FIXME: Randomise dates: http://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates

"""

IDEA: Make one method of antibiogram more popular than others, some kind of percentage based allocation in the random selection.


Config for AB
"""


#FIXME: Shouldn't be declared as a global!!
ANTIBIOGRAM_RESULTS = []


def build_random_antibiogram_list():

    # Build a list of usable antibiograms
    for index in ANTIBIOGRAM_RESULT_BANK:

        antibiogram = {}

        # For each antibiogram antibiotic
        for antibiotic in ANTIBIOGRAM_ANTIBIOTICS:

            # Allocate a random result to the antibiotic
            antibiogram[antibiotic] = random.choice(ANTIBIOGRAM_ANTIBIOTIC_VALUES)

        ANTIBIOGRAM_RESULTS.append(antibiogram)

def get_antibiogram_list_from_file(filename):

    # Open file for reading
    try:
        # Open the file with option 'rU' Enable Universal newline support
        with open(filename, 'rU') as csvfile:

            reader = csv.DictReader(csvfile)

            # Load the file into memory (FIXME: this won't work for big data sets)
            mapped_data = []

            for row in reader:

                row_data = {}

                for heading in ANTIBIOGRAM_SOURCE_FILE_HEADINGS:
                    row_data.update({
                        heading: row[heading]
                    })

                ANTIBIOGRAM_RESULTS.append(row_data)

    except IOError as err:
        sys.exit(err)

def generate_random_admission(master_start_date, master_end_date, master_duration):
    """

    :param start: Date
    :param end: Date
    :param duration: Int
    :return: Dict: { start: Date, end: Date }
    """
    duration = random.choice(master_duration)

    # Generate a random date between the specified time period
    start_date = radar.random_date(
        start=master_start_date,
        stop=master_end_date
    )

    end_date = start_date + timedelta(minutes=duration)

    return {
        'start': start_date,
        'end': end_date
    }

#http://www.caijournal.com/viewimage.asp?img=CommunityAcquirInfect_2015_2_1_13_153857_b2.jpg


def generate_location_count(master_start_date, master_end_date, location_duration_per_count, location_average_count):

    # Dictate how many locations the admission should have
    location_count = random.choice(location_average_count)

    # how many days is the admission
    duration = master_end_date - master_start_date

    blocks = int(math.ceil(duration.days / location_duration_per_count))

    if blocks > 1:
        location_count *= blocks

    return location_count


def generate_movement_list_dates(master_start_date, master_end_date, location_count):
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


def generate_movement(writer):

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

    for individual in INDIVIDUAL_LIST:

        ###############
        # Admissions
        ###############

        # Number of admissions

        admission = generate_random_admission(DATE_START, DATE_END, ADMISSION_AVG_DURATION)

        admission_start_date = admission['start']
        admission_end_date = admission['end']

        ###############
        # LOCATIONS
        ###############

        location_count = generate_location_count(admission_start_date, admission_end_date, LOCATION_DURATION_PER_COUNT, LOCATION_AVG_COUNT)

        location_dates = generate_movement_list_dates(admission['start'], admission['end'], location_count)

        admissions = []

        """

        Get number of movements
        for the total count of movements
            generate a random date between the admission start and end date

        organise the randomly selected dates into the

        """


        for i, locations_preselected in enumerate(xrange(0, location_count)):

            location_start_date = location_dates[i]['start']
            location_end_date = location_dates[i]['end']

            location_selected = random.choice(LOCATION_LIST)
            #location_days = random.choice(LOCATION_AVG_DURATION)

            #tmp_location_start_date = location_start_date
            #location_end_date = tmp_location_start_date + timedelta(minutes=location_duration)


            # Write the entry to the output file
            writer.writerow({
                'EpisodeAdmissionDate': location_start_date.strftime(DATE_FORMAT),
                'EpisodeDischargeDate': location_end_date.strftime(DATE_FORMAT),
                'SpellDischargeDate': admission_end_date.strftime(DATE_FORMAT),
                'SpellAdmissionDate': admission_start_date.strftime(DATE_FORMAT),
                'Ward': location_selected,
                'AnonPtNo': individual,
                'Hospital': 'ABCDEF'
            })

            # Set the start to be the end of the last location
            location_start_date = location_end_date


        admissions.append({
            'admission_date': admission_start_date,
            'discharge_date': admission_end_date
        })

        output.append({
            'individual': individual,
            'admissions': admissions
        })

    return output

def generateIsolate(writer, output):

    for isolate in ISOLATE_COUNT:

        # Randomly select an individual
        random_individual = random.choice(output)

        # Randomly select an antibiogram result set
        random_antibiogram = random.choice(ANTIBIOGRAM_RESULTS)

        # randomly select a date within the individuals admissions
        random_date = radar.random_date(
            start=random_individual.get('admissions')[0].get('admission_date'), #FIXME: Getting 0 is a hack!!
            stop=random_individual.get('admissions')[0].get('discharge_date'), #FIXME: Getting 0 is a hack!!
        )

        #TODO: Auto write the rows headings etc to the file rather than entering each manually here

        current_row = {
            'AnonPtNo': random_individual.get('individual'),
            'DateSent': random_date.strftime(ISOLATE_DATE_FORMAT),
            'Originaldescription': random.choice(original_description),
            'SampleID': 'MPROS' + str(isolate)
        }

        for antibiotic in ANTIBIOGRAM_ANTIBIOTICS:

            current_row.update({
                antibiotic: random_antibiogram.get(antibiotic)
            })

        writer.writerow(current_row)


def build_movement_file():

    # Open file for writing
    try:
        # Open the file with option 'rU' Enable Universal newline support
        with open(OUTPUT_MOVEMENT_FILENAME, 'w') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_MOVEMENT_HEADINGS)
            writer.writeheader()

            return generate_movement(writer)

    except IOError as err:
        print("Error in file writing", err)


def build_isolate_file(output):

    # Open file for writing
    try:
        # Open the file with option 'rU' Enable Universal newline support
        with open(OUTPUT_ISOLATE_FILENAME, 'w') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_ISOLATE_HEADINGS)
            writer.writeheader()

            generateIsolate(writer, output)

    except IOError as err:
        print("Error in file writing", err)


def main():

    build_random_antibiogram_list()
    #get_antibiogram_list_from_file(ANTIBIOGRAM_SOURCE_FILE_LOCATION)

    output = build_movement_file()

    build_isolate_file(output)

    exit()

if __name__ == "__main__":
    main()
