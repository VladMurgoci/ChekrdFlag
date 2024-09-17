from numpy import genfromtxt
import csv
import numpy as np
import os

def init_race_catalogue(year):
    np_data = np.zeros(2, dtype=int)
    np.savetxt(f"storage/race_catalog_{year}.csv", np_data, delimiter=',')
    return

def get_current_race_idx(year):
    file_name = f"storage/race_catalog_{year}.csv"
    try:
        data = np.genfromtxt(file_name, delimiter=",", dtype=int)
        return data[1]
    except FileNotFoundError:
        # If the file does not exist, create it and initialize a NumPy array
        init_race_catalogue(year)
        return 0

def get_current_qualy_idx(year):
    file_name = f"storage/race_catalog_{year}.csv"
    try:
        data = np.genfromtxt(file_name, delimiter=',', dtype=int)
        return data[0]
    except FileNotFoundError:
        init_race_catalogue(year)
        return 0

def fill_race(year, race_idx):
    """
    Fills the race txt pointer with the next race to be reported
    @param year: Year of the race
    @param race_idx: Index of the next race
    @return: null
    """
    file_name = f"storage/race_catalog_{year}.csv"
    if os.path.isfile(file_name):
        data = np.genfromtxt(file_name, delimiter=",", dtype=int)
        data[1] = race_idx
        np.savetxt(file_name, data, delimiter=",")
    else:
        init_race_catalogue(year)
        fill_race(year, race_idx)
    return

def fill_qualy(year, qualy_idx):
    file_name = f"storage/race_catalog_{year}.csv"
    if os.path.isfile(file_name):
        data = np.genfromtxt(file_name, delimiter=",", dtype=int)
        data[0] = qualy_idx
        np.savetxt(file_name, data, delimiter=",")
    else:
        init_race_catalogue(year)
        fill_qualy(year, qualy_idx)
    return