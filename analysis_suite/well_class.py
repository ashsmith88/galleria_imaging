"""
well_class.py file for analysis_suite

Contains a class for storing time series information on each well
"""
import pandas as pd
import numpy as np

class AllWells(object):
    """
    Class AllWells - contains information on all the wells

    Attributes
    ------
    wells : dict
        dictionary where keys are well numbers and values are instances of SingleWell
        object containing information on that well at each timepoint`
    dataframe : dict
        dictionary where keys are meausrement type and values are a pandas dataframe
        with the rows as each well and the columns as measurements at each timepoint
    tpoints : list
        chronological list of timepoints
    """

    def __init__(self):
        self.wells = {}
        self.dataframes = {}

    def add_well_info(self, well_num, tpoint= None, area_well = None, mean_fluo_well=None, total_fluo_well=None, melanisation=None,
                    area_gall=None, mean_fluo_gall=None, total_fluo_gall=None):
        """
        Adds information about a new well

        Parameters
        ------
        well_num : int
            The well number
        tpoint : int, optional
            timepoint for measurements
        area: int, optional
            the measured area
        mean_fluo : int, optional
            the measured mean fluorescence
        total_fluo : int, optional
            the measured integrated fluorescence
        melanisation : int, optional
            the median melanisation value (greyscale pixel value)
        """
        # create an instance of SingleWell for the well if it doesn't already exist
        if well_num not in self.wells.keys():
            self.wells[well_num] = SingleWell()
        # add the new data for that timepoint
        self.wells[well_num].add_tpoint_data(tpoint=tpoint, area_well=area_well, mean_fluo_well=mean_fluo_well, total_fluo_well=total_fluo_well, melanisation=melanisation,
                                            area_gall=area_gall, mean_fluo_gall=mean_fluo_gall, total_fluo_gall=total_fluo_gall)

    def create_dataframes(self):
        """
        Creates dataframes for each measurement based on the values in wells
        """
        # get the attributes in the SingleWell instance (each measurement)
        attributes = self.wells[1].__dict__.keys()
        for att in attributes:
            data_dict = {}
            # set the timepoints
            self.tpoints = sorted(self.wells[1].__dict__[att])
            for well in self.wells.keys():
                # add the measurement for each well for each timepoint to a list
                # empty tpoints set to np.nan - ## TODO: review if this is right
                data_dict[well] = [self.wells[well].__dict__[att][tpo] if tpo in self.wells[well].__dict__[att].keys() else np.nan for tpo in self.tpoints]
            # create dataframe for the dictionary
            self.dataframes[att] = pd.DataFrame.from_dict(data_dict, orient='index', columns=self.tpoints)


class SingleWell(object):
    """
    Contains timepoint data for a single well

    Attributes
    ------

    area_dict : dict
        a dictionary where each key is a timepoint and each value is the measured area
    mean_fluo_dict : dict
        a dictionary where each key is a timepoint and each value is the measured average fluorescence
    total_fluo_dict : dict
        a dictionary where each key is a timepoint and each value is the measured integrated fluorescence
    melanisation_median : dict
        a dictionary where each key is a timepoint and each value is the measured melanisation
    """

    def __init__(self):
        self.well_area_dict = {}
        self.well_mean_fluo_dict = {}
        self.well_total_fluo_dict = {}
        self.gall_area_dict = {}
        self.gall_mean_fluo_dict = {}
        self.gall_total_fluo_dict = {}
        self.melanisation_median = {}

    def add_tpoint_data(self, tpoint, area_well = None, mean_fluo_well=None, total_fluo_well=None, melanisation=None, area_gall=None, mean_fluo_gall=None, total_fluo_gall=None):
        """
        Adds data to the correct dictionary for the timepoint

        Parameters
        ------
        tpoint : int, optional
            timepoint for measurements
        area: int, optional
            the measured area
        mean_fluo : int, optional
            the measured mean fluorescence
        total_fluo : int, optional
            the measured integrated fluorescence
        melanisation : int, optional
            the median melanisation value (greyscale pixel value)
        """

        ### TODO: look into assigning this dynamically
        if area_well:
            self.well_area_dict[tpoint] = area_well
        if mean_fluo_well:
            self.well_mean_fluo_dict[tpoint] = mean_fluo_well
        if total_fluo_well:
            self.well_total_fluo_dict[tpoint] = total_fluo_well
        if area_gall:
            self.gall_area_dict[tpoint] = area_gall
        if mean_fluo_gall:
            self.gall_mean_fluo_dict[tpoint] = mean_fluo_gall
        if total_fluo_gall:
            self.gall_total_fluo_dict[tpoint] = total_fluo_gall
        if melanisation:
            self.melanisation_median[tpoint] = melanisation
