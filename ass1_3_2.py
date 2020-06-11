#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 22:02:21 2020

@author: bajro
"""

##############################################################
#                                                            #
#    Mark Hoogendoorn and Burkhardt Funk (2018)              #
#    Machine Learning for the Quantified Self                #
#    Springer                                                #
#    Chapter 3                                               #
#                                                            #
##############################################################

from util.VisualizeDataset import VisualizeDataset
from OutlierDetection import DistributionBasedOutlierDetection
from OutlierDetection import DistanceBasedOutlierDetection
import sys
import copy
import pandas as pd
import numpy as np
from pathlib import Path


def main():

    # Set up file names and locations.
    DATA_PATH = Path('./intermediate_datafiles/')
    DATASET_FNAME = sys.argv[1] if len(sys.argv) > 1 else 'chapter2_result.csv'
    RESULT_FNAME = sys.argv[2] if len(sys.argv) > 2 else 'chapter3_result_outliers.csv'

    # Next, import the data from the specified location and parse the date index.
    try:
        dataset = pd.read_csv(Path(DATA_PATH / DATASET_FNAME), index_col=0)
        dataset.index = pd.to_datetime(dataset.index)

    except IOError as e:
        print('File not found, try to run the preceding crowdsignals scripts first!')
        raise e

    DataViz = VisualizeDataset(sys.argv[0])

    # Compute the number of milliseconds covered by an instance using the first two rows.
    milliseconds_per_instance = (dataset.index[1] - dataset.index[0]).microseconds/1000

    # Step 1: Let us see whether we have some outliers we would prefer to remove.

    # Determine the columns we want to experiment on.
    outlier_columns = ['acc_phone_x']

    # Create the outlier classes.
    OutlierDistr = DistributionBasedOutlierDetection()
    OutlierDist = DistanceBasedOutlierDetection()

    # And investigate the approaches for all relevant attributes.
    for col in outlier_columns:

        print(f"Applying outlier criteria for column {col}")


        # And try out all different approaches. Note that we have done some optimization
        # of the parameter values for each of the approaches by visual inspection.
        #for c in [0.5, 1, 2, 10]:
        #    res = OutlierDistr.chauvenet(dataset, col, c)
        #    print(res)
        for c in [2, 3, 5, 10]:
            for i in [1, 20, 100]:
                dataset = OutlierDistr.mixture_model(dataset, col, c, i)
                DataViz.plot_dataset(dataset, [col, col + '_mixture_' + str(c)+'_'+str(i)], ['exact','exact'], ['line', 'points'])

        # This requires:
        # n_data_points * n_data_points * point_size =
        # 31839 * 31839 * 32 bits = ~4GB available memory
        
        #for i,j in [(0.10, 0.99), (0.20, 0.99), (0.10, 0.90), (0.20, 0.90)]:
        #    try:
        #        res = OutlierDist.simple_distance_based(dataset, [col], 'euclidean', i, j)
        #        print(i, j, res)
        #    except MemoryError as e:
        #        print('Not enough memory available for simple distance-based outlier detection...')
        #        print('Skipping.')

        for i in [3,5]:
            try:
                dataset = OutlierDist.local_outlier_factor(dataset, [col], 'euclidean', i)
                DataViz.plot_dataset(dataset, [col, 'lof'+str(i)], ['exact','exact'], ['line', 'points'])
            except MemoryError as e:
                print('Not enough memory available for lof...')
                print('Skipping.')


        # Remove all the stuff from the dataset again.
        cols_to_remove = [col + '_outlier', col + '_mixture', 'simple_dist_outlier', 'lof']
        for to_remove in cols_to_remove:
            if to_remove in dataset:
                del dataset[to_remove]

    # We take Chauvenet's criterion and apply it to all but the label data...

    for col in [c for c in dataset.columns if not 'label' in c]:
        print(f'Measurement is now: {col}')
        dataset = OutlierDistr.chauvenet(dataset, col)
        dataset.loc[dataset[f'{col}_outlier'] == True, col] = np.nan
        del dataset[col + '_outlier']

    dataset.to_csv(DATA_PATH / RESULT_FNAME)

if __name__ == '__main__':
    main()