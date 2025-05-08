class MoveAndReplaceConfigurationFlagSets:
    def __init__(
        self,
        create_new_folders_flag: bool,
        check_source_exists: bool,
        check_target_exists: bool,
        check_workspace_exists: bool,
        commit_changes_flag: bool,
    ):
        self.create_new_folders_flag = (
            create_new_folders_flag
        )

        self.check_source_exists = (
            check_source_exists
        )

        self.check_target_exists = (
            check_target_exists
        )

        self.check_workspace_exists = (
            check_workspace_exists
        )

        self.commit_changes_flag = (
            commit_changes_flag
        )
