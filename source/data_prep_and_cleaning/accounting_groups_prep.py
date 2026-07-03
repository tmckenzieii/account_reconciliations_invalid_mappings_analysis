import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def accounting_group_prep(tab, global_acc, tab_name):
    logger.info(f"Checking {tab_name} data for accounting group overlap.")
    
    if not tab.empty:
        tab = tab.copy()
        tab['Acc Group?'] = tab['AC'].isin(global_acc['Future State - Account'])
    else:
        logger.info(f"{tab_name} is empty, skipping processing.")
    
    return tab

def create_accounting_groups_dfs(tab, global_acc, consolidated_pre_rev, profiles, tab_name):
    logger.info(f"Creating {tab_name} accounting group data.")
    
    if tab.empty:
        logger.info(f"{tab_name} is empty. Returning an empty dataframe.")
        return pd.DataFrame(
            columns=[
                'AC', 
                'Acc Groups', 
                'Acc Desc', 
                'Grouping', 
                'Proposed Target from Mapping'
            ]
        )

    tab_1x_ag = tab[tab['AC'].isin(global_acc['Future State - Account'])].copy()
    
    tab_1x_ag['Acc Groups'] = tab_1x_ag['AC'].map(
        global_acc.set_index('Future State - Account')['Wesco 1A Account Grouping Exceptions']
        )
    tab_1x_ag['Acc Desc'] = tab_1x_ag['Acc Groups'].map(
        consolidated_pre_rev.set_index('Account Group')['Account Description']
        )
    tab_1x_ag['Grouping'] = tab_1x_ag['Acc Groups'].map(
        consolidated_pre_rev.set_index('Account Group')['Grouping']
        )
    
    conditions = [
        (tab_1x_ag['Grouping'] == 'LE'),
        (tab_1x_ag['Grouping'] == 'LE & OG'),
        (tab_1x_ag['Grouping'] == 'Globally')
        ]
    
    choices = [
        tab_1x_ag['LE'].astype(str) 
        + '-XXXX-' 
        + tab_1x_ag['Acc Desc'].astype(str) 
        + '-XXXX-XXXXX-XXXX-XXXX-XXXX',
        tab_1x_ag['LE'].astype(str) 
        + '-' + tab_1x_ag['OG'].astype(str) 
        + '-' + tab_1x_ag['Acc Desc'].astype(str) 
        + '-XXXX-XXXXX-XXXX-XXXX-XXXX',
        'XXXX-XXXX-' 
        + tab_1x_ag['Acc Desc'].astype(str) 
        + '-XXXX-XXXXX-XXXX-XXXX-XXXX'
        ]
    
    tab_1x_ag['Proposed Target from Mapping'] = np.select(
        conditions, 
        choices, 
        default=''
        )
    
    mask = ~tab_1x_ag['Proposed Target from Mapping'].isin(
        profiles['Joined Target']
        )
    tab_1x_ag.loc[mask, 'Proposed Target from Mapping'] = 'No Target'
    
    return tab_1x_ag

def finalize_accounting_groups_dfs(tab_1a_ag, tab_1b_ag, profiles, role_assignment):
    logger.info("Finalizing account group data for future export.")
    
    columns_to_drop = ['LE', 
        'LE Clean', 
        'OG', 
        'AC', 
        'Acc Group?', 
        'Acc Desc', 
        'Acc Groups', 
        'Grouping'
        ]
    
    accounting_groups_1a = tab_1a_ag[
        tab_1a_ag['Proposed Target from Mapping'] != 'No Target'
        ]
    accounting_groups_1a = accounting_groups_1a.drop(
        columns=columns_to_drop, 
        errors='ignore'
        )
    accounting_groups_1a.reset_index(drop=True, inplace=True)
    
    profiles_mapping_dict = dict(zip(profiles['Joined Target'], profiles['Preparer']))
    accounting_groups_1a['User ID'] = accounting_groups_1a['Proposed Target from Mapping'].map(profiles_mapping_dict)
    
    role_assignment_mapping_dict = dict(
        zip(role_assignment['User Login'], role_assignment['Email'])
        )
    accounting_groups_1a['User Email'] = accounting_groups_1a['User ID'].map(role_assignment_mapping_dict)

    accounting_groups_1b = tab_1b_ag[tab_1b_ag['Proposed Target from Mapping'] != 'No Target']
    accounting_groups_1b = accounting_groups_1b.drop(columns=columns_to_drop, errors='ignore')
    accounting_groups_1b.reset_index(drop=True, inplace=True)
    
    profiles_mapping_dict = dict(zip(profiles['Joined Target'], profiles['Preparer']))
    accounting_groups_1b['User ID'] = accounting_groups_1b['Proposed Target from Mapping'].map(profiles_mapping_dict)
    
    role_assignment_mapping_dict = dict(zip(role_assignment['User Login'], role_assignment['Email']))
    accounting_groups_1b['User Email'] = accounting_groups_1b['User ID'].map(role_assignment_mapping_dict)
    
    return accounting_groups_1a, accounting_groups_1b

def create_1a_non_accounting_groups_df(tab_1a, fccs_maps):
    logger.info("Creating 1A non-accounting group data.")
    
    tab_1a_non_ag = tab_1a[tab_1a['Acc Group?'] == False].copy()
    tab_1a_non_ag.drop('Acc Group?', axis=1, inplace=True)
    
    for col in ['LE', 'OG', 'AC']:
        tab_1a_non_ag[col] = tab_1a_non_ag[col].str.strip().str.upper()
        
    tab_1a_non_ag['LE-OG-AC'] = (
        tab_1a_non_ag['LE'] 
        + '-' + tab_1a_non_ag['OG'] 
        + '-' + tab_1a_non_ag['AC']
    )
    
    tab_1a_non_ag['Proposed Target from Mapping'] = tab_1a_non_ag[
        'LE-OG-AC'
        ].apply(
            lambda x: (
                fccs_maps.loc[fccs_maps['LE-OG-AC'] == x, 'Target'].values[0] 
                if x in fccs_maps['LE-OG-AC'].values 
                else "No Target"
            )
        )
    
    tab_1a_non_ag = tab_1a_non_ag.drop(columns=['LE', 'LE Clean', 'OG', 'AC']) 
    
    try:
        tab_1a_errored_rows = tab_1a_non_ag[~tab_1a_non_ag['Proposed Target from Mapping'].str.endswith('XXXX')
                                        & (tab_1a_non_ag['Proposed Target from Mapping'] != 'No Target')]
        
        tab_1a_errored_rows = tab_1a_errored_rows.drop(
            columns=['LE-OG-AC', 'Proposed Target from Mapping']
            )
        
        tab_1a_non_ag = tab_1a_non_ag.drop(tab_1a_errored_rows)
        
        logger.info(tab_1a_non_ag)
        
        if not tab_1a_errored_rows.empty:
            tab_1a_non_ag = tab_1a_non_ag[
                ~tab_1a_non_ag['Account ID'].isin(
                    tab_1a_errored_rows['Account ID']
                    )
                ]
            
    except KeyError as e:
        logger.info(f"Error: {e} column not found in data frame")
        
    return tab_1a_non_ag, tab_1a_errored_rows

