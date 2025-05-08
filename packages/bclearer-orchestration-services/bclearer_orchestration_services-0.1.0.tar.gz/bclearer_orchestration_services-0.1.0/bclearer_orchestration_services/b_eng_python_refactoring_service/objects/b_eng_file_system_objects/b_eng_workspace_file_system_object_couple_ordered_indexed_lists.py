from nf_common.code.services.b_eng_python_refactoring_service.objects.b_eng_file_system_objects.b_eng_workspace_file_system_object_couples import (
    BEngWorkspaceFileSystemObjectCouples,
)


class BEngWorkspaceFileSystemObjectCouplesOrderedIndexedLists:
    def __init__(
        self,
        ordered_indexed_list: dict,
    ):
        self.__ordered_indexed_list = (
            ordered_indexed_list
        )

    def get_ordered_iterator(
        self,
    ) -> iter:
        ordered_iterator = iter(
            sorted(
                self.__ordered_indexed_list.keys(),
            ),
        )

        return ordered_iterator

    def get_path_couple_with_index(
        self,
        index: int,
    ) -> BEngWorkspaceFileSystemObjectCouples:
        path_couple = (
            self.__ordered_indexed_list[
                index
            ]
        )

        return path_couple
