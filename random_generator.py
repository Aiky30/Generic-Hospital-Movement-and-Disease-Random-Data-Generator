from config import *

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


import random
import csv
import radar


def build_antibiogram_list():
    # Build a list of usable antibiograms
    for index in ANTIBIOGRAM_RESULT_BANK:

        antibiogram={}

        # For each antibiogram antibiotic
        for antibiotic in ANTIBIOGRAM_ANTIBIOTICS:

            # Allocate a random result to the antibiotic
            antibiogram[antibiotic] = random.choice(ANTIBIOGRAM_ANTIBIOTIC_VALUES)

        ANTIBIOGRAM_RESULTS.append(antibiogram)

    print("ANTIBIOGRAM_RESULTS: %s", ANTIBIOGRAM_RESULTS)


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

    for individual in INDIVIDUAL_LIST:

        ###############
        # Admissions
        ###############

        # Number of admissions
        admission = 1
        admission_duration = random.choice(ADMISSION_AVG_DURATION)

        # Generate a random date between the specified time period
        admission_start_date = radar.random_date(
            start=DATE_START,
            stop=DATE_END
        )

        admission_end_date = admission_start_date + timedelta(minutes=admission_duration)
        #FIXME: Locations will be per admission!!

        ###############
        # LOCATIONS
        ###############

        # Dictate how many locations the admission should have
        location_count = random.choice(LOCATION_AVG_COUNT)

        #print("individual: %s location_count: %s" % (individual, location_count))
        #print("Admission start: %s, end: %s" % (admission_start_date.strftime(DATE_FORMAT), admission_end_date.strftime(DATE_FORMAT)))

        #FIXME: This requires an algorithm
        # Algorithm could contain

        # Define the duration of each location for the
        location_duration = admission_duration / location_count
        location_start_date = admission_start_date

        admissions=[]

        for locations_preselected in xrange(0, location_count):

            location_selected = random.choice(LOCATION_LIST)
            #location_days = random.choice(LOCATION_AVG_DURATION)

            tmp_location_start_date = location_start_date
            location_end_date = tmp_location_start_date + timedelta(minutes=location_duration)

            #print("location duration: %s, admission_days: %s, location_count: %s" % (location_duration, admission_duration, location_count) )
            #print("Location: %s, start: %s, end: %s" % (location_selected, location_start_date.strftime(DATE_FORMAT), location_start_date.strftime(DATE_FORMAT)))

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

        MASTER_COPY.append({
            'individual': individual,
            'admissions': admissions
        })

def generateIsolate(writer):

    for isolate in ISOLATE_COUNT:

        # Randomly select an individual
        random_individual = random.choice(MASTER_COPY)

        # Randomly select an antibiogram resutl set
        random_antibiogram = random.choice(ANTIBIOGRAM_RESULTS)

        # randomly select a date within the individuals admissions
        random_date = radar.random_date(
            start=random_individual.get('admissions')[0].get('admission_date'), #FIXME: Getting 0 is a hack!!
            stop=random_individual.get('admissions')[0].get('discharge_date'), #FIXME: Getting 0 is a hack!!
        )

        #TODO: Auto write the rows headings etc to the file rather than entering each manually here

        writer.writerow({
            'AnonPtNo': random_individual.get('individual'),
            'DateSent': random_date.strftime(ISOLATE_DATE_FORMAT),
            'Originaldescription': random.choice(original_description),
            'SampleID': 'MPROS' + str(isolate),
            'VitekSRBenzylpenicillin': random_antibiogram.get('VitekSRBenzylpenicillin'),
            'VitekSRCefoxitin': random_antibiogram.get('VitekSRCefoxitin'),
            'VitekSROxacillin': random_antibiogram.get('VitekSROxacillin'),
            'VitekSRCiprofloxacin': random_antibiogram.get('VitekSRCiprofloxacin'),
            'VitekSRErythromycin': random_antibiogram.get('VitekSRErythromycin'),
            'VitekSRChloramphenicol': random_antibiogram.get('VitekSRChloramphenicol'),
            'VitekSRDaptomycin': random_antibiogram.get('VitekSRDaptomycin'),
            'VitekSRFusidicAcid': random_antibiogram.get('VitekSRFusidicAcid'),
            'VitekSRGentamicin': random_antibiogram.get('VitekSRGentamicin'),
            'VitekSRLinezolid': random_antibiogram.get('VitekSRLinezolid'),
            'VitekSRMupirocin': random_antibiogram.get('VitekSRMupirocin'),
            'VitekSRNitrofurantoin': random_antibiogram.get('VitekSRNitrofurantoin'),
            'VitekSRRifampicin': random_antibiogram.get('VitekSRRifampicin'),
            'VitekSRTeicoplanin': random_antibiogram.get('VitekSRTeicoplanin'),
            'VitekSRTetracycline': random_antibiogram.get('VitekSRTetracycline'),
            'VitekSRTigecycline': random_antibiogram.get('VitekSRTigecycline'),
            'VitekSRTrimethoprim': random_antibiogram.get('VitekSRTrimethoprim'),
            'VitekSRVancomycin': random_antibiogram.get('VitekSRVancomycin'),
            'VitekSRClindamycin': random_antibiogram.get('VitekSRClindamycin'),
            'VitekSRInducibleClindResis': random_antibiogram.get('VitekSRInducibleClindResis'),
        })


def build_movement_file():

    # Open file for reading
    try:
        # Open the file with option 'rU' Enable Universal newline support
        with open(OUTPUT_MOVEMENT_FILENAME, 'w') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_MOVEMENT_HEADINGS)
            writer.writeheader()

            generate_movement(writer)

    except IOError as err:
        print("Error in file writing", err)


def build_isolate_file():

    # Open file for reading
    try:
        # Open the file with option 'rU' Enable Universal newline support
        with open(OUTPUT_ISOLATE_FILENAME, 'w') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_ISOLATE_HEADINGS)
            writer.writeheader()

            generateIsolate(writer)

    except IOError as err:
        print("Error in file writing", err)


def main():

    build_antibiogram_list()

    build_movement_file()

    build_isolate_file()

main()
