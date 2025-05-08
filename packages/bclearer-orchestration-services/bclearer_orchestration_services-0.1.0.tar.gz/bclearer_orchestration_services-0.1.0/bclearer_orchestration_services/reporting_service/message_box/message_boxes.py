import ctypes

from nf_common.code.services.reporting_service.message_box.message_box_style_types import (
    MessageBoxStyleTypes,
)
from nf_common.code.services.reporting_service.message_box.message_box_w_return_types import (
    MessageBoxWReturnTypes,
)


def message_box_dialog(
    title,
    text,
    style: MessageBoxStyleTypes,
):
    return_value = ctypes.windll.user32.MessageBoxW(
        0,
        text,
        title,
        style.value,
    )

    return MessageBoxWReturnTypes(
        return_value,
    )
