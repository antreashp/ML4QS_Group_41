##############################################################
#                                                            #
#    Mark Hoogendoorn and Burkhardt Funk (2017)              #
#    Machine Learning for the Quantified Self                #
#    Springer                                                #
#    Chapter 2                                               #
#                                                            #
##############################################################

# Import the relevant classes.
from Chapter2.CreateDataset import CreateDataset
from util.VisualizeDataset import VisualizeDataset
from util import util
from pathlib import Path
import copy
import os
import sys

# Chapter 2: Initial exploration of the dataset.

"""
First, we set some module-level constants to store our data locations. These are saved as a pathlib.Path object, the
preferred way to handle OS paths in Python 3 (https://docs.python.org/3/library/pathlib.html). Using the Path's methods,
you can execute most path-related operations such as making directories.

sys.argv contains a list of keywords entered in the command line, and can be used to specify a file path when running
a script from the command line. For example:

$ python3 crowdsignals_ch2.py my/proj/data/folder my_dataset.csv

If no location is specified, the default locations in the else statement are chosen, which are set to load each script's
output into the next by default.
"""
user = 'user_1'
# user = 'user_2'
# user = 'user_3'
# DATASET_PATH = Path(sys.argv[1] if len(sys.argv) > 1 else '../csv-participant-one/')
DATASET_PATH = Path(sys.argv[1] if len(sys.argv) > 1 else '../my_dataset/'+user+'/')
RESULT_PATH = Path('./intermediate_datafiles/'+user+'/')
RESULT_FNAME = sys.argv[2] if len(sys.argv) > 2 else 'chapter2_result.csv'

# Set a granularity (the discrete step size of our time series data). We'll use a course-grained granularity of one
# instance per minute, and a fine-grained one with four instances per second.
GRANULARITIES = [250]

# We can call Path.mkdir(exist_ok=True) to make any required directories if they don't already exist.
[path.mkdir(exist_ok=True, parents=True) for path in [DATASET_PATH, RESULT_PATH]]


datasets = []
for milliseconds_per_instance in GRANULARITIES:
    print(f'Creating numerical datasets from files in {DATASET_PATH} using granularity {milliseconds_per_instance}.')

    # Create an initial dataset object with the base directory for our data and a granularity
    dataset = CreateDataset(DATASET_PATH, milliseconds_per_instance)

    # Add the selected measurements to it.
    if user == 'user_2':
        dataset.add_numerical_dataset('accelerometer_phone.csv', 'timestamps', ['x','y','z'], 'avg', 'acc_phone_')
        dataset.add_numerical_dataset('proximity_phone.csv', 'timestamps', ['distance'], 'avg', 'prox_phone_')
        dataset.add_event_dataset('labels.csv', 'label_start', 'label_end', 'label', 'binary')
        dataset = dataset.data_table

        # Plot the data
        DataViz = VisualizeDataset(__file__,user)

        # Boxplot
        DataViz.plot_dataset_boxplot(dataset, ['acc_phone_x','acc_phone_y','acc_phone_z'])
        print(dataset)
        print(dataset.shape)
        # Plot all data

        DataViz.plot_dataset(dataset, ['acc_','prox_phone_' , 'label'],
                                    ['like', 'like', 'like', 'like'],
                                    ['line','line', 'points', 'points' ])

    else:
        dataset.add_numerical_dataset('accelerometer_phone.csv', 'timestamps', ['x','y','z'], 'avg', 'acc_phone_')
        dataset.add_numerical_dataset('proximity_phone.csv', 'timestamps', ['distance'], 'avg', 'prox_phone_')
        dataset.add_numerical_dataset('gyroscope_phone.csv', 'timestamps', ['x','y','z'], 'avg', 'gyr_phone_')
        dataset.add_numerical_dataset('light_phone.csv', 'timestamps', ['lux'], 'avg', 'light_phone_')
        dataset.add_numerical_dataset('magnetometer_phone.csv', 'timestamps', ['x','y','z'], 'avg', 'mag_phone_')
        dataset.add_numerical_dataset('pressure_phone.csv', 'timestamps', ['pressure'], 'avg', 'press_phone_')

        dataset.add_event_dataset('labels.csv', 'label_start', 'label_end', 'label', 'binary')
        dataset = dataset.data_table

        # Plot the data
        DataViz = VisualizeDataset(__file__,user)

        # Boxplot
        DataViz.plot_dataset_boxplot(dataset, ['acc_phone_x','acc_phone_y','acc_phone_z'])
        print(dataset)
        print(dataset.shape)
        # Plot all data

        DataViz.plot_dataset(dataset, ['acc_','prox_phone_' ,'gyr_phone_' ,'light_phone_' ,'mag_phone_' ,'press_phone_' , 'label'],
                                    ['like',      'like',      'like',        'like',       'like',        'like',        'like', 'like','like'],
                                    ['line',      'line',      'line',        'line',       'line',        'line',        'points','points', 'points' ])

    # We add the accelerometer data (continuous numerical measurements) of the phone and the smartwatch
    # and aggregate the values per timestep by averaging the values
    # dataset.add_numerical_dataset('accelerometer_smartwatch.csv', 'timestamps', ['x','y','z'], 'avg', 'acc_watch_')

    # We add the gyroscope data (continuous numerical measurements) of the phone and the smartwatch
    # and aggregate the values per timestep by averaging the values
    # dataset.add_numerical_dataset('gyroscope_smartwatch.csv', 'timestamps', ['x','y','z'], 'avg', 'gyr_watch_')

    # We add the heart rate (continuous numerical measurements) and aggregate by averaging again
    # dataset.add_numerical_dataset('heart_rate_smartwatch.csv', 'timestamps', ['rate'], 'avg', 'hr_watch_')

    # We add the labels provided by the users. These are categorical events that might overlap. We add them
    # as binary attributes (i.e. add a one to the attribute representing the specific value for the label if it
    # occurs within an interval).
    
    # We add the amount of light sensed by the phone (continuous numerical measurements) and aggregate by averaging
    # dataset.add_numerical_dataset('light_phone.csv', 'timestamps', ['lux'], 'avg', 'light_phone_')

    # We add the magnetometer data (continuous numerical measurements) of the phone and the smartwatch
    # and aggregate the values per timestep by averaging the values
    # dataset.add_numerical_dataset('magnetometer_phone.csv', 'timestamps', ['x','y','z'], 'avg', 'mag_phone_')
    # dataset.add_numerical_dataset('magnetometer_smartwatch.csv', 'timestamps', ['x','y','z'], 'avg', 'mag_watch_')

    # We add the pressure sensed by the phone (continuous numerical measurements) and aggregate by averaging again
    # dataset.add_numerical_dataset('pressure_phone.csv', 'timestamps', ['pressure'], 'avg', 'press_phone_')

    # Get the resulting pandas data table
    # And print a summary of the dataset.
    util.print_statistics(dataset)
    datasets.append(copy.deepcopy(dataset))

    dataset.to_csv(RESULT_PATH / RESULT_FNAME)
    # If needed, we could save the various versions of the dataset we create in the loop with logical filenames:
    # dataset.to_csv(RESULT_PATH / f'chapter2_result_{milliseconds_per_instance}')


# Make a table like the one shown in the book, comparing the two datasets produced.
# util.print_latex_table_statistics_two_datasets(datasets[0], datasets[1])

# Finally, store the last dataset we generated (250 ms).
