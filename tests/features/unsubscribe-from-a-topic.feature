Feature: Unsubscribe from a topic
    In order to test the Unsubscribe method
    As a user
    I will unsubscribe from a topic

    Scenario: Unsubscribe from a subscribed topic
        Given I create a new topic using POST /topic0
        When I subscribe using POST /topic0/user1
        And I unsubscribe using DELETE /topic0/user1
        Then I should get a 200 back

    Scenario: Unsubscribe from an unsubscribe topic
        Given I unsubscribe using DELETE /topic0/user1
        Then I should get a 404 back
