from config import *

import sys
import random
import csv
import radar


class Isolate:

    def __init__(self, movement, antibiogram):


        self.antibiogram = antibiogram
        self.movement = movement

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
            if new_random_individual < len(self.movement.individual_list):

                random_individual = self.movement.individual_list[new_random_individual]

                random_individual_id = random_individual.id

                # randomly select a date within the individuals admissions
                # Random admission
                random_admission = random.choice(random_individual.admission_list)

                random_date = radar.random_date(
                    start=random_admission.admission_date,
                    stop=random_admission.discharge_date,
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
            random_antibiogram = self.antibiogram.choose_random_antibiogram()

            current_row = {
                'AnonPtNo': random_individual_id,
                'DateSent': random_date.strftime(ISOLATE_DATE_FORMAT),
                'Originaldescription': random.choice(ISOLATE_SAMPLE_DESCRIPTION),
                'Sampletype': sample_type,
                'SampleID': isolate_id,
                'GPHospital': building_sent_from_name,
                'Location': building_sent_from_location
            }

            mapped_antibiogram = self.antibiogram.get_antibiogram_map(random_antibiogram, ANTIBIOGRAM_ANTIBIOTICS)

            current_row.update(mapped_antibiogram)

            writer.writerow(current_row)

