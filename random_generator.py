from config import *

from movement import Movement
from antibiogram import Antibiogram
from isolate import IsolateRandomSimulator, IsolateOutput
from outbreak_simulator import OutbreakSimulator
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

"""

IDEA: Make one method of antibiogram more popular than others, some kind of percentage based allocation in the random selection.


Config for AB
"""

class MasterResultSet:
    def __init__(self):
        self.isolate_list = []

def main():

    master_resultset = MasterResultSet()


    antibiogram = Antibiogram()

    movement = Movement()

    outbreak = OutbreakSimulator(movement, antibiogram, master_resultset)

    # TODO: Link the outbreak data into the isolate file,
    #          the isolate file should add additional samples and also miss some, any missed should be recorded as missed to eliminate any unknowns

    IsolateRandomSimulator(movement, antibiogram, outbreak, master_resultset)

    IsolateOutput(antibiogram, master_resultset)

    """

        Isolate file writer takes the generated isolate list

        Generate movement
        Generate outbreak
        Generate isolates / samples from the outbreak data
        Generate random isolate list

        IsolateOutbreakSimulator
        IsolateRandomSimulator


        IsolateWriter writes out the completed list of isolates
    """

    exit(0)

if __name__ == "__main__":
    main()
