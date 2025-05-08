from bclearer_core.constants.standard_constants import (
    UTF_8_ENCODING_NAME,
)
from kafka import KafkaProducer


class NfKafkaProducers:
    __kafka_producer = None

    __topic_name = None

    __key = None

    @staticmethod
    def log_to_kafka_producer(
        message: str,
    ):
        if (
            NfKafkaProducers.__kafka_producer
            is None
        ):
            return

        if (
            NfKafkaProducers.__topic_name
            is None
        ):
            return

        if (
            NfKafkaProducers.__key
            is None
        ):
            return

        try:
            message_as_bytes = bytes(
                message,
                encoding=UTF_8_ENCODING_NAME,
            )

            NfKafkaProducers.__kafka_producer.send(
                topic=NfKafkaProducers.__topic_name,
                key=NfKafkaProducers.__key,
                value=message_as_bytes,
            )

            NfKafkaProducers.__kafka_producer.flush()

        except Exception as exception:
            print(
                "Exception logging message in Kafka: "
                + str(exception),
            )

    @staticmethod
    def set_kafka_producer(
        list_of_kafka_broker_servers_with_ports: list,
        topic_name: str,
        key: str,
    ):
        NfKafkaProducers.__topic_name = (
            topic_name
        )

        NfKafkaProducers.__key = bytes(
            key,
            encoding=UTF_8_ENCODING_NAME,
        )

        try:
            NfKafkaProducers.__kafka_producer = KafkaProducer(
                bootstrap_servers=list_of_kafka_broker_servers_with_ports,
                api_version=(0, 10),
            )

        except Exception as exception:
            print(
                "Exception while connecting Kafka: "
                + str(exception),
            )

    @staticmethod
    def close_kafka_producer():
        if (
            NfKafkaProducers.__kafka_producer
            is None
        ):
            return

        NfKafkaProducers.__kafka_producer.close()
