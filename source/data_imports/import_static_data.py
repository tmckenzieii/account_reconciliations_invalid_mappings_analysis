import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Assign data from static data as variables
def import_static_data():
    logger.info("Importing non-dynamic data.")
    path_consolidated_preparers_and_reviewers = r"C:\Users\e312628\.vscode\apps\invalid_mappings_update\non_dynamic_data\consolidated_preparers_and_reviewers.csv"
    path_global_accounting_groups = r"C:\Users\e312628\.vscode\apps\invalid_mappings_update\non_dynamic_data\global_accounting_group_db.csv"
    
    return path_consolidated_preparers_and_reviewers, path_global_accounting_groups

# Read files in Pandas
def assign_static_data_variables(path_consolidated, path_global_accounting_groups):
    logger.info("Assigning non-dynamic data to dataframe variables.")
    consolidated_preparers_and_reviewers = pd.read_csv(path_consolidated)
    global_accounting_groups = pd.read_csv(path_global_accounting_groups)
    global_accounting_groups['Future State - Account'] = global_accounting_groups['Future State - Account'].astype(str).str.strip()
    
    return consolidated_preparers_and_reviewers, global_accounting_groups