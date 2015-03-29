Feature: Subscribe to a topic
    In order to test the Subscription method
    As a user
    I will subscribe to a topic

    Scenario: Subscribe to a topic
        Given I create a new topic using POST /topic0
        When I subscribe using POST /topic0/user1
        Then I should get a 200 back

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




