import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


IN_PATIENT_COUNT = 2000
OUT_PATIENT_COUNT = 1000

INDIVIDUAL_COUNT = IN_PATIENT_COUNT + OUT_PATIENT_COUNT
ISOLATE_COUNT = 2500
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
LOCATION_AVG_COUNT = range(1, 3)  # (+/- 10%)
LOCATION_DURATION_PER_COUNT = 14  # In days

#FIXME: Some areas will have a higher value than others, i.e. A&E would have a different average duration!!
#       That would also affect how many locations the individual had, A&E wopuld be the only one for some etc.
# FIXME: Shouldn't be creating here

LOCATION_LIST = []
_location_prefix = "W"
for location in range(1, LOCATION_COUNT):
    LOCATION_LIST.append(_location_prefix + str(location))


# Admission
ADMISSION_MIN_DURATION = 1440 * 1  # In mins (calculated to days)
ADMISSION_MAX_DURATION = 1440 * 50  # In mins (calculated to days)
ADMISSION_AVG_COUNT = 1
ADMISSION_AVG_DURATION = range(ADMISSION_MIN_DURATION, ADMISSION_MAX_DURATION)

# Global
DATE_END = datetime.today() - relativedelta(minutes=ADMISSION_MAX_DURATION)
DATE_START = DATE_END - relativedelta(years=1)
DATE_FORMAT = "%m/%d/%y %H:%M"  # https://docs.python.org/2/library/datetime.html

ISOLATE_DATE_FORMAT = "%m/%d/%y"

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
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

OUTPUT_MOVEMENT_FILENAME = os.path.join(BASE_DIR, 'Movemt_MT.csv')


# Output movement file
OUTPUT_ISOLATE_HEADINGS = [
    'AnonPtNo',
    'DateSent',
    'Originaldescription',
    'Sampletype',
    'SampleID',
    'GPHospital',
    'Location',
    'VitekMICBenzylpenicillin',
    'VitekSRBenzylpenicillin',
    'VitekMICCefoxitin',
    'VitekSRCefoxitin',
    'VitekMICOxacillin',
    'VitekSROxacillin',
    'VitekMICCiprofloxacin',
    'VitekSRCiprofloxacin',
    'VitekMICErythromycin',
    'VitekSRErythromycin',
    'VitekMICChloramphenicol',
    'VitekSRChloramphenicol',
    'VitekMICDaptomycin',
    'VitekSRDaptomycin',
    'VitekMICFusidicAcid',
    'VitekSRFusidicAcid',
    'VitekMICGentamicin',
    'VitekSRGentamicin',
    'VitekMICLinezolid',
    'VitekSRLinezolid',
    'VitekMICMupirocin',
    'VitekSRMupirocin',
    'VitekMICNitrofurantoin',
    'VitekSRNitrofurantoin',
    'VitekMICRifampicin',
    'VitekSRRifampicin',
    'VitekMICTeicoplanin',
    'VitekSRTeicoplanin',
    'VitekMICTetracycline',
    'VitekSRTetracycline',
    'VitekMICTigecycline',
    'VitekSRTigecycline',
    'VitekMICTrimethoprim',
    'VitekSRTrimethoprim',
    'VitekMICVancomycin',
    'VitekSRVancomycin',
    'VitekMICClindamycin',
    'VitekSRClindamycin',
    'VitekMICInducibleClindResis',
    'VitekSRInducibleClindResis',
    'MeditechSRFlucloxacillin',
    'MeditechSRCiprofloxacin',
    'MeditechSRErythromycin',
    'MeditechSRFusidicAcid',
    'MeditechSRGentamicin',
    'MeditechSRTetracycline',
    'MeditechSRVancomycin',
    'MeditechSRMupirocin',
    'MeditechSRRifampicin',
    'MeditechSRNeomycin',
    'MeditechSRLinezolid',
    'MeditechSRChloramphenicol',
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

OUTPUT_ISOLATE_FILENAME = os.path.join(BASE_DIR, 'Isolate_MT.csv')


# Bacteria / disease

ISOLATE_LIST = range(1, ISOLATE_COUNT)

ANTIBIOGRAM_RESULT_BANK = range(0, ANTIBIOGRAM_RESULT_BANK_COUNT)

ANTIBIOGRAM_ANTIBIOTICS = [
    'VitekSRBenzylpenicillin',
    'VitekSRCefoxitin',
    'VitekSROxacillin',
    'VitekSRCiprofloxacin',
    'VitekSRErythromycin',
    'VitekSRChloramphenicol',
    'VitekSRDaptomycin',
    'VitekSRFusidicAcid',
    'VitekSRGentamicin',
    'VitekSRLinezolid',
    'VitekSRMupirocin',
    'VitekSRNitrofurantoin',
    'VitekSRRifampicin',
    'VitekSRTeicoplanin',
    'VitekSRTetracycline',
    'VitekSRTigecycline',
    'VitekSRTrimethoprim',
    'VitekSRVancomycin',
    'VitekSRClindamycin',
    'VitekSRInducibleClindResis',
    'MeditechSRFlucloxacillin',
    'MeditechSRCiprofloxacin',
    'MeditechSRErythromycin',
    'MeditechSRFusidicAcid',
    'MeditechSRGentamicin',
    'MeditechSRTetracycline',
    'MeditechSRVancomycin',
    'MeditechSRMupirocin',
    'MeditechSRRifampicin',
    'MeditechSRNeomycin',
    'MeditechSRLinezolid',
    'MeditechSRChloramphenicol',
]

ANTIBIOGRAM_ANTIBIOTIC_VALUES = ['S', 'I', 'R']
