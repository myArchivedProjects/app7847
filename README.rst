This repository contains a HTTP API gateway for Redis PubSub Qs based on
Flask

It uses a single docker instance running redis on port 6379, and flask on port 5000.


Requirements:
-------------

You'll need:

* virtualbox (for boot2docker)
* boot2docker
* python2.7 (won't work with python3)
* docker
* docker-compose
* redis (optional, only usefull for non docker based tests)


To build:
----------

  .. line-block::

      boot2docker init
      boot2docker up
      pip2 -r requirements.txt

If you get a TLS error, then you may need to temporarly disable TLS
see: https://github.com/docker/compose/issues/890#issuecomment-84468058

  .. line-block::

    docker-compose build

To run:
--------

  .. line-block::

    docker-compose up


Integration tests:
--------------------

Run tests:

  .. line-block::

      docker-compose up
      export BOOT2DOCKERIP=$( boot2docker ip)
      (cd tests && lettuce)



  .. line-block::


      **Feature: Publish a message**                        # features/publish-a-message.feature:1
        **In order to test the publish method**             # features/publish-a-message.feature:2
        **As a user**                                       # features/publish-a-message.feature:3
        **I will publish a message to a topic**             # features/publish-a-message.feature:4

        **Scenario: Publish a message to a topic**          # features/publish-a-message.feature:6
          **Given I create a new topic using POST /topic0** # features/test_helpers.py:9
          **Then I should get a 200 back**                  # features/test_helpers.py:51

      **Feature: Retrieve the next message from a topic**                    # features/retrieve-the-next-message-from-a-topic.feature:2
        **In order to test the read_next messages method**                   # features/retrieve-the-next-message-from-a-topic.feature:3
        **As a user**                                                        # features/retrieve-the-next-message-from-a-topic.feature:4
        **I will retrieve a message**                                        # features/retrieve-the-next-message-from-a-topic.feature:5

        **Scenario: 200: Retrieval succeeded**                               # features/retrieve-the-next-message-from-a-topic.feature:7
          **Given I create a new topic using POST /topic1**                  # features/test_helpers.py:9
          **When I subscribe using POST /topic1/user1**                      # features/test_helpers.py:25
          **And I publish a message 'message1' with a POST /topic1**         # features/test_helpers.py:17
          **And discard the first 'subscribe' message from /topic1/user1**   # features/test_helpers.py:45
          **And get new messages using GET /topic1/user1**                   # features/test_helpers.py:39
          **Then I should see 'message1' in the body of the message**        # features/test_helpers.py:57
          **And I should get a 200 back**                                    # features/test_helpers.py:51

        **Scenario: 204: No messages available on this topic for this user** # features/retrieve-the-next-message-from-a-topic.feature:16
          **Given I create a new topic using POST /topic2**                  # features/test_helpers.py:9
          **When I subscribe using POST /topic2/user1**                      # features/test_helpers.py:25
          **And I publish a message 'message1' with a POST /topic1**         # features/test_helpers.py:17
          **And I publish a message 'message2' with a POST /topic1**         # features/test_helpers.py:17
          **And I publish a message 'message3' with a POST /topic1**         # features/test_helpers.py:17
          **And discard the first 'subscribe' message from /topic1/user1**   # features/test_helpers.py:45
          **And get new messages using GET /topic1/user1**                   # features/test_helpers.py:39
          **And get new messages using GET /topic1/user1**                   # features/test_helpers.py:39
          **And get new messages using GET /topic1/user1**                   # features/test_helpers.py:39
          **Then I should receive nothing**                                  # features/test_helpers.py:63
          **And I should get a 204 back**                                    # features/test_helpers.py:51

        **Scenario: 404: The subscription does not exist**                   # features/retrieve-the-next-message-from-a-topic.feature:29
          **Given The subscription does not exist**                          # features/test_helpers.py:69
          **When get new messages using GET /topic1/user1**                  # features/test_helpers.py:39
          **Then I should get a 204 back**                                   # features/test_helpers.py:51

        **Scenario: Two users, one message, same topic**                     # features/retrieve-the-next-message-from-a-topic.feature:34
          **Given I create a new topic using POST /topic3**                  # features/test_helpers.py:9
          **When I subscribe using POST /topic3/user1**                      # features/test_helpers.py:25
          **And I subscribe using POST /topic3/user2**                       # features/test_helpers.py:25
          **And I publish a message 'message1' with a POST /topic3**         # features/test_helpers.py:17
          **And discard the first 'subscribe' message from /topic3/user1**   # features/test_helpers.py:45
          **And discard the first 'subscribe' message from /topic3/user2**   # features/test_helpers.py:45
          **And get new messages using GET /topic3/user1**                   # features/test_helpers.py:39
          **Then I should see 'message1' in the body of the message**        # features/test_helpers.py:57
          **And I should get a 200 back**                                    # features/test_helpers.py:51
          **When get new messages using GET /topic3/user2**                  # features/test_helpers.py:39
          **Then I should see 'message1' in the body of the message**        # features/test_helpers.py:57
          **And I should get a 200 back**                                    # features/test_helpers.py:51

      **Feature: Subscribe to a topic**                                    # features/subscribe-to-a-topic.feature:1
        **In order to test the Subscription method**                       # features/subscribe-to-a-topic.feature:2
        **As a user**                                                      # features/subscribe-to-a-topic.feature:3
        **I will subscribe to a topic**                                    # features/subscribe-to-a-topic.feature:4

        **Scenario: Subscribe to a topic**                                 # features/subscribe-to-a-topic.feature:6
          **Given I create a new topic using POST /topic0**                # features/test_helpers.py:9
          **When I subscribe using POST /topic0/user1**                    # features/test_helpers.py:25
          **Then I should get a 200 back**                                 # features/test_helpers.py:51

        **Scenario: Two users, one message, same topic**                   # features/subscribe-to-a-topic.feature:11
          **Given I create a new topic using POST /topic3**                # features/test_helpers.py:9
          **When I subscribe using POST /topic3/user1**                    # features/test_helpers.py:25
          **And I subscribe using POST /topic3/user2**                     # features/test_helpers.py:25
          **And I publish a message 'message1' with a POST /topic3**       # features/test_helpers.py:17
          **And discard the first 'subscribe' message from /topic3/user1** # features/test_helpers.py:45
          **And discard the first 'subscribe' message from /topic3/user2** # features/test_helpers.py:45
          **And get new messages using GET /topic3/user1**                 # features/test_helpers.py:39
          **Then I should see 'message1' in the body of the message**      # features/test_helpers.py:57
          **And I should get a 200 back**                                  # features/test_helpers.py:51
          **When get new messages using GET /topic3/user2**                # features/test_helpers.py:39
          **Then I should see 'message1' in the body of the message**      # features/test_helpers.py:57
          **And I should get a 200 back**                                  # features/test_helpers.py:51

      **Feature: Unsubscribe from a topic**                  # features/unsubscribe-from-a-topic.feature:1
        **In order to test the Unsubscribe method**          # features/unsubscribe-from-a-topic.feature:2
        **As a user**                                        # features/unsubscribe-from-a-topic.feature:3
        **I will unsubscribe from a topic**                  # features/unsubscribe-from-a-topic.feature:4

        **Scenario: Unsubscribe from a subscribed topic**    # features/unsubscribe-from-a-topic.feature:6
          **Given I create a new topic using POST /topic0**  # features/test_helpers.py:9
          **When I subscribe using POST /topic0/user1**      # features/test_helpers.py:25
          **And I unsubscribe using DELETE /topic0/user1**   # features/test_helpers.py:33
          **Then I should get a 200 back**                   # features/test_helpers.py:51

        **Scenario: Unsubscribe from an unsubscribe topic**  # features/unsubscribe-from-a-topic.feature:12
          **Given I unsubscribe using DELETE /topic0/user1** # features/test_helpers.py:33
          **Then I should get a 404 back**                   # features/test_helpers.py:51

      4 features (4 passed)
      9 scenarios (9 passed)
      56 steps (56 passed)

To consume:
------------

  .. line-block::

      docker-compose up
      export BOOT2DOCKERIP=$( boot2docker ip)

      curl -x POST -d "message1"  http://$BOOT2DOCKERIP:5000/topic1/user1
      curl -x POST  http://$BOOT2DOCKERIP:5000/topic1/user1
      curl -x GET  http://$BOOT2DOCKERIP:5000/topic1/user1
      curl -x DELETE  http://$BOOT2DOCKERIP:5000/topic1/user1


Improvements sorted by benefits:
----------------

* Add unitTests, code only contains gherkin style Integration tests, no unit tests were produced due to time constrains.
* clean redis state between tests, the second invocation of integration tests fails due to old state in redis
* Add development workflow using python-livereload and shovel (guard and rake for the python world)
* Refactor Code and Tests to be DRYer
* add a stunnel docker instance frontend to the flask Api app exposing only https to the outside world
* Add versioning support to the Api: http://endpoint:5000/v1/topic/user1
* Use common english verbs (or esperanto) for api calls : /v2/subscribe/topic1/user1 instead of POST,DELETE calls over the same URL
* Add json support to the Api: http://endpoint:5000/v3/topic/user1/output/json
* decouple redis-server from Dockerfile into its own docker instance
* Refactor code to use a discovery service (consul, etcd), allowing for autoscale and downscale of both redis and the flask Api web app
* package upstream into python pip servers


