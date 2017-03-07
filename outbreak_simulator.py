from config import *

import random
import csv
import radar

from dateutil.relativedelta import relativedelta


OUTPUT_OUTBREAK_REPORT_FILENAME = os.path.join(BASE_DIR, 'Outbreak.csv')

OUTPUT_OUTBREAK_HEADINGS = [
    'source_individual',
    'individual',
    'location',
    'date_of_infection'
]

# FIXME: Requires plumbing!!
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

    return {
        'start': overlap_start,
        'end': overlap_end
    }

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

class Stats:

    def __init__(self):
        self.isolate_count = 1

    def add_isolate(self):
        self.isolate_count += 1


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

        # A list of all of those who have been infected and canoot be re infected!!
        self.infected_individuals = []

        self.stats = Stats()

        self.create_output_file()

        self.outbreak_results

        self.writer

    def get_output(self):
        return self.outbreak_results

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

    # Only choose an individual that has had locations or else this oubreak is useless!!
    def choose_suitable_individual(self, min_locations=3):

        individual_lottery = True

        while individual_lottery:

            individual = random.choice(self.movement.individual_list)

            # Check that the individual has locations making it a suitable candidate
            if len(individual.location_list) >= min_locations:
                return individual

    def create_outbreak_source(self):

        #FIXME: USe the antibiogram object helpers!!
        chosen_antibiogram = random.choice(ANTIBIOGRAM_RESULT_BANK)

        chosen_individual = self.choose_suitable_individual()

        chosen_individual_id = chosen_individual.id
        # Randomly choose a location to start the outbreak
        chosen_location = random.choice(chosen_individual.location_list)

        # Pick a date to start the outbreak
        date_of_infection = radar.random_date(
            start=chosen_location.admission_date,
            stop=chosen_location.discharge_date,
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
            'location': chosen_location.name,
            'date_of_infection': date_of_infection
        })

    def individual_already_part_of_outbreak(self, source_individual, current_individual, outbreak_results):

        """
        Check to see if the current individual has been part of an outbreak before
        """
        for outbreak_case in outbreak_results:

            outbreak_individual = outbreak_case['individual'].id
            outbreak_source = outbreak_case.get('source_individual')

            # The source is different but the individual has been infected before
            if current_individual == outbreak_individual and source_individual != outbreak_source:
                return True

        return False

    def initiate_outbreak_phase(self, previous_phase_output):

        current_phase_output = []
        outbreak_results = []
        outbreak_in_progress = True

        while outbreak_in_progress:

            for source in previous_phase_output:

                source_individual_id = source.get('individual').id
                print("New source %s" % source_individual_id)

                # Check to see if this individual has already been a source of infection
                if source_individual_id in self.infected_individuals:
                    continue

                # Record the source so that they cannot be re-infected
                self.infected_individuals.append(source_individual_id)

                #FIXME: Switch the loop on individual and locations so you can break out of the iondividual and save process time

                # get all individuals who have shared the locations at the same time
                for individual in self.movement.individual_list:

                    current_individual_id = individual.id

                    # Check if the individual has already been infected (different to the source check!!)
                    uptodate_outbreak_list = outbreak_results + current_phase_output
                    if self.individual_already_part_of_outbreak(source_individual_id, current_individual_id, uptodate_outbreak_list):
                        continue

                    # for each of the sources locations
                    for location in source['individual'].location_list:
                        location_name = location.name
                        location_start = location.admission_date
                        location_end = location.discharge_date

                        # For each of the current individuals locations
                        for curr_location in individual.location_list:

                            if (curr_location.name == location_name and
                                    two_date_blocks_overlap(location_start, location_end,
                                                            curr_location.admission_date,
                                                            curr_location.discharge_date)):

                                # Find the time slot of the overlap
                                overlap = two_date_blocks_calculate_overlap(location_start, location_end,
                                                                            curr_location.admission_date,
                                                                            curr_location.discharge_date)

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
                                        'source_individual': source_individual_id,
                                        'individual': individual,  # Individual object
                                        'location': curr_location.name,
                                        'date_of_infection': date_of_transmission,
                                        'overlap_start': overlap.get('start'),
                                        'overlap_end': overlap.get('end'),
                                    })

                                    self.writer.writerow({
                                        'source_individual': source_individual_id,
                                        'individual': current_individual_id,
                                        'location': curr_location.name,
                                        'date_of_infection': date_of_transmission
                                    })

                                    self.stats.add_isolate()

            # if the outbreak has finished
            if not current_phase_output:
                outbreak_in_progress = False
            else:
                # store the result
                outbreak_results = outbreak_results + current_phase_output

            # Set the next phase for another pass if required
            previous_phase_output = current_phase_output
            # Initialise current as empty
            current_phase_output = []

        return outbreak_results

    def create_outbreak(self):

        self.create_outbreak_source()

        self.outbreak_results = self.initiate_outbreak_phase([self.outbreak_source])

        print(self.stats.isolate_count)

