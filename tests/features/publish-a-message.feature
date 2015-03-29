Feature: Publish a message
    In order to test the publish method
    As a user
    I will publish a message to a topic

    Scenario: Publish a message to a topic
        Given I create a new topic using POST /topic0
        Then I should get a 200 back
