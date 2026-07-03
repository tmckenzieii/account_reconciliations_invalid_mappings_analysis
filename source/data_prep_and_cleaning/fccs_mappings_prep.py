import logging

logger = logging.getLogger(__name__)

def fccs_mappings_prep(fccs_mappings):
    logger.info("Preparing FCCS mappings file data.")
    
    fccs_mappings['LE'] = fccs_mappings['String'].apply(lambda x: x.split('-')[0].strip())
    fccs_mappings['LE'] = fccs_mappings['LE'].str.replace('LE_', '')
    fccs_mappings['OG'] = fccs_mappings['String'].apply(lambda x: x.split('-')[1].strip())
    fccs_mappings['OG'] = fccs_mappings['OG'].str.replace('OG_', '')
    fccs_mappings['AC'] = fccs_mappings['String'].apply(lambda x: x.split('-')[2].strip())
    fccs_mappings['AC'] = fccs_mappings['AC'].str.replace('AC_', '')
    fccs_mappings['LE-OG-AC'] = fccs_mappings['LE'].astype(str) + '-' + fccs_mappings['OG'].astype(str) + '-' + fccs_mappings['AC'].astype(str)
    
    for col in ['LE', 'OG', 'AC']:
        fccs_mappings[col] = fccs_mappings[col].str.strip().str.upper()
        
    return fccs_mappings

