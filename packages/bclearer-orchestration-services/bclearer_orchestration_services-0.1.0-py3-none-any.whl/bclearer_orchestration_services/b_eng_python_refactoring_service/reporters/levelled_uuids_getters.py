from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_folders import (
    BEngFolders,
)


def get_levelled_uuids(
    parent_folder: BEngFolders,
):
    if parent_folder is None:
        return ["", "", "", "", "", ""]

    rep_level = 8

    if (
        parent_folder.absolute_level
        < rep_level
    ):
        return ["", "", "", "", "", ""]

    levelled_uuids = []

    focus_folder = parent_folder

    while focus_folder is not None:
        levelled_uuids.append(
            focus_folder.uuid,
        )

        focus_folder = (
            focus_folder.parent_folder
        )

    levelled_uuids.reverse()

    levelled_uuids.extend(
        ["", "", "", "", "", ""],
    )

    levelled_uuids = levelled_uuids[
        5:10
    ]

    return levelled_uuids
