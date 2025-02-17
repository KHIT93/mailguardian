import logging
from huey.consumer import Consumer
from huey.consumer_options import ConsumerConfig
import typer

from mailguardian.app.scheduler import queue

app = typer.Typer()

@app.command()
def run():
    consumer_options: dict = {
        'name': 'MailGuardian',
        'consumer': {
            'workers': 4,
            'worker_type': 'process'
        },
        'verbose': False
    }

    logger = logging.getLogger('huey')

    config: ConsumerConfig = ConsumerConfig(**consumer_options)
    config.validate()

    if not logger.handlers:
        config.setup_logger(logger)

    consumer: Consumer = queue.create_consumer(**config.values)

    consumer.run()