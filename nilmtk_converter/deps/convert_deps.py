import pandas as pd
import numpy as np
import re
import os
from os.path import join, isdir, isfile
from os import listdir
from sys import stdout
from nilmtk.utils import get_datastore
from nilmtk.datastore import Key
from nilmtk.measurement import LEVEL_NAMES
from nilmtk.utils import get_module_directory, check_directory_exists
from nilm_metadata import save_yaml_to_datastore
from functools import reduce

def convert_deps(deps_path, input_filename, output_filename, format='HDF'):    
    """
    Parameters
    ----------
    deps_path : str
        The root path of the DEPS dataset. 
        e.g 'C:/data/deps'
    input_filename : str
        The rawdata filename (including path and suffix).
        e.g 'C:/data/rawdata.csv'
    output_filename : str
        The destination HDF5 filename (including path and suffix).
        e.g 'C:/data/deps/DEPS_data.h5'
    format : str
        format of output. Either 'HDF' or 'CSV'. Defaults to 'HDF'
        
    Meters & Measurements :
    ----------
    Measurement assignment (idMeasurement) in rawdata to REDD format
    
    Measurements id's           Units           Meters Name
    14011 14012             --> W VAr       --> Main_RST 
    14001 14007 14014 14017 --> V A W VAr   --> Main_R 
    14002 14008 14015 14018 --> V A W VAr   --> Main_S
    14003 14009 14016 14019 --> V A W VAr   --> Main_T
    13001                   --> W           --> Lights_1
    13002                   --> W           --> Lights_2
    10003 10006 10014 10018 --> V A W VAr   --> HVAC_1 
    10002 10005 10013 10017 --> V A W VAr   --> HVAC_2
    10001 10004 10012 10016 --> V A W VAr   --> HVAC_4
    21001 21002 21003 21005 --> V A W VAr   --> Rack    
          
    Example
    ----------
    raw_data.csv (input_filename):
    --
    idMeasurement, UNIX_timestamp(tStampUTC), dataValue
    14011,         1583103600,                      123
    14012,         1583103600,                     -416
    14011,         1583103601,                      126
    14012,         1583103601,                     -416
    ...            ...                              ...
    14011,         1583535599,                      121
    14012,         1583535599,                     -411
    
    Outputs REDD format: deps_path/classroom1/ :
    --
    channel_1.dat: 
    1583103600 123 -416
    1583103600 126 -416
    ...        ...  ...  
    1583103600 121 -411
    --
    labels.dat:   
    1 Main_RST
    
    Output HDF5 file: output_filename.h5    
        
    """ 
    #--------------------------------------------------------------------
    # writed by Andrés Arias Silva 
    # Raw data converter to REDD format extracted from DEPS SQL database
    _deps_to_redd_format(deps_path, input_filename)
    #--------------------------------------------------------------------    
    
    def _deps_measurement_mapping_func(classroom_id, chan_id):
        
        if chan_id == 1:
            meas =([('power', 'active'), ('power', 'reactive')])
        elif chan_id >1 and chan_id <= 4:
            meas =([('voltage', ''), ('current', ''), ('power', 'active'), ('power', 'reactive')])
        elif chan_id > 4 and chan_id <= 6:
            meas =([('power', 'active')])
        elif chan_id > 6 and chan_id <= 10:
            meas =([('voltage', ''), ('current', ''), ('power', 'active'), ('power', 'reactive'),])
        else:
            raise NameError('incorrect channel number')
        return meas   
       
    # Open DataStore
    store = get_datastore(output_filename, format, mode='w')

    # Convert raw data to DataStore
    _convert(deps_path, store, _deps_measurement_mapping_func, 'Europe/Madrid')

#    s=join(get_module_directory(),
#                              'dataset_converters',
#                              'deps',
#                              'metadata')

    # Add metadata
    save_yaml_to_datastore(join(get_module_directory(), 
                              'dataset_converters', 
                              'deps', 
                              'metadata'),
                         store)
    store.close()

    print("Done converting DEPS data to HDF5!")
 
 
#----------------------------------------------------------------------------------------------------------------
# writed by Andrés Arias Silva   
def _deps_to_redd_format(deps_path, input_filename):
    """
    DEPS raw data converter to REDD format
    Raw data extracted direct from DEPS SQL database
    
    Parameters
    ----------
    deps_path : The root path of the DEPS dataset.
    input_filename : The rawdata filename (including path and suffix).
       
    """
    print("Converting " +input_filename+ " to REDD format...")

    # Load document csv
    df = pd.read_csv(input_filename, sep=',', low_memory=False)
    
    # Meters Names (labels)
    mets =  ['Main_RST', 'Main_R', 'Main_S', 'Main_T', 'Lights_1', 'Lights_2', 'HVAC_1', 'HVAC_2', 'HVAC_4', 'Rack'] 
    
    # Measurements for each meter
    meas = [[14011, 14012],                # Main_RST
            [14001, 14007, 14014, 14017],  # Main_R
            [14002, 14008, 14015, 14018],  # Main_S
            [14003, 14009, 14016, 14019],  # Main_T
            [13001],                       # Lights_1
            [13002],                       # Lights_2
            [10003, 10006, 10014, 10018],  # HVAC_1
            [10002, 10005, 10013, 10017],  # HVAC_2
            [10001, 10004, 10012, 10016],  # HVAC_4
            [21001, 21002, 21003, 21005]]  # Rack
    
    # Units
    units = [['W', 'VAr'],                 # Main_RST
             ['V', 'A', 'W', 'VAr'],       # Main_R
             ['V', 'A', 'W', 'VAr'],       # Main_S
             ['V', 'A', 'W', 'VAr'],       # Main_T
             ['W'],                        # Lights_1
             ['W'],                        # Lights_2
             ['V', 'A', 'W', 'VAr'],       # HVAC_1
             ['V', 'A', 'W', 'VAr'],       # HVAC_2
             ['V', 'A', 'W', 'VAr'],       # HVAC_4
             ['V', 'A', 'W', 'VAr']]       # Rack
    
    # Associates each measurement with a meter
    conditions=[]
    choices=[]
    for i in list(range((len(mets)))):
        cond=[]
        for j in list(range((len(meas[i])))):
            cond="df['idMeasurement']=="+str(meas[i][j])
            conditions.append(eval(cond))
            choices.append(mets[i])
            
    # creates 'meter' column and assigns meter to each measure
    df['meter'] = np.select(conditions, choices, default='-')
    
    # Assigns a multi-index based on meters and measures
    df.set_index(['meter', 'idMeasurement'], inplace=True)
    # Drops undefined measurements in meas[] and sorts indexes
    df.drop('-', level='meter', inplace=True)
    df.sort_index(inplace=True)
    
    # Generate one file for each meter (timestamp + one column per measure)
    data_dir = deps_path+'/classroom_1'   
    if not os.path.exists(data_dir): # Create target Directory if don't exist
        os.mkdir(data_dir)
        print("Directory " , data_dir , "Created ")
    else:
        print("Directory " , data_dir , "Already exists")
    
    df_m=[]
    labels=[]
    for i in list(range((len(mets)))):
        dfs=[]
        for j in list(range((len(meas[i])))):
            df_c=df.xs(meas[i][j], level='idMeasurement').copy() # Select and copy
            #************************************************************* 
            #*********** Calibration mainsRST W measurements *************
            if meas[i][j]==14011: 
                df_c['dataValue']+=150 #add 150 W to mains RST
            #*********** Calibration mainsR W measurements ***************
            if meas[i][j]==14014: 
                df_c['dataValue']+=50  #add 50 W to mains R
            #*********** Calibration mainsS W measurements ***************
            if meas[i][j]==14015: 
                df_c['dataValue']+=50  #add 50 W to mains S
            #*********** Calibration mainsT W measurements ***************
            if meas[i][j]==14016: 
                df_c['dataValue']+=50  #add 50 W to mains T
            #************************************************************* 
            #************ Lights 1 readings converted to W ***************
            if meas[i][j]==13001: 
                df_c['dataValue']*=8 #8*100 W
            #************ Lights 2 readings converted to W ***************
            if meas[i][j]==13002: 
                df_c['dataValue']*=5 #5*100 W
            #*************************************************************         
            df_c.rename(columns={'dataValue':units[i][j]+'_'+mets[i]}, inplace=True) #assign measure
            dfs.append(df_c)
        # Outer Join: measures are joined for each meter with same time
        df_final = reduce(lambda left,right: pd.merge(left, right, how='outer', on='UNIX_timestamp(tStampUTC)'), dfs)
        df_final.dropna(inplace=True) # Drop NaN values
        df_final.drop_duplicates(subset='UNIX_timestamp(tStampUTC)',inplace=True) # Drop duplicates timestamp
        df_m.append(df_final)
        labels.append([str(i+1),str(mets[i])])
        df_final.to_csv(data_dir+'/channel_'+str(i+1)+'.dat',sep=' ', index=False, header=False) # Export csv file
        print('           export data from '+str(mets[i])+' to channel_'+str(i+1)+'.dat')
        
    # Export Labels
    labels_df=pd.DataFrame(labels)
    labels_df.to_csv(data_dir+'/labels.dat',sep=' ', index=False, header=False)
    print('           export labels.dat')
    
    print("Done converting raw data to REDD format!")
    print(" ")
#----------------------------------------------------------------------------------------------------------------       
   

def _convert(input_path, store, measurement_mapping_func, tz, sort_index=True, drop_duplicates=False):
    """
    Parameters
    ----------
    input_path : str
        The root path of the DEPS dataset.
    store : DataStore
        The NILMTK DataStore object.
    measurement_mapping_func : function
        Must take these parameters:
            - classroom_id
            - chan_id
        Function should return a list of tuples e.g. [('power', 'active')]
    tz : str 
        Timezone e.g. 'US/Eastern'
    sort_index : bool
        Defaults to True
    drop_duplicates : bool
        Remove entries with duplicated timestamp (keeps the first value)
        Defaults to False for backwards compatibility.
    """
    
    check_directory_exists(input_path)

    # Iterate though all classrooms and channels
    classrooms = _find_all_classrooms(input_path)
    for classroom_id in classrooms:
        print("Loading data from 'Aula 2.2 Bis' to classroom N°", classroom_id, end=" ... Loading channels ")
        stdout.flush()
        chans = _find_all_chans(input_path, classroom_id)
        for chan_id in chans:
            print(chan_id, end=" ")
            stdout.flush()
            key = Key(building=classroom_id, meter=chan_id)
            measurements = measurement_mapping_func(classroom_id, chan_id)
            csv_filename = _get_csv_filename(input_path, key)
            df = _load_csv(csv_filename, measurements, tz, 
                sort_index=sort_index, 
                drop_duplicates=drop_duplicates
            )
            store.put(str(key), df)
        print()


def _find_all_classrooms(input_path):
    """
    Returns
    -------
    list of integers (classroom instances)
    """
    dir_names = [p for p in listdir(input_path) if isdir(join(input_path, p))]
    return _matching_ints(dir_names, r'^classroom_(\d)$')


def _find_all_chans(input_path, classroom_id):
    """
    Returns
    -------
    list of integers (channels)
    """
    classroom_path = join(input_path, 'classroom_{:d}'.format(classroom_id))
    filenames = [p for p in listdir(classroom_path) if isfile(join(classroom_path, p))]
    return _matching_ints(filenames, r'^channel_(\d\d?).dat$')


def _matching_ints(strings, regex):
    """Uses regular expression to select and then extract an integer from
    strings.

    Parameters
    ----------
    strings : list of strings
    regex : string
        Regular Expression.  Including one group.  This group is used to
        extract the integer from each string.

    Returns
    -------
    list of ints
    """
    ints = []
    p = re.compile(regex)
    for string in strings:
        m = p.match(string)
        if m:
            integer = int(m.group(1))
            ints.append(integer)
    ints.sort()
    return ints


def _get_csv_filename(input_path, key_obj):
    """
    Parameters
    ----------
    input_path : (str) the root path of the DEPS dataset
    key_obj : (nilmtk.Key) the classroom and channel to load

    Returns
    ------- 
    filename : str
    """
    assert isinstance(input_path, str)
    assert isinstance(key_obj, Key)

    # Get path
    classroom_path = 'classroom_{:d}'.format(key_obj.building)
    path = join(input_path, classroom_path)
    assert isdir(path)

    # Get filename
    filename = 'channel_{:d}.dat'.format(key_obj.meter)
    filename = join(path, filename)
    assert isfile(filename)

    return filename


def _load_csv(filename, columns, tz, drop_duplicates=False, sort_index=False):
    """
    Parameters
    ----------
    filename : str
    columns : list of tuples (for hierarchical column index)
    tz : str 
        e.g. 'US/Eastern'
    sort_index : bool
        Defaults to True
    drop_duplicates : bool
        Remove entries with duplicated timestamp (keeps the first value)
        Defaults to False for backwards compatibility.

    Returns
    -------
    pandas.DataFrame
    """
    # Load data
    df = pd.read_csv(filename, sep=' ', names=columns,
                     dtype={m:np.float32 for m in columns})
    
    # Modify the column labels to reflect the power measurements recorded.
    df.columns.set_names(LEVEL_NAMES, inplace=True)

    # Convert the integer index column to timezone-aware datetime 
    df.index = pd.to_datetime(df.index.values, unit='s', utc=True)
    df = df.tz_convert(tz)

    if sort_index:
        df = df.sort_index() # raw DEPS data isn't always sorted
        
    if drop_duplicates:
        dups_in_index = df.index.duplicated(keep='first')
        if dups_in_index.any():
            df = df[~dups_in_index]

    return df