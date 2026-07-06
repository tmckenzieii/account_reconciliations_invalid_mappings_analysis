import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def accounting_group_prep(
    tab, 
    global_accounting_groups, 
    separated_1x_dataframe_label):
    logger.info(f"Checking {separated_1x_dataframe_label} data for accounting group overlap.")
    
    if not tab.empty:
        tab = tab.copy()
        tab['Acc Group?'] = tab['AC'].isin(global_accounting_groups['Future State - Account'])
    else:
        logger.info(f"{separated_1x_dataframe_label} is empty, skipping processing.")
    
    return tab

def create_accounting_groups_dfs(
    tab, 
    global_accounting_groups, 
    consolidated_preparers_and_reviewers, 
    profiles, 
    separated_1x_dataframe_label):
    logger.info(f"Creating {separated_1x_dataframe_label} accounting group data.")
    
    if tab.empty:
        logger.info(f"{separated_1x_dataframe_label} is empty. Returning an empty dataframe.")
        return pd.DataFrame(
            columns=[
                'AC', 
                'Acc Groups', 
                'Acc Desc', 
                'Grouping', 
                'Proposed Target from Mapping'
            ]
        )

    separated_1x_ag = tab[tab['AC'].isin(global_accounting_groups['Future State - Account'])].copy()
    
    separated_1x_ag['Acc Groups'] = separated_1x_ag['AC'].map(
        global_accounting_groups.set_index('Future State - Account')['Wesco 1A Account Grouping Exceptions']
        )
    separated_1x_ag['Acc Desc'] = separated_1x_ag['Acc Groups'].map(
        consolidated_preparers_and_reviewers.set_index('Account Group')['Account Description']
        )
    separated_1x_ag['Grouping'] = separated_1x_ag['Acc Groups'].map(
        consolidated_preparers_and_reviewers.set_index('Account Group')['Grouping']
        )
    
    conditions = [
        (separated_1x_ag['Grouping'] == 'LE'),
        (separated_1x_ag['Grouping'] == 'LE & OG'),
        (separated_1x_ag['Grouping'] == 'Globally')
        ]
    
    choices = [
        separated_1x_ag['LE'].astype(str) 
        + '-XXXX-' 
        + separated_1x_ag['Acc Desc'].astype(str) 
        + '-XXXX-XXXXX-XXXX-XXXX-XXXX',
        separated_1x_ag['LE'].astype(str) 
        + '-' + separated_1x_ag['OG'].astype(str) 
        + '-' + separated_1x_ag['Acc Desc'].astype(str) 
        + '-XXXX-XXXXX-XXXX-XXXX-XXXX',
        'XXXX-XXXX-' 
        + separated_1x_ag['Acc Desc'].astype(str) 
        + '-XXXX-XXXXX-XXXX-XXXX-XXXX'
        ]
    
    separated_1x_ag['Proposed Target from Mapping'] = np.select(
        conditions, 
        choices, 
        default=''
        )
    
    mask = ~separated_1x_ag['Proposed Target from Mapping'].isin(
        profiles['Joined Target']
        )
    separated_1x_ag.loc[mask, 'Proposed Target from Mapping'] = 'No Target'
    
    return separated_1x_ag

def finalize_accounting_groups_dfs(
    separated_1a_invalid_mappings, 
    separated_1b_invalid_mappings, 
    profiles, 
    role_assignment):
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
    
    accounting_groups_1a = separated_1a_invalid_mappings[
        separated_1a_invalid_mappings['Proposed Target from Mapping'] != 'No Target'
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

    accounting_groups_1b = separated_1b_invalid_mappings[separated_1b_invalid_mappings['Proposed Target from Mapping'] != 'No Target']
    accounting_groups_1b = accounting_groups_1b.drop(columns=columns_to_drop, errors='ignore')
    accounting_groups_1b.reset_index(drop=True, inplace=True)
    
    profiles_mapping_dict = dict(zip(profiles['Joined Target'], profiles['Preparer']))
    accounting_groups_1b['User ID'] = accounting_groups_1b['Proposed Target from Mapping'].map(profiles_mapping_dict)
    
    role_assignment_mapping_dict = dict(zip(role_assignment['User Login'], role_assignment['Email']))
    accounting_groups_1b['User Email'] = accounting_groups_1b['User ID'].map(role_assignment_mapping_dict)
    
    return accounting_groups_1a, accounting_groups_1b

def create_1a_non_accounting_groups_df(tab_1a, fccs_maps):
    logger.info("Creating 1A non-accounting group data.")
    
    non_accounting_group_1a = tab_1a[tab_1a['Acc Group?'] == False].copy()
    non_accounting_group_1a.drop('Acc Group?', axis=1, inplace=True)
    
    for col in ['LE', 'OG', 'AC']:
        non_accounting_group_1a[col] = non_accounting_group_1a[col].str.strip().str.upper()
        
    non_accounting_group_1a['LE-OG-AC'] = (
        non_accounting_group_1a['LE'] 
        + '-' + non_accounting_group_1a['OG'] 
        + '-' + non_accounting_group_1a['AC']
    )
    
    non_accounting_group_1a['Proposed Target from Mapping'] = non_accounting_group_1a[
        'LE-OG-AC'
        ].apply(
            lambda x: (
                fccs_maps.loc[fccs_maps['LE-OG-AC'] == x, 'Target'].values[0] 
                if x in fccs_maps['LE-OG-AC'].values 
                else "No Target"
            )
        )
    
    non_accounting_group_1a = non_accounting_group_1a.drop(columns=['LE', 'LE Clean', 'OG', 'AC']) 
    
    try:
        tab_1a_errored_rows = non_accounting_group_1a[~non_accounting_group_1a['Proposed Target from Mapping'].str.endswith('XXXX')
                                        & (non_accounting_group_1a['Proposed Target from Mapping'] != 'No Target')]
        
        tab_1a_errored_rows = tab_1a_errored_rows.drop(
            columns=['LE-OG-AC', 'Proposed Target from Mapping']
            )
        
        non_accounting_group_1a = non_accounting_group_1a.drop(tab_1a_errored_rows)
        
        logger.info(non_accounting_group_1a)
        
        if not tab_1a_errored_rows.empty:
            non_accounting_group_1a = non_accounting_group_1a[
                ~non_accounting_group_1a['Account ID'].isin(
                    tab_1a_errored_rows['Account ID']
                    )
                ]
            
    except KeyError as e:
        logger.info(f"Error: {e} column not found in data frame")
        
    return non_accounting_group_1a, tab_1a_errored_rows

