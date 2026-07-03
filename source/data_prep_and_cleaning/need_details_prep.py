import pandas as pd
import logging

logger = logging.getLogger(__name__)

def create_1a_need_details_df(tab_1a_non_ag, tab_1a_errored_rows):
    logger.info("Creating 1A need details dataframe.")
    tab_1a_need_details = tab_1a_non_ag[tab_1a_non_ag['Proposed Target from Mapping'] == 'No Target']
    tab_1a_need_details = tab_1a_need_details.drop(columns=['LE-OG-AC', 'Proposed Target from Mapping']) # Check later
    
    tab_1a_need_details = pd.concat([tab_1a_need_details, tab_1a_errored_rows], ignore_index=True)
    tab_1a_need_details.reset_index(drop=True, inplace=True)
    return tab_1a_need_details

def create_1b_need_details_df(tab_1b):
    logger.info("Creating 1B need details dataframe.")
    
    if tab_1b.empty:
        logger.info("tab 1B is empty. Returning an empty DataFrame with the original structure.")
        
        return pd.DataFrame(
            columns=[col for col in tab_1b.columns if col not in ['LE', 'OG', 'AC', 'Acc Group?']]
            )
        
    tab_1b_need_details = tab_1b[tab_1b['Acc Group?'] == False]
    tab_1b_need_details = tab_1b_need_details.drop(columns=['LE', 'OG', 'AC', 'Acc Group?'])
    
    return tab_1b_need_details

def consolidate_need_details_dfs(tab_1a_need_details, tab_1b_need_details):
    logger.info("Consolidating need details dataframes and splitting by regions.")
    
    headers_to_add = [
        'Group/Individual', 
        'Existing group (Yes/No/NA)', 
        'Existing Group Name',
        'New Group Name', 
        'Override Frequency', 
        'Frequency', 
        'Risk rating',
        'Preparer User ID', 
        'Reviewer 1 User ID', 
        'Reviewer 2 User ID'
    ]
    
    need_details = pd.concat(
        [tab_1a_need_details, tab_1b_need_details], 
        axis=0, ignore_index=True)
    
    need_details_na = need_details[need_details['Account ID'].str.startswith(('1', '2'))]
    need_details_cala = need_details[need_details['Account ID'].str.startswith('3')]
    need_details_apac = need_details[need_details['Account ID'].str.startswith('4')]
    need_details_emea = need_details[need_details['Account ID'].str.startswith('5')]
    
    def add_headers(df):
        new_columns = {header: pd.NA for header in headers_to_add}
        
        return df.assign(**new_columns)
    
    need_details_na = add_headers(need_details_na)
    need_details_cala = add_headers(need_details_cala)
    need_details_apac = add_headers(need_details_apac)
    need_details_emea = add_headers(need_details_emea)
    
    return need_details, need_details_na, need_details_cala, need_details_apac, need_details_emea 

