import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Individual - Note count must either
INDIVIDUAL_COUNT = 1000
INDIVIDUAL_LIST = range(1, INDIVIDUAL_COUNT)

# Location
LOCATION_AVG_COUNT = range(1, 3)  # (+/- 10%)
LOCATION_DURATION_PER_COUNT = 14  # In days

#FIXME: Some areas will have a higher value than others, i.e. A&E would have a different average duration!!
#       That would also affect how many locations the individual had, A&E wopuld be the only one for some etc.
LOCATION_LIST = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11', 'W12', 'W13', 'W14', 'W15', 'W16',
                 'W17', 'W18', 'W19', 'W20', 'W21', 'W22', 'W23', 'W24']

# Admission
ADMISSION_MIN_DURATION = 1440 * 1 # In mins (calculated to days)
ADMISSION_MAX_DURATION = 1440 * 50 # In mins (calculated to days)
ADMISSION_AVG_COUNT = 1
ADMISSION_AVG_DURATION = range(ADMISSION_MIN_DURATION, ADMISSION_MAX_DURATION)

# Global
DATE_END = datetime.today() - relativedelta(minutes=ADMISSION_MAX_DURATION)
DATE_START = DATE_END - relativedelta(years=1)
DATE_FORMAT = "%d/%m/%Y %H:%M:%S"  # https://docs.python.org/2/library/datetime.html

ISOLATE_DATE_FORMAT = "%m/%d/%y"

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = '/srv/www/development/imperial-college/gismoh-v2/backend/data/mrsa001_data'

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
    'SampleID',
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

original_description = [
    'Multi site collection',
    'Intra-vascular catheter',
    'LEG',
    'FOOT',
    'SPUTUM',
    'TOE',
    'GROIN',
    'ABDOMEN',
]



OUTPUT_ISOLATE_FILENAME = os.path.join(BASE_DIR, 'Isolate_MT.csv')


# Bacteria / disease

ISOLATE_COUNT = range(1, 100)

ANTIBIOGRAM_RESULT_BANK = range(0,10)

ANTIBIOGRAM_RESULTS = []

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
]

ANTIBIOGRAM_ANTIBIOTIC_VALUES = ['S','I','R']



MASTER_COPY = []