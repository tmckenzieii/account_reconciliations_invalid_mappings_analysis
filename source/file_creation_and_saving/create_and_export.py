import pandas as pd 
import datetime    
import os
import logging  

from tkinter import filedialog

logger = logging.getLogger(__name__)

def folder_selection():
    logger.info("Select a folder to save export files.")
    folder_selected = filedialog.askdirectory()
    now = datetime.datetime.now().strftime("%y-%m-%d")

    if not folder_selected:
        logger.info("No folder selected.")
        return None, None

    return folder_selected, now

def export_invalid_mappings_analysis(
    invalid_mappings, 
    tab_1a, 
    tab_1a_ag, 
    tab_1a_non_ag, 
    tab_1a_need_details, 
    tab_1b, 
    tab_1b_ag, 
    tab_1b_need_details, 
    folder_selected, 
    now):
    logger.info("Saving invalid mappings analysis to your selected folder.")
    
    if folder_selected:
        writer = pd.ExcelWriter(os.path.join(folder_selected, f'Invalid Mapping Analysis {now}.xlsx'), engine='xlsxwriter')
        
        invalid_mappings.to_excel(writer, sheet_name='All Invalid Mappings', index=False)
        tab_1a.to_excel(writer, sheet_name='1A', index=False)
        tab_1a_ag.to_excel(writer, sheet_name='1A AG', index=False)
        tab_1a_non_ag.to_excel(writer, sheet_name='1A Non AG', index=False)
        tab_1a_need_details.to_excel(writer, sheet_name='1A Need Details', index=False)
        tab_1b.to_excel(writer, sheet_name='1B', index=False)
        tab_1b_ag.to_excel(writer, sheet_name='1B AG', index=False)
        tab_1b_need_details.to_excel(writer, sheet_name='1B Need Details', index=False)
        
        writer._save()
        
        logger.info(f"All files have been saved to {folder_selected}.")
        
    else:
        logger.info("No folder selected.")
        
    return None

def export_accounting_groups(
    accounting_groups_1a, 
    accounting_groups_1b, 
    folder_selected, 
    now):
    logger.info("Saving accounting groups file to previously selected folder.")
    
    if folder_selected:
        writer_accounting_groups = pd.ExcelWriter(os.path.join(folder_selected, f'Accounting Groups {now}.xlsx'), engine='xlsxwriter')
        
        accounting_groups_1a.to_excel(writer_accounting_groups, sheet_name='1A Confirmations', index=False)
        accounting_groups_1b.to_excel(writer_accounting_groups, sheet_name='1B Confirmations', index=False)
        
        writer_accounting_groups._save()
        
        accounting_groups_count = len(accounting_groups_1a) + len(accounting_groups_1b)
        
        logger.info(f"The account groups file has been saved in {folder_selected}.")
        
    else:
        logger.info("No folder selected.")
        
    return accounting_groups_count

def export_new_profiles_need_wf_details(
    new_profile_need_wf_details, 
    folder_selected, 
    now):
    logger.info("Saving profile export to previously selected folder.")

    if folder_selected:
        writer_new_profile_need_wf_details = pd.ExcelWriter(os.path.join(folder_selected, f'New Profile - Need Workflow Details {now}.xlsx'), engine='xlsxwriter')
        new_profile_need_wf_details.to_excel(writer_new_profile_need_wf_details, sheet_name='New Profiles', index=False)
        writer_new_profile_need_wf_details._save()
        new_profile_need_wf_details_count = len(new_profile_need_wf_details)
        
    else:
        logger.info("No folder selected.")
        
    return new_profile_need_wf_details_count

def export_user_confirmations(
    user_confirmations, 
    folder_selected, 
    now):
    logger.info("Saving user confirmations file to previously selected folder.")
    
    if folder_selected:
        writer_user_confirmations = pd.ExcelWriter(os.path.join(folder_selected, f'User Confirmations {now}.xlsx'), engine='xlsxwriter')
        user_confirmations.to_excel(writer_user_confirmations, sheet_name='1A Invalid Mappings', index=False)
        
        writer_user_confirmations._save()
        
        user_confirmations_count = len(user_confirmations)
        
    else:
        logger.info("No folder selected.")
        
    return user_confirmations_count

def export_need_details(
    need_details, 
    need_details_na, 
    need_details_cala, 
    need_details_apac, 
    need_details_emea, 
    folder_selected, 
    now):
    logger.info("Saving need details file to previously selected folder.")
    
    if folder_selected:
        writer_need_details = pd.ExcelWriter(os.path.join(folder_selected, f'Need Details {now}.xlsx'), engine='xlsxwriter')
        need_details.to_excel(writer_need_details, sheet_name='Invalid Mappings', index=False)
        need_details_na.to_excel(writer_need_details, sheet_name='NA', index=False)
        need_details_cala.to_excel(writer_need_details, sheet_name='CALA', index=False)
        need_details_apac.to_excel(writer_need_details, sheet_name='APAC', index=False)
        need_details_emea.to_excel(writer_need_details, sheet_name='EMEA', index=False)
        
        writer_need_details._save()
        
        need_details_count = len(need_details)
        
    else:
        logger.info("No folder selected.")
        
    return need_details_count

def total_invalid_mapping_count(
    accounting_groups_count, 
    new_profile_need_wf_details_count, 
    need_details_count, 
    user_confirmations_count):
    logger.info("Processing invalid mapping volume.")
    
    total_count = sum([
        accounting_groups_count, 
        new_profile_need_wf_details_count, 
        need_details_count, 
        user_confirmations_count
        ])
    
    return total_count