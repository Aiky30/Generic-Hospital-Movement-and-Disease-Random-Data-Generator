import config
from models import Isolate

import random
import csv
import radar

#FIXME: Somehow an individual who is set an isolate can be set muleiplte isolates. This should nto be possible!!


class IsolateRandomSimulator:

    def __init__(self, movement, antibiogram, outbreak, master_isolate_list):

        self.outbreak = outbreak
        self.antibiogram = antibiogram
        self.movement = movement
        self.isolate_list = master_isolate_list.isolate_list

        self.generate_isolates()

    def get_random_individual(self):
        individual_not_found = True

        while individual_not_found:

            # Randomly select an individual
            new_random_individual = random.choice(self.movement.individual_list)

            # Ensure that the individual is not part of an existing outbreak!!
            if new_random_individual.id not in self.outbreak.infected_individuals:
                return new_random_individual

    def generate_isolates(self):

        for isolate in config.ISOLATE_LIST:

            # Randomly select an individual
            random_individual = self.get_random_individual()
            random_individual_id = random_individual.id

            # Randomly select a sample type
            sample_type = random.choice(config.ISOLATE_SAMPLE_TYPE)

            # Generate an isolate id
            isolate_id = isolate

            # Is the randomly selected individual an in patient
            if random_individual_id < len(self.movement.individual_list):

                # randomly select a date within the individuals admissions
                # Random admission
                random_admission = random.choice(random_individual.admission_list)

                random_date = radar.random_date(
                    start=random_admission.admission_date,
                    stop=random_admission.discharge_date,
                )

                building_sent_from_name = config.ISOLATE_IN_PATIENT_SAMPLE_BUILDING
                building_sent_from_location = "unkown"

            # Otherwise the individual is an outpatient
            else:

                # Generate a random date
                random_date = radar.random_date(
                    start=config.DATE_START,
                    stop=config.DATE_END
                )

                building_sent_from = random.choice(config.ISOLATE_OUT_PATIENT_SAMPLE_BUILDING)

                building_sent_from_name = building_sent_from.get('name')
                building_sent_from_location = random.choice(building_sent_from.get('locations'))

            # Randomly select an antibiogram result set
            random_antibiogram = self.antibiogram.choose_random_antibiogram()

            new_isolate = Isolate(isolate_id)
            new_isolate.individual_id = random_individual_id
            new_isolate.sample_type = sample_type
            new_isolate.sample_description = random.choice(config.ISOLATE_SAMPLE_DESCRIPTION)
            new_isolate.date_sent = random_date
            new_isolate.sent_from_location = building_sent_from_location
            new_isolate.sent_from_name = building_sent_from_name
            new_isolate.antibiogram = random_antibiogram

            #mapped_antibiogram = self.antibiogram.get_antibiogram_map(random_antibiogram, ANTIBIOGRAM_ANTIBIOTICS)

            self.isolate_list.append(new_isolate)


class IsolateOutput:

    def __init__(self, antibiogram, master_resultset):

        self.antibiogram = antibiogram
        self.isolate_list = master_resultset.isolate_list

        self.create_output_file()

    def create_output_file(self):

        # Open file for writing
        try:
            # Open the file with option 'rU' Enable Universal newline support
            with open(config.OUTPUT_ISOLATE_FILENAME, 'w') as csvfile:

                writer = csv.DictWriter(csvfile, fieldnames=config.OUTPUT_ISOLATE_HEADINGS)
                writer.writeheader()

                self.write_output(writer)

        except IOError as err:
            print("Error in file writing", err)
            exit(1)

    def write_output(self, writer):

        for isolate in self.isolate_list:

            #FIXME: Method and organismshould be randomly selected!!
            current_row = {
                config.OUTPUT_ISOLATE_HEADING_MAPPING['patient_id']: isolate.individual_id,
                config.OUTPUT_ISOLATE_HEADING_MAPPING['date']: isolate.date_sent.strftime(config.ISOLATE_DATE_FORMAT),
                config.OUTPUT_ISOLATE_HEADING_MAPPING['sample_description']: isolate.sample_description,
                config.OUTPUT_ISOLATE_HEADING_MAPPING['sample_type']: isolate.sample_type,
                config.OUTPUT_ISOLATE_HEADING_MAPPING['sample_id']: isolate.id,
                config.OUTPUT_ISOLATE_HEADING_MAPPING['test_method']: "Method 1",
                config.OUTPUT_ISOLATE_HEADING_MAPPING['organism']: "Organism 1",
                #config.OUTPUT_ISOLATE_HEADING_MAPPING['sent_from_name']: isolate.sent_from_name,
                #config.OUTPUT_ISOLATE_HEADING_MAPPING['sent_from_location']: isolate.sent_from_location,
            }

            mapped_antibiogram = self.antibiogram.get_antibiogram_map(isolate.antibiogram, config.ANTIBIOGRAM_ANTIBIOTICS)

            current_row.update(mapped_antibiogram)

            writer.writerow(current_row)

