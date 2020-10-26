""" Celery configuration. """

from rcvis.environment import environment

## Broker settings.
broker_url = 'sqs://'  # pylint: disable=invalid-name

# List of modules to import when the Celery worker starts.
imports = ('movie.tasks',)

# No backend - we don't care about the results, we'll update the database
result_backend = None  # pylint: disable=invalid-name

task_annotations = {'tasks.create_movie': {'rate_limit': '1/s'}}

sqs_queue_name = environment.get_sqs_queue_name()

broker_transport_options = {
    'queue_name_prefix': sqs_queue_name
}

# At most two processes at once - can later be scaled as needed, but for now,
# too many workers were spawned (seemingly ncores+1 despite requesting just ncores?)
celeryd_concurrency = 2  # pylint: disable=invalid-name
