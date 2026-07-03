import pandas as pd 
import logging

logger = logging.getLogger(__name__)

def create_new_profile_need_wf_details(tab_1a_ag, tab_1b_ag):
    logger.info("Creating new profile need details dataframe.")
    
    columns_to_drop = [
        'LE', 
        'LE Clean', 
        'OG', 
        'AC', 
        'Acc Group?', 
        'Acc Desc', 
        'Acc Groups', 
        'Grouping', 
        'Proposed Target from Mapping'
        ]
    
    columns_to_add  = [
        'Preparer',
        'Preparer Email',
        'Reviewer 1',
        'Reviewer 1 Email',
        'Reviewer 2',
        'Reviewer 2 Email',
        'Preparer User ID',
        'Reviewer 1 User ID',
        'Reviewer 2 User ID'
        ]
    
    new_profile_need_wf_details_1a = tab_1a_ag[tab_1a_ag['Proposed Target from Mapping'] == 'No Target']
    new_profile_need_wf_details_1b = tab_1b_ag[tab_1b_ag['Proposed Target from Mapping'] == 'No Target']
    
    new_profile_need_wf_details = pd.concat([
        new_profile_need_wf_details_1a, 
        new_profile_need_wf_details_1b], axis=0
        )
    
    new_profile_need_wf_details = new_profile_need_wf_details.drop(columns=columns_to_drop, errors='ignore')
    new_profile_need_wf_details.reset_index(drop=True, inplace=True)

    for col_name in columns_to_add:
        new_profile_need_wf_details[col_name] = pd.NA
    
    return new_profile_need_wf_details