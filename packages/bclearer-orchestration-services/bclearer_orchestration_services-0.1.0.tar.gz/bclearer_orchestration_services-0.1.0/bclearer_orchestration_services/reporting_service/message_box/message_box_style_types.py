from enum import Enum


class MessageBoxStyleTypes(Enum):
    Ok = 0
    OkCancel = 1
    AbortRetryIgnore = 2
    YesNoCancel = 3
    YesNo = 4
    RetryCancel = 5
    CancelTryAgainContinue = 6
