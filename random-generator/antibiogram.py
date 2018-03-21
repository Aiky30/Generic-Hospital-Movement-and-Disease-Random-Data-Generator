import config

import random
import csv
import sys

class Antibiogram:
    """
    """

    def __init__(self):

        self.antibiogram_list = self.build_random_antibiogram_list()

    def choose_random_antibiogram(self):
        return random.choice(self.antibiogram_list)

    def get_antibiogram_map(self, antibiogram, antibiotic_list):

        current_row = {}

        for antibiotic in antibiotic_list:
            current_row.update({
                antibiotic: antibiogram.get(antibiotic)
            })

        return current_row

    def build_random_antibiogram_list(self):

        antibiogram_list = []

        # Build a list of usable antibiograms
        for index in config.ANTIBIOGRAM_RESULT_BANK:

            antibiogram = {}

            # For each antibiogram antibiotic
            for antibiotic in config.ANTIBIOGRAM_ANTIBIOTICS:
                # Allocate a random result to the antibiotic
                antibiogram[antibiotic] = random.choice(config.ANTIBIOGRAM_ANTIBIOTIC_VALUES)

            antibiogram_list.append(antibiogram)

        return antibiogram_list

    def get_antibiogram_list_from_file(self, filename):
        # Open file for reading
        try:
            # Open the file with option 'rU' Enable Universal newline support
            with open(filename, 'rU') as csvfile:

                reader = csv.DictReader(csvfile)

                # Load the file into memory (FIXME: this won't work for big data sets)
                # mapped_data = []

                for row in reader:

                    row_data = {}

                    for heading in config.ANTIBIOGRAM_SOURCE_FILE_HEADINGS:
                        row_data.update({
                            heading: row[heading]
                        })

                    self.antibiogram_list.append(row_data)

        except IOError as err:
            sys.exit(err)
