from source.data_imports.import_static_data import (
    import_static_data, 
    assign_static_data_variables
    )

from source.data_imports.import_period_data import (
    import_fccs_mappings, 
    import_invalid_mappings, 
    import_profiles, 
    import_role_assignment_report
    )

from source.data_prep_and_cleaning.invalid_mappings_prep import (
    separate_1a_invalid_mappings, 
    separate_1b_invalid_mappings
    )

from source.data_prep_and_cleaning.accounting_groups_prep import (
    create_accounting_groups_dfs, 
    accounting_group_prep, 
    finalize_accounting_groups_dfs, 
    create_1a_non_accounting_groups_df
    )

from source.data_prep_and_cleaning.need_details_prep import (
    create_1a_need_details_df, 
    create_1b_need_details_df, 
    consolidate_need_details_dfs
    )

from source.data_prep_and_cleaning.new_profile_need_wf_details import create_new_profile_need_wf_details
from source.data_prep_and_cleaning.user_confirmations_prep import create_user_confirmations
from source.data_prep_and_cleaning.fccs_mappings_prep import fccs_mappings_prep

from source.file_creation_and_saving.create_and_export import (
    folder_selection,
    export_invalid_mappings_analysis,
    export_accounting_groups,
    export_need_details,
    export_new_profiles_need_wf_details,
    export_user_confirmations,
    total_invalid_mapping_count
)

def main():
    # ─────────────────────────────────────────────
    # 1. Import static data
    # ─────────────────────────────────────────────
    path_consolidated, path_global_accounting = import_static_data()
    
    consolidated_preparers_and_reviewers, global_accounting_groups = assign_static_data_variables(
        path_consolidated,
        path_global_accounting)
    
    # ─────────────────────────────────────────────
    # 2. Import period data
    # ─────────────────────────────────────────────
    invalid_mappings = import_invalid_mappings()
    fccs_mappings_import = import_fccs_mappings()
    profiles = import_profiles()
    role_assignment = import_role_assignment_report()
    
    # ─────────────────────────────────────────────
    # 3. Split invalid mappings into 1A and 1B
    # ─────────────────────────────────────────────
    separated_1a_invalids = separate_1a_invalid_mappings(invalid_mappings)
    separated_1b_invalids = separate_1b_invalid_mappings(invalid_mappings)
    
    # ─────────────────────────────────────────────
    # 4. Accounting group prep
    # ─────────────────────────────────────────────
    separated_1a_invalids_label = '1A'
    separated_1b_invalids_label = '1B'
    
    tab_1a = accounting_group_prep(
        separated_1a_invalids, 
        global_accounting_groups, 
        separated_1a_invalids_label
        )
    tab_1b = accounting_group_prep(
        separated_1b_invalids, 
        global_accounting_groups, 
        separated_1b_invalids_label
        )
    
    tab_1a_ag = create_accounting_groups_dfs(
        separated_1a_invalids, 
        global_accounting_groups, 
        consolidated_preparers_and_reviewers, 
        profiles, 
        separated_1a_invalids_label
        )
    tab_1b_ag = create_accounting_groups_dfs(tab_1b, 
        global_accounting_groups, 
        consolidated_preparers_and_reviewers, 
        profiles, 
        separated_1b_invalids_label
        )
    
    tab_1a_ag_final, tab_1b_ag_final = finalize_accounting_groups_dfs(
        tab_1a_ag, tab_1b_ag, 
        profiles, 
        role_assignment
        )
    
    # ─────────────────────────────────────────────
    # 5. FCCS mappings prep
    # ─────────────────────────────────────────────
    fccs_mappings = fccs_mappings_prep(fccs_mappings_import)
    
    # ─────────────────────────────────────────────
    # 6. Non-accounting group prep
    # ─────────────────────────────────────────────
    tab_1a_non_accounting_groups, tab_1a_errored_rows = create_1a_non_accounting_groups_df(tab_1a, fccs_mappings)
    
    # ─────────────────────────────────────────────
    # 7. Need details prep
    # ─────────────────────────────────────────────
    tab_1a_need_details = create_1a_need_details_df(tab_1a_non_accounting_groups, tab_1a_errored_rows)
    tab_1b_need_details = create_1b_need_details_df(tab_1b)
    
    (
        need_details, 
        need_details_na, 
        need_details_cala, 
        need_details_apac, 
        need_details_emea) = consolidate_need_details_dfs(tab_1a_need_details, tab_1b_need_details
    )
    
    # ─────────────────────────────────────────────
    # 8. New profile need workflow details
    # ─────────────────────────────────────────────
    new_profile_need_wf_details = create_new_profile_need_wf_details(tab_1a_ag, tab_1b_ag)
    
    # ─────────────────────────────────────────────
    # 9. User confirmations
    # ─────────────────────────────────────────────
    user_confirmations = create_user_confirmations(
        tab_1a_non_accounting_groups, 
        profiles, 
        role_assignment
        )
    
    # ─────────────────────────────────────────────
    # 10. Folder selection
    # ─────────────────────────────────────────────
    folder_selected, now = folder_selection()
    
    # ─────────────────────────────────────────────
    # 11. Exporting files
    # ─────────────────────────────────────────────
    export_invalid_mappings_analysis(
        invalid_mappings, 
        tab_1a, 
        tab_1a_ag, 
        tab_1a_non_accounting_groups, 
        tab_1a_need_details, 
        tab_1b, 
        tab_1b_ag, 
        tab_1b_need_details, 
        folder_selected, 
        now
    )
    
    accounting_groups_count = export_accounting_groups(
        tab_1a_ag_final, 
        tab_1b_ag_final, 
        folder_selected, 
        now
    )
    
    need_details_count = export_need_details(
        need_details, 
        need_details_na, 
        need_details_cala, 
        need_details_apac, 
        need_details_emea, 
        folder_selected, 
        now
    )
    
    new_profile_need_wf_details_count = export_new_profiles_need_wf_details(
        new_profile_need_wf_details, 
        folder_selected, 
        now
    )
    
    user_confirmations_count = export_user_confirmations(
        user_confirmations, 
        folder_selected, 
        now
    )
    
    total_invalid_mapping_count(
        accounting_groups_count, 
        new_profile_need_wf_details_count, 
        need_details_count, 
        user_confirmations_count
    )
    
    
    # # Visualize period data tables
    # print("\nPrinting invalid mappings sample\n")
    # print(invalid_mappings.head(1))
    # print("\nPrinting FCCS mappings sample\n")
    # print(fccs_maps.head(1))
    # print("\nPrinting profiles sample\n")
    # print(profiles.head(1))
    # print("\nPrinting role assignment report sample\n")
    # print(role_assignment.head(1))

if __name__ == "__main__":
    main()