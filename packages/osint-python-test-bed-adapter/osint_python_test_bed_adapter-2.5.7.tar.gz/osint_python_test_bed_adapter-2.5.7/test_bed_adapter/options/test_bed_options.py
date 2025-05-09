class TestBedOptions:
    def __init__(self, dictionary):
        # Group ID that this adapter should join
        self.consumer_group = None

        # Uri for the Kafka broker, e.g. broker:3501
        self.kafka_host = None

        # Uri for the schema registry, e.g. schema_registry:3502
        self.schema_registry = "localhost:3502"

        # Max message bytes
        self.message_max_bytes = 10000000

        # Partitioner type for producer. Values: random, consistent, consistent_random, murmur2, murmur2_random, fnv1a, fnv1a_random
        self.partitioner = 'random'

        # Use string based keys for the producer
        self.string_based_keys = True

        # If string_based_keys is true, this is the type of the key. Values: id, group_id
        self.string_key_type = "id"

        # Interval poll in ms
        self.max_poll_interval_ms = 300000

        # Session timeout in ms
        self.session_timeout_ms = 90000
        # Set auto commit interval in ms
        self.auto_commit_interval_ms = 5000
        self.processing_thread_count = 1
        # If true, automatically register schema's on startup
        # Not implemented
        # self.auto_register_schemas = False

        # If autoRegisterSchemas is true, contains the folder with *.avsc schema's to register
        # NOt implemented
        # self.schema_folder = "data/schemas/"

        # If true fetch all schema versions (and not only the latest)
        # Not implemented
        # self.fetch_all_versions = False

        # If true fetch all schema's (and not only the consume and produce topics)
        # Not implemented
        # self.fetch_all_schemas = False

        # If true fetch all schema's (and not only the consume and produce topics)
        # Not implemented
        # self.fetch_all_topics = False

        # If set true, use the topics offset to retreive messages
        # Not implemented
        # self.exclude_internal_topics = False

        # Reset the offset messages on start.
        # Not implemented
        # self.reset_offset_on_start = False

        # Offset type possibles: earliest, latest, error
        self.offset_type = "latest"
        # Ignore messages that for timeout
        self.ignore_timeout = None
        # If true, use the send the latest message
        self.use_latest = False

        # How often should the adapter try to reconnect to the kafka server if the first time fails
        # Not implemented
        # self.reconnection_retries = 5

        # Interval between two heartbeat messages in secs
        self.heartbeat_interval = 10

        # Send messages asynchronously
        # Send is async by default
        # self.send_messages_asynchronously = True

        # Topics you want to consume
        # Not implemented
        # self.consume = []

        # Topics you want to produce
        # Not implemented
        # self.produce = []

        # If set true, use SSL
        # self.use_ssl = False

        # Path to trusted CA certificate. It will only be used if use_ssl is set true.
        # self.ca_file = ""

        # Path to client certificate. It will only be used if use_ssl is set true.
        # self.cert_file: str = None

        # Path to client private-key file. It will only be used if use_ssl is set true.
        # self.key_file: str = None

        # Password for private key. It will only be used if use_ssl is set true.
        # self.password_private_key: str = None

        # Here we override the default values if they were introduced in the dictionary as an input of the constructor
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def validate_options(self):
        print("")

    def get_options_from_file(self):
        print("")
