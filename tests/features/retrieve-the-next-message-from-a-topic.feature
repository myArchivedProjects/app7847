
Feature: Retrieve the next message from a topic
    In order to test the read_next messages method
    As a user
    I will retrieve a message

    Scenario: 200: Retrieval succeeded
        Given I create a new topic using POST /topic1
        When I subscribe using POST /topic1/user1
        And I publish a message 'message1' with a POST /topic1
        And discard the first 'subscribe' message from /topic1/user1
        And get new messages using GET /topic1/user1
        Then I should see 'message1' in the body of the message
        And I should get a 200 back

    Scenario: 204: No messages available on this topic for this user
        Given I create a new topic using POST /topic2
        When I subscribe using POST /topic2/user1
        And I publish a message 'message1' with a POST /topic1
        And I publish a message 'message2' with a POST /topic1
        And I publish a message 'message3' with a POST /topic1
        And discard the first 'subscribe' message from /topic1/user1
        And get new messages using GET /topic1/user1
        And get new messages using GET /topic1/user1
        And get new messages using GET /topic1/user1
        Then I should receive nothing
        And I should get a 204 back

    Scenario: 404: The subscription does not exist
        Given The subscription does not exist
        When get new messages using GET /topic1/user1
        Then I should get a 204 back

    Scenario: Two users, one message, same topic
        Given I create a new topic using POST /topic3
        When I subscribe using POST /topic3/user1
        And I subscribe using POST /topic3/user2
        And I publish a message 'message1' with a POST /topic3
        And discard the first 'subscribe' message from /topic3/user1
        And discard the first 'subscribe' message from /topic3/user2
        And get new messages using GET /topic3/user1
        Then I should see 'message1' in the body of the message
        And I should get a 200 back
        When get new messages using GET /topic3/user2
        Then I should see 'message1' in the body of the message
        And I should get a 200 back
