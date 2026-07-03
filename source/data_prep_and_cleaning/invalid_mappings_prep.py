import logging

logger = logging.getLogger(__name__)

def separate_1a_invalid_mappings(invalid_mappings): 

    logger.info("Separating 1A invalid mappings.")
    tab_1a = invalid_mappings[~invalid_mappings['Account ID'].str.contains('ALL-ALL-ALL-ALL-ALL')].copy()
    if not tab_1a.empty:
        tab_1a.loc[:, 'LE'] = tab_1a['Account ID'].str.split('-', expand=True)[0]
        tab_1a.loc[:, 'LE Clean'] = tab_1a['LE'].str.split('_').str[0]
        tab_1a.loc[:, 'OG'] = tab_1a['Account ID'].str.split('-', expand=True)[1]
        tab_1a.loc[:, 'AC'] = tab_1a['Account ID'].str.split('-', expand=True)[2]
    else:
        pass
    return tab_1a

def separate_1b_invalid_mappings(invalid_mappings):
    logger.info("Separating 1B invalid mappings.")
    tab_1b = invalid_mappings[invalid_mappings['Account ID'].str.contains('ALL-ALL-ALL-ALL-ALL')].copy()
    if not tab_1b.empty:
        tab_1b.loc[:, 'LE'] = tab_1b['Account ID'].str.split('-', expand=True)[0]
        tab_1b.loc[:, 'OG'] = tab_1b['Account ID'].str.split('-', expand=True)[1]
        tab_1b.loc[:, 'AC'] = tab_1b['Account ID'].str.split('-', expand=True)[2]
    else:
        pass
    return tab_1b