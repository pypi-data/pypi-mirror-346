from bclearer_interop_services.file_system_service import (
    read_file_content_as_string,
)
from bclearer_interop_services.file_system_service.objects.files import (
    Files,
)
from nf_common.code.services.string_service.string_by_separators_splitter import (
    split_string_by_separators,
)


def split_file_by_separators(
    file_to_split: Files,
    separators: list,
) -> list:
    file_content_as_string = read_file_content_as_string(
        file_path=file_to_split.absolute_path_string,
    )

    results = split_string_by_separators(
        string_content=file_content_as_string,
        separators=separators,
    )

    return results
