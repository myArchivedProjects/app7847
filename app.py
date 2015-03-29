#!/usr/bin/env python2

__author__ = 'azul'

from flask import Flask, request
import redis
import redispubsub


class Publisher(object):

    def __init__(self):
        """
        Initialises a connection to Redis for the publisher

        """
        self.publisher = redis.Redis()

    def publish(self, topic, message):
        """
        Publishes a message to a redis queue

        :param topic: name of the redis queue to subscribe
        :param message: message to push into the queue
        :return: True/False
        """
        try:
            self.publisher.publish(topic, message)
            return True
        except:
            return False


class Consumer(object):

    def __init__(self):
        """
        Initialises a connection to Redis for the redis consumer

        """
        self.publisher = redis.Redis()
        self.consumer = redispubsub.RedisPubsub(self.publisher.pubsub())
        self.is_consumer_running = False

    def subscribe(self, topic):
        """
        Subscribes to a redis queue

        :param topic: name of the redis queue to subscribe
        :return: True
        """
        if self.is_consumer_running is False:
            self.consumer.subscribe(topic)
            self.consumer.start()
            self.is_consumer_running = True
        else:
            self.consumer.subscribe(topic)
        return True

    def unsubscribe(self, topic):
        """
        Unsubcribes from a redis queue

        :param topic: name of the redis queue to subscribe
        :return: True
        """
        self.consumer.unsubscribe(topic)
        return True

    def read_next(self, topic):
        """

        :param topic: name of the redis queue
        :return: String containing the next message in the redis queue
        """
        message = self.consumer.dequeue(topic)
        if message is None:
            response = ''
        elif message['type'] == 'subscribe':
            response = ''
        else:
            response = message['data']
        return str(response)


if __name__ == '__main__':

    publisher = Publisher()
    users = {}

    app = Flask(__name__)

    @app.route('/<topic>', methods=['POST'])
    def publish(topic):
        # we need to call get_data() to get the body of the message posted
        request.get_data()
        result = publisher.publish(topic, request.data)
        if result:
            return 'Publish succeeded : message %s published to topic %s' % (request.data, topic)
        else:
            return 'failed to publish message %s to topic %s' % (
                request.data, topic)

    @app.route('/<topic>/<username>', methods=['POST'])
    def subscribe(topic, username):
        if username not in users.keys():
            users[username] = Consumer()
        if users[username].subscribe(topic):
            return 'Subscription succeeded : %s to topic %s' % (username, topic)

    @app.route('/<topic>/<username>', methods=['DELETE'])
    def unsubscribe(topic, username):
        if username in users.keys():
            try:
                if users[username].unsubscribe(topic):
                    result = \
                        "Unsubscribe succeeded : user %s from topic %s" \
                        % (username, topic)
                    return str(result)
                else:
                    return 'The subscription does not exist', 404
            except:
                return 'The subscription does not exist', 404
        else:
            return 'The subscription does not exist', 404

    @app.route('/<topic>/<username>', methods=['GET'])
    def read_next(topic, username):
        if username in users.keys():
            result = users[username].read_next(topic)
        else:
            return str('The subscription does not exist'), 404
        if result == '':
            return \
                'There are no messages available for this topic on this user', 204
        else:
            return str(result)

    app.run(host='0.0.0.0')