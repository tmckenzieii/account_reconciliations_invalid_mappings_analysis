import logging

logger = logging.getLogger(__name__)

def create_user_confirmations(tab_1a_non_ag, profiles, role_assignment):
    logger.info("Creating user confirmations dataframe.")
    
    columns_to_drop = ['LE-OG-AC']
    
    user_confirmations = tab_1a_non_ag[tab_1a_non_ag['Proposed Target from Mapping'].str.endswith('XXXX')]
    user_confirmations = user_confirmations.drop(columns=columns_to_drop, errors='ignore')
    user_confirmations.reset_index(drop=True, inplace=True)
    
    profiles_mapping_dict = dict(
        zip(profiles['Joined Target'], profiles['Preparer'])
        )
    
    user_confirmations['User ID'] = user_confirmations['Proposed Target from Mapping'].map(profiles_mapping_dict)
    
    role_assignment_mapping_dict = dict(
        zip(role_assignment['User Login'], role_assignment['Email'])
        )
    user_confirmations['User Email'] = user_confirmations['User ID'].map(role_assignment_mapping_dict)
    
    return user_confirmations