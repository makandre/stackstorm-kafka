from st2common.runners.base_action import Action

from kafka import KafkaProducer
from kafka.errors import KafkaError
import base64

class ProduceMessageAction(Action):
    """
    Action to send messages to Apache Kafka system.
    """
    DEFAULT_CLIENT_ID = 'st2-kafka-producer'

    def run(self, topic, message, hosts=None):
        """
        Simple round-robin synchronous producer to send one message to one topic.

        :param hosts: Kafka hostname(s) to connect in host:port format.
                      Comma-separated for several hosts.
        :type hosts: ``str``
        :param topic: Kafka Topic to publish the message on.
        :type topic: ``str``
        :param message: The message to publish.
        :type message: ``str``

        :returns: Response data: `topic`, target `partition` where message was sent,
                  `offset` number and `error` code (hopefully 0).
        :rtype: ``dict``
        """

        if hosts:
            _hosts = hosts
        elif self.config.get('hosts', None):
            _hosts = self.config['hosts']
        else:
            raise ValueError("Need to define 'hosts' in either action or in config")

        # set default for empty value
        _client_id = self.config.get('client_id') or self.DEFAULT_CLIENT_ID

        if self.config.get('tls_enable', False):
            producer = KafkaProducer(bootstrap_servers=_hosts, client_id=_client_id,
                                     security_protocol='SSL',
                                     ssl_cafile=create_file_base64(self.config.get('tls_ca_certificate', None), '/var/tls_ca_certificate'),
                                     ssl_certfile=create_file_base64(self.config.get('tls_client_certificate', None), '/var/tls_client_certificate'),
                                     ssl_keyfile=create_file_base64(self.config.get('tls_client_key', None),'/var/tls_client_key'))
        else:
            producer = KafkaProducer(bootstrap_servers=_hosts, client_id=_client_id)

        producer.send(topic, message.encode('utf_8'))
        producer.flush()
        producer.close()
        return 0
    
def create_file_base64(contents, file_name):
    """
    Create a file with the base64 encoded parameter contents and return the file name

    :param contents: base64 encoded file contents
    :type contents: ``str``
    :param file_name: file name
    :type fulename: ``str``

    :return: file name
    :rtype: ``str``
    """
    if contents == None:
        return None
    file = open(file_name, 'w')
    file.write(base64.b64decode(contents).decode('utf-8'))
    file.close()
    return file_name

