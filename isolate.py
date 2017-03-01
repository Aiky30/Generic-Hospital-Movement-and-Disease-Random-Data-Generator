from config import *

import sys
import random
import csv
import radar


class Isolate:

    def __init__(self, movement):

        self.antibiogram_list = []
        self.movement = movement

        self.build_random_antibiogram_list()
        # get_antibiogram_list_from_file(ANTIBIOGRAM_SOURCE_FILE_LOCATION)

        self.create_output_file()

    def create_output_file(self):

        # Open file for writing
        try:
            # Open the file with option 'rU' Enable Universal newline support
            with open(OUTPUT_ISOLATE_FILENAME, 'w') as csvfile:

                writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_ISOLATE_HEADINGS)
                writer.writeheader()

                self.generate_isolate(writer)

        except IOError as err:
            print("Error in file writing", err)
            exit(1)

    def generate_isolate(self, writer):

        for isolate in ISOLATE_LIST:

            # Randomly select an individual
            new_random_individual = random.choice(INDIVIDUAL_LIST)

            # Randomly select a sample type
            sample_type = random.choice(ISOLATE_SAMPLE_TYPE)

            # Generate an isolate id
            isolate_id = 'MPROS' + str(isolate)

            # Is the randomly selected individual an in patient
            if new_random_individual < len(self.movement):

                random_individual = self.movement[new_random_individual]

                random_individual_id = random_individual.get('individual')

                # randomly select a date within the individuals admissions
                random_date = radar.random_date(
                    start=random_individual.get('admissions')[0].get('admission_date'),
                    # FIXME: Getting 0 is a hack!!
                    stop=random_individual.get('admissions')[0].get('discharge_date'),
                    # FIXME: Getting 0 is a hack!!
                )

                building_sent_from_name = ISOLATE_IN_PATIENT_SAMPLE_BUILDING
                building_sent_from_location = "unkown"

            # Otherwise the individual is an outpatient
            else:

                random_individual_id = new_random_individual

                # Generate a random date
                random_date = radar.random_date(
                    start=DATE_START,
                    stop=DATE_END
                )

                building_sent_from = random.choice(ISOLATE_OUT_PATIENT_SAMPLE_BUILDING)

                building_sent_from_name = building_sent_from.get('name')
                building_sent_from_location = random.choice(building_sent_from.get('locations'))

            # Randomly select an antibiogram result set
            random_antibiogram = random.choice(self.antibiogram_list)

            current_row = {
                'AnonPtNo': random_individual_id,
                'DateSent': random_date.strftime(ISOLATE_DATE_FORMAT),
                'Originaldescription': random.choice(ISOLATE_SAMPLE_DESCRIPTION),
                'Sampletype': sample_type,
                'SampleID': isolate_id,
                'GPHospital': building_sent_from_name,
                'Location': building_sent_from_location
            }

            for antibiotic in ANTIBIOGRAM_ANTIBIOTICS:
                current_row.update({
                    antibiotic: random_antibiogram.get(antibiotic)
                })

            writer.writerow(current_row)


    def build_random_antibiogram_list(self):

        # Build a list of usable antibiograms
        for index in ANTIBIOGRAM_RESULT_BANK:

            antibiogram = {}

            # For each antibiogram antibiotic
            for antibiotic in ANTIBIOGRAM_ANTIBIOTICS:

                # Allocate a random result to the antibiotic
                antibiogram[antibiotic] = random.choice(ANTIBIOGRAM_ANTIBIOTIC_VALUES)

            self.antibiogram_list.append(antibiogram)

    def get_antibiogram_list_from_file(self, filename):

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

                    self.antibiogram_list.append(row_data)

        except IOError as err:
            sys.exit(err)
