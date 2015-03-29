from lettuce import step, world
import requests
import os

endpoint = "http://%s:5000" % os.environ['BOOT2DOCKERIP']


@step("I create a new topic using POST /(.*)")
def create_topic(step, topic):
    world.message_response = requests.post(
        '%s/%s' % (endpoint, topic), data='subscribe')
    assert world.message_response.status_code == 200, \
        "Got %s" % world.message_response.status_code


@step("I publish a message '(.*)' with a POST /(.*)")
def publish(step, message, topic):
    world.message_response = requests.post(
        '%s/%s' % (endpoint, topic), data=message)
    assert world.message_response.status_code == 200, \
        "Got %s" % world.message_response.status_code


@step("I subscribe using POST /(.*)/(.*)")
def subscribe(step, topic, user):
    world.message_response = requests.post(
        '%s/%s/%s' % (endpoint, topic, user))
    assert world.message_response.status_code == 200, \
        "Got %s" % world.message_response.status_code


@step("I unsubscribe using DELETE /(.*)/(.*)")
def unsubscribe(step, topic, user):
    world.message_response = requests.delete(
        '%s/%s/%s' % (endpoint, topic, user))


@step("get new messages using GET /(.*)/(.*)")
def read_next(step, topic, user):
    world.message_response = requests.get(
        '%s/%s/%s' % (endpoint, topic, user))


@step("discard the first 'subscribe' message from /(.*)/(.*)")
def discard_next(step, topic, user):
    world.message_response = requests.get(
        '%s/%s/%s' % (endpoint, topic, user))


@step("I should get a (.*) back")
def check_message_http_code(step, expected):
    assert world.message_response.status_code == int(expected), \
        "Got %s" % world.message_response.status_code


@step("I should see '(.*)' in the body of the message")
def check_message_body(step, expected):
    assert world.message_response.content == expected, \
        "Got %s" % world.message_response.content


@step("I should receive nothing")
def check_that_I_receive_nothing(step):
    assert world.message_response.content == '', \
        "Got %s" % world.message_response.content


@step("The subscription does not exist")
def pass_the_subscription_does_not_exist(step):
    pass

