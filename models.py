class Location:
    def __init__(self, name="", admission_date=None, discharge_date=None):
        self.name = name
        self.admission_date = admission_date
        self.discharge_date = discharge_date

class Isolate:
    def __init__(self, id=None):
        self.id = 'MPROS' + str(id)
        self.individual_id = None
        self.sample_type = None
        self.sample_description = None
        self.date_sent = None
        self.sent_from_location = None
        self.sent_from_name = None
        self.antibiogram = None


class Admission:
    def __init__(self, admission_date=None, discharge_date=None):
        self.admission_date = admission_date
        self.discharge_date = discharge_date

class Individual:

    def __init__(self, id=None):

        self.id = id

        self.location_list = []
        self.admission_list = []

    def add_location(self, location):
        self.location_list.append(location)

    def add_admission(self, admission):
        self.admission_list.append(admission)


