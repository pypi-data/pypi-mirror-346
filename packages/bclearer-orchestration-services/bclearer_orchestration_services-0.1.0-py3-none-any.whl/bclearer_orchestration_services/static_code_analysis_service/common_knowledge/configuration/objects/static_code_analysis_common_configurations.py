from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


class StaticCodeAnalysisCommonConfigurations:
    def __init__(
        self,
        input_file_system_objects: list,
        database_template_folder_relative_path: str,
        output_database_name: str,
        output_folder: Folders,
    ):
        self.input_file_system_objects = (
            input_file_system_objects
        )

        self.database_template_folder_relative_path = database_template_folder_relative_path

        self.output_database_name = (
            output_database_name
        )

        self.output_folder = (
            output_folder
        )
