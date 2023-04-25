Feature: The Wishlist service back-end
    As a wishlist customer
    I need a RESTful catalog service
    So that I can keep track of all my items

Background:
    Given the server is started

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Wishlist REST API Service" in the title
    And I should not see "404 Not Found"