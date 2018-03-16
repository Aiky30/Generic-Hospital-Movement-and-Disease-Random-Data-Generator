import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


IN_PATIENT_COUNT = 3000
OUT_PATIENT_COUNT = 0

INDIVIDUAL_COUNT = IN_PATIENT_COUNT + OUT_PATIENT_COUNT
ISOLATE_COUNT = 150
ANTIBIOGRAM_RESULT_BANK_COUNT = 20
LOCATION_COUNT = 114

# TODO: Create outpatients that are recorded in the isolate file!!
# TODO: Make a percentage system where you say that x percent are in patients and x percent are outpatients
# TODO: Patient numbers should have a start auto increment value / prefix. NHS numbers are between 9 and 11 digits long

# Individual
INDIVIDUAL_LIST = range(1, INDIVIDUAL_COUNT)
IN_PATIENT_LIST = range(1, IN_PATIENT_COUNT)
OUT_PATIENT_LIST = range(IN_PATIENT_COUNT, INDIVIDUAL_COUNT)

# Location
LOCATION_AVG_COUNT = range(1, 4)  # (+/- 10%)
LOCATION_DURATION_PER_COUNT = 6  # In days

#FIXME: Some areas will have a higher value than others, i.e. A&E would have a different average duration!!
#       That would also affect how many locations the individual had, A&E wopuld be the only one for some etc.
# FIXME: Shouldn't be creating here

LOCATION_LIST = []
_location_prefix = "W"
for location in range(1, LOCATION_COUNT):
    LOCATION_LIST.append(_location_prefix + str(location))


# Admission
ADMISSION_MIN_DURATION = 1440 * 1  # In mins (calculated to days)
ADMISSION_MAX_DURATION = 1440 * 30  # In mins (calculated to days)
ADMISSION_AVG_COUNT = 1
ADMISSION_AVG_DURATION = range(ADMISSION_MIN_DURATION, ADMISSION_MAX_DURATION)

# Start and end dates
DATE_END = datetime.today() + timedelta(days=4)
DATE_START = DATE_END - relativedelta(years=1)

MOVEMENT_DATE_START = DATE_START
MOVEMENT_DATE_END = DATE_END - relativedelta(minutes=ADMISSION_MAX_DURATION)


# Date formats
DATE_FORMAT = "%m/%d/%y %H:%M"  # https://docs.python.org/2/library/datetime.html

ISOLATE_DATE_FORMAT = "%m/%d/%y"

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
#BASE_DIR = '/srv/www/development/imperial-college/gismoh-v2/backend/data/mrsa001_data'

# Output movement file
OUTPUT_MOVEMENT_HEADINGS = [
    'EpisodeAdmissionDate',
    'EpisodeDischargeDate',
    'SpellDischargeDate',
    'SpellAdmissionDate',
    'Ward',
    'AnonPtNo',
    'Hospital',
    'diagnostics',
]

OUTPUT_MOVEMENT_FILENAME = os.path.join(BASE_DIR, 'movement.csv')


# Output movement file
OUTPUT_ISOLATE_HEADINGS = [
    'AnonPtNo',
    'DateSent',
    'Originaldescription',
    'Sampletype',
    'SampleID',
    'GPHospital',
    'Location',
    'Benzylpenicillin',
    'Cefoxitin',
    'Oxacillin',
    'Ciprofloxacin',
    'Erythromycin',
    'Chloramphenicol',
]

ISOLATE_SAMPLE_DESCRIPTION = [
    'Multi site collection',
    'Intra-vascular catheter',
    'LEG',
    'FOOT',
    'SPUTUM',
    'TOE',
    'GROIN',
    'ABDOMEN',
]

ISOLATE_SAMPLE_TYPE = [
    'Screen',
    'Pus or swab, to be verified',
]

ISOLATE_IN_PATIENT_SAMPLE_BUILDING = "AddiesWards"

ISOLATE_OUT_PATIENT_SAMPLE_BUILDING = [
    {
        'name': 'AddiesDayUnit',
        'locations': [
            'Haematology DU Box 259',
        ]
    },
    {
        'name': 'Hinch',
        'locations': [
            'Hinch Procedure Unit',
        ]
    },
    {
        'name': 'GP',
        'locations': [
            'GP - SAWTRY, 45 High Street',
            'GP-BARLEY, The Surgery,High St',
        ]
    },
]

OUTPUT_ISOLATE_FILENAME = os.path.join(BASE_DIR, 'isolate.csv')


# Bacteria / disease

ISOLATE_LIST = range(1, ISOLATE_COUNT)

ANTIBIOGRAM_RESULT_BANK = range(0, ANTIBIOGRAM_RESULT_BANK_COUNT)

ANTIBIOGRAM_ANTIBIOTICS = [
    'Benzylpenicillin',
    'Cefoxitin',
    'Oxacillin',
    'Ciprofloxacin',
    'Erythromycin',
    'Chloramphenicol',
]

ANTIBIOGRAM_ANTIBIOTIC_VALUES = ['S', 'I', 'R']

"""
# Outbreak Simulator
"""

OUTBREAK_SIMULATOR_ADMISSION_CUT_OFF_DATE = DATE_START + relativedelta(months=10)

# Randomly select an individual
# If True loop indefinitely until a match is found
# If False loop through the individuals in the order that they were created until a match is found
OUTBREAK_SIMULATOR_RANDOM_INDIVIDUAL_SELECTION = True

#OUTBREAK_SIMULATOR_IDEAL_INFECTION_COUNT_MIN = 40
#OUTBREAK_SIMULATOR_IDEAL_INFECTION_COUNT_MAX = 100

OUTPUT_OUTBREAK_REPORT_FILENAME = os.path.join(BASE_DIR, 'outbreak.csv')

OUTPUT_OUTBREAK_HEADINGS = [
    'source_individual',
    'individual',
    'location',
    'date_of_infection',
    'level'
]

# FIXME: Requires plumbing!!
# TODO: Could be a range and randomly selected max / min multiplier
DISEASE_CALC_LIST = range(1, 10)
DISEASE_SEVERITY = 2  # Range is determined by DISEASE_CALC_LIST where 1 is low and 10 is high severity

SOURCE_INDIVIDUAL_MIN_LOCATION_COUNT = 2