from aiokafka import AIOKafkaConsumer
from config import settings


class KafkaConsumerManager:
    def __init__(self, kafka_conf):
        '''
        :param kafka_conf: config of AIOKafkaConsumer
        '''
        self._topics = None
        self._kafka_conf = kafka_conf
        self._kafka_consumer: AIOKafkaConsumer = None
        self._wrapper_function = None
        self._response_producer = None

    async def init_consumer(self, topics, wrapper_function, response_producer=None):
        '''
        :param topics: name of the topic to consume
        :param wrapper_function: function that receives 2 params: msg from topic & kafka producer (optional)
        :param response_producer: instance of KafkaProducerSessionManager class
        :return: None
        '''
        self._topics = topics
        self._kafka_consumer = AIOKafkaConsumer(self._topics, **self._kafka_conf)
        self._wrapper_function = wrapper_function
        self._response_producer = response_producer

    async def stop(self):
        return await self._kafka_consumer.stop()

    async def consume(self):
        if self._topics is None or self._wrapper_function is None:
            raise Exception("kafka consumer is not initialized")

        consumer = self._kafka_consumer
        await consumer.start()
        try:
            async for msg in consumer:
                await self._wrapper_function(msg, self._response_producer)
        finally:
            await consumer.stop()


KAFKA_CONF = {"bootstrap_servers": f"{settings.kafka_host}:{settings.kafka_port}"}
kafka_likes_consumer = KafkaConsumerManager(KAFKA_CONF)
kafka_views_consumer = KafkaConsumerManager(KAFKA_CONF)
