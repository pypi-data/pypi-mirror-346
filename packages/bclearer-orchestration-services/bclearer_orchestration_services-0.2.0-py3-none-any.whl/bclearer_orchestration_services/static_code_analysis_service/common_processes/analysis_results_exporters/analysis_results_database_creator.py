from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from bclearer_interop_services.file_system_service.resources_service.processes.resource_copier import (
    copy_resource_and_rename,
)


def create_results_database_file(
    results_folder: Folders,
    database_template_folder_path: str,
    database_template_name: str,
    results_database_name: str,
) -> Files:
    results_database_file = copy_resource_and_rename(
        database_template_folder_path=database_template_folder_path,
        database_template_name=database_template_name,
        target_folder=results_folder,
        new_name=results_database_name,
    )

    return results_database_file
