from config import *

#import sys
import random
import csv
import radar

from dateutil.relativedelta import relativedelta






#FIXME: Exclude individuals from being reused!!!!






OUTPUT_OUTBREAK_REPORT_FILENAME = os.path.join(BASE_DIR, 'Outbreak.csv')

OUTPUT_OUTBREAK_HEADINGS = [
    'source_individual',
    'individual',
    'location',
    'date_of_infection'
]

# TODO: Could be a range and randomly selected max / min multiplier
OUTBREAK_MULTIPLIER = 2  # The nth number of transmission


# TODO: Need the time that the overlap occured to better add an isolate date!!
# FIXME: Should be an external package!!
def two_date_blocks_overlap(master_start, master_end, test_start, test_end):

    # Has overlaps
    if((master_start < test_start < master_end) or
       (master_start < test_end < master_end) or
       (test_start < master_start < test_end)):
        return True

    # No overlaps
    return False


#FIXME: Requires unit tests and an external package
def two_date_blocks_calculate_overlap(master_start, master_end, test_start, test_end):

    overlap_start = max(master_start, test_start)
    overlap_end = min(master_end, test_end)

    print( overlap_start )
    print( overlap_end )

    return { 'start': overlap_start, 'end': overlap_end }

"""
def date_in_date_range(date, range_start, range_end):

    # is inbetween
    if((master_start < test_start < master_end) or
       (master_start < test_end < master_end) or
       (test_start < master_start < test_end)):
        return True

    # No overlaps
    return False
"""


class OutbreakSimulator:
    """
    An outbreak continues until the end date set

    """

    def __init__(self, movement):

        self.movement = movement

        # FIXME: Add to external config
        self.outbreak_start_date = DATE_START + relativedelta(days=1)
        self.outbreak_end_date = DATE_END - relativedelta(days=1)
        self.outbreak_source = {}

        self.antibiogram_list = self.build_random_antibiogram_list()

        self.create_output_file()

        # A list of all of those who have been infected and canoot be re infected!!
        self.infected_individuals = []

        self.writer
        #self.outbreak_report

    def create_output_file(self):

        # Open file for writing
        try:
            # Open the file with option 'rU' Enable Universal newline support
            with open(OUTPUT_OUTBREAK_REPORT_FILENAME, 'w') as csvfile:

                writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_OUTBREAK_HEADINGS)
                writer.writeheader()

                self.writer = writer

                self.create_outbreak()

        except IOError as err:
            print("Error in file writing", err)
            exit(1)

    def create_outbreak_source(self):

        chosen_antibiogram = random.choice(ANTIBIOGRAM_RESULT_BANK)
        chosen_individual_id = random.choice(INDIVIDUAL_LIST)
        chosen_individual = {}

        #FIXME: Only choose an individual that has had locations or else this oubreak is useless!!

        # Get the chosen individuals movements
        for original_individual in self.movement:

            if chosen_individual_id == original_individual.get('individual'):
                chosen_individual = original_individual

        # Randomly choose a location to start the outbreak
        chosen_location = random.choice(chosen_individual.get('locations'))

        # Pick a date to start the outbreak
        date_of_infection = radar.random_date(
            start=chosen_location.get('admission_date'),
            stop=chosen_location.get('discharge_date'),
        )

        self.outbreak_source = {
            'antibiogram': chosen_antibiogram,
            'individual': chosen_individual,
            'location': chosen_location,
            'date_of_infection': date_of_infection
        }

        self.writer.writerow({
            'source_individual': chosen_individual_id,
            'individual': chosen_individual_id,
            'location': chosen_location.get('name'),
            'date_of_infection': date_of_infection
        })


    def initiate_outbreak_phase(self, source_list):

        previous_phase_output = source_list
        current_phase_output = []
        outbreak_results = []
        outbreak_in_progress = True

        while outbreak_in_progress:

            for source in previous_phase_output:

                # Record the source so that they cannot be re-infected
                self.infected_individuals = self.infected_individuals + source['individual'].get('individual')

                #FIXME: Switch the loop on individual and locations so you can break out of the iondividual and safe process time


                # for each of the sources locations
                for location in source['individual'].get('locations'):

                    location_name = location.get('name')
                    location_start = location.get('admission_date')
                    location_end = location.get('discharge_date')

                    # get all individuals who have shared the locations at the same time
                    for original_individual in self.movement:

                        # Check to see if this individual has already been a source of infection
                        if original_individual.get('individual') in self.infected_individuals:
                            continue

                        for curr_location in original_individual.get('locations'):

                            if (curr_location.get('name') == location_name and
                                    two_date_blocks_overlap(location_start, location_end,
                                                            curr_location.get('admission_date'),
                                                            curr_location.get('discharge_date'))
                                ):

                                # Find the time slot of the overlap
                                overlap = two_date_blocks_calculate_overlap(location_start, location_end,
                                                                            curr_location.get('admission_date'),
                                                                            curr_location.get('discharge_date'))

                                # Source individuals transmission date is the earliest date that a transmission can occur!!!
                                if source.get('date_of_infection') < overlap.get('start'):

                                    # Pick a date to simulate a transmission
                                    date_of_transmission = radar.random_date(
                                        start=overlap.get('start'),
                                        stop=overlap.get('end'),
                                    )

                                    # Pick a date within the overlap to create a sample date, this would be ideal to know but not
                                    # realistic in the real world, the date would be after.
                                    # TODO: Define a metric of delay between the date of transmission vs sample

                                    current_phase_output.append({
                                        'source_individual': source['individual'].get('individual'),
                                        'individual': original_individual,
                                        'location': curr_location.get('name'),
                                        'date_of_infection': date_of_transmission,
                                        'overlap_start': overlap.get('start'),
                                        'overlap_end': overlap.get('end'),
                                    })

                                    self.writer.writerow({
                                        'source_individual': source['individual'].get('individual'),
                                        'individual': original_individual.get('individual'),
                                        'location': curr_location.get('name'),
                                        'date_of_infection': date_of_transmission
                                    })

            if not current_phase_output:
                outbreak_in_progress = False
            else:
                # store the result
                outbreak_results = outbreak_results + current_phase_output

            # Set the next phase for another pass if required
            previous_phase_output = current_phase_output
            # Initialise current as empty
            current_phase_output = []



        # FIXME: Re run the code above with the output until no more can be output!!
        """

        if current_phase_output is empty
            break the loop
            the outbreak has finished
            the world is yours
        Else
            compiled_phases_output merged with current_phase_output
            Continue the loop with another pass, loading in the results from the last run (previous_phase_output)

        """
        return outbreak_results

    def create_outbreak(self):

        self.create_outbreak_source()

        outbreak_results = self.initiate_outbreak_phase([self.outbreak_source])

        print(outbreak_results)

    def build_random_antibiogram_list(self):

        antibiogram_list = []

        # Build a list of usable antibiograms
        for index in ANTIBIOGRAM_RESULT_BANK:

            antibiogram = {}

            # For each antibiogram antibiotic
            for antibiotic in ANTIBIOGRAM_ANTIBIOTICS:
                # Allocate a random result to the antibiotic
                antibiogram[antibiotic] = random.choice(ANTIBIOGRAM_ANTIBIOTIC_VALUES)

            antibiogram_list.append(antibiogram)

        return antibiogram_list