from bclearer_orchestration_services.datetime_service.time_helpers.time_getter import (
    now_time_as_string,
)
from bclearer_orchestration_services.reporting_service.reporters.log_file import (
    LogFiles,
)
from bclearer_orchestration_services.reporting_service.reporters.nf_kafka_producers import (
    NfKafkaProducers,
)


def log_message(message: str):
    date_stamped_message = (
        now_time_as_string()
        + ": "
        + message
    )

    print(date_stamped_message)

    LogFiles.write_to_log_file(
        message=date_stamped_message
        + "\n",
    )

    NfKafkaProducers.log_to_kafka_producer(
        message=date_stamped_message,
    )
