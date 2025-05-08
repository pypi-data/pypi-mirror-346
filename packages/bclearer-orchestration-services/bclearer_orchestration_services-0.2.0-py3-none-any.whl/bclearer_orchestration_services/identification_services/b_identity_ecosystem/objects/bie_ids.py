from bclearer_orchestration_services.identification_services.b_identity_ecosystem.converters.int_to_base32_converter import (
    convert_int_to_base32,
)


class BieIds:
    def __init__(self, int_value: int):
        self.int_value = int_value

    def __str__(self):
        return convert_int_to_base32(
            int_value=self.int_value,
        )

    def __eq__(self, other):
        if not isinstance(
            other,
            BieIds,
        ):
            return NotImplemented

        return (
            self.int_value
            == other.int_value
        )

    def __lt__(self, other):
        if not isinstance(
            other,
            BieIds,
        ):
            return NotImplemented

        return (
            self.int_value
            < other.int_value
        )

    def __hash__(self):
        return hash(self.int_value)

    def __repr__(self):
        return convert_int_to_base32(
            int_value=self.int_value,
        )
