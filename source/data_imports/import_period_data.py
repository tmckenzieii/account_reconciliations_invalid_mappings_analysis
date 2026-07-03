import pandas as pd
import logging

logger = logging.getLogger(__name__)

from tkinter.filedialog import askopenfilename

def import_invalid_mappings(): 
    logger.info("Invalid mappings file selection.")
    print("Select an invalid mappings file for import.")
    
    invalid_mappings_sheet = askopenfilename(
        filetypes=[("Excel files", "*.xlsx")]
        )
    invalid_mappings = pd.read_excel(
        invalid_mappings_sheet, engine='openpyxl'
        )
    
    return invalid_mappings

def import_fccs_mappings():
    logger.info("FCCS mappings file selection.")
    print("Select an FCCS mappings fine for import.") 
    
    fccs_maps_sheet = askopenfilename(
        filetypes=[("Excel files", "*.csv")]
        )
    fccs_maps = pd.read_csv(
        fccs_maps_sheet, 
        usecols=[0, 1]
        )
    
    fccs_maps = fccs_maps[
        fccs_maps.iloc[:, 0].str.startswith('LE')
        ]
    fccs_maps.columns = ['String', 'Target'] + list(fccs_maps.columns[2:])
    
    return fccs_maps

def import_profiles():
    logger.info("Profiles file selection.")
    print("Select a profiles file for import.") 
    
    profiles_sheet = askopenfilename(
        filetypes=[("Excel files", "*.csv")]
        )
    profiles = pd.read_csv(
        profiles_sheet, 
        usecols=[0,1,2,3,4,5,6,7,28]
        )
    
    profiles = profiles.rename(
        columns={
            'Profile Segment 1': 'LE', 
            'Profile Segment 2': 'OG', 
            'Profile Segment 3': 'AC', 
            'Profile Segment 4': 'DT', 
            'Profile Segment 5': 'ST', 
            'Profile Segment 6': 'PJ', 
            'Profile Segment 7': 'F1', 
            'Profile Segment 8': 'F2'}
        )
    
    profiles['DT'] = profiles['DT'].replace('0', '0000')
    profiles['OG'] = profiles['OG'].replace('0', '0000')
    profiles['PJ'] = profiles['PJ'].replace({'0': '0000', '12': '0012'})
    
    profiles['Joined Target'] = (
        profiles[['LE','OG','AC','DT','ST','PJ','F1','F2']]
        .fillna('')      
        .astype(str)         
        .agg('-'.join, axis=1)
        )
    
    return profiles

def import_role_assignment_report():
    logger.info("Role assignment report file selection.")
    print("Select a role assignment report for import.")
    
    role_assignment_sheet = askopenfilename(
        filetypes=[("Excel files", ".csv")]
        )
    role_assignment = pd.read_csv(role_assignment_sheet)
    
    return role_assignment

