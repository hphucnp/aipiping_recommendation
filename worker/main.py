import asyncio
from concurrent.futures import ThreadPoolExecutor

from beanie import init_beanie
from confluent_kafka import Consumer, KafkaError

from common.config.client.mongo_client import mongo_client
from common.config.client.openai_client import openai_client
from common.config.logger import logger
from common.config.settings import settings
from common.model.recommendation import Recommendation, RecommendationStatus, Season

KAFKA_TOPIC = settings.KAFKA_WORKER_TOPIC

async def init_beanie_session():
    await init_beanie(database=mongo_client.recommendations, document_models=[Recommendation], multiprocessing_mode=True)


def get_recommendations_data(country: str, season: Season):
    prompt = f"Recommend three things to do in {country} during {season}."
    print(f"Send prompt: {prompt} to OpenAI API for completion.")
    logger.info(f"Send prompt: {prompt} to OpenAI API for completion.")
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
        ]
    )
    content = response.choices[0].message.content
    return [li[3:] for li in content.splitlines() if li]


async def get_data_and_persist(uid: str):
    print("Get data and persist")
    try:
        recommendation: Recommendation = await Recommendation.find_one({"_id": uid})
        country = recommendation.country
        season = recommendation.season
        recommendation.recommendations = get_recommendations_data(country, season)
        recommendation.status = RecommendationStatus.COMPLETED
        print(f"Recommendations: {recommendation.recommendations}")
        await recommendation.save()
    except Exception as e:
        print(e.with_traceback())


async def process_message(msg):
    # Extract the message key and value
    key = msg.key().decode('utf-8')
    value = msg.value().decode('utf-8')
    print(f"Received message: key={key}, value={value}")
    await get_data_and_persist(value)


def run_in_new_loop(loop, coro):
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


async def main():
    await init_beanie_session()
    # Create a Kafka consumer
    consumer = Consumer({
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVER,
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest'
    })

    # Subscribe to the Kafka topic
    consumer.subscribe([KAFKA_TOPIC])

    # Create a ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=20)
    try:
        # Continuously poll for new messages
        while True:
            msg = consumer.poll(1.0)

            # If a message is received, process it
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            # Submit a new task to the executor to process the message
            loop = asyncio.new_event_loop()
            executor.submit(run_in_new_loop, loop, process_message(msg))

    finally:
        # Close the consumer and executor when done
        consumer.close()
        executor.shutdown()


if __name__ == '__main__':
    # consume_kafka_topic()
    asyncio.run(main())
