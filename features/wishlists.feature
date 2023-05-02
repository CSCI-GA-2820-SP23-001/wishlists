Feature: The Wishlist service back-end
    As a wishlist customer
    I need a RESTful catalog service
    So that I can keep track of all my items

Background:
    Given the server is started

    Given the following wishlists
        | name          | account_id |
        | wish_1        | 3    | 
        | wish_2        | 3    | 
        | wish_3        | 4    |
        | wish_4        | 5    |

    Given the following wishlist items
        | item_id   | wishlist_id | sku | item_available | item_count |
        | 1         | 111       | 3 | 5 | 100 |
        | 2         | 112       | 4 | 2 | 250 |
        | 3         | 113       | 5 | 3 | 150 |
        | 4         | 114       | 6 | 1 | 200 |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Wishlist REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Wishlist
    When I visit the "Home Page"
    And I set the "Wishlist Name" to "wish_5"
    And I set the "Customer Id" to "5"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Wishlist Id" field
    And I press the "Clear" button
    Then the "Wishlist Id" field should be empty
    And the "Wishlist Name" field should be empty
    And the "Customer Id" field should be empty
    When I paste the "Wishlist Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "wish_5" in the "Wishlist Name" field
    And I should see "5" in the "Customer Id" field

Scenario: List all Wishlists
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "wish_1" in the results
    And I should see "wish_2" in the results
    And I should see "wish_3" in the results
    And I should see "wish_4" in the results


Scenario: Search for Wishlist with customer_id 3
    When I visit the "Home Page"
    And I set the "Customer Id" to "3"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "wish_1" in the results
    And I should see "wish_2" in the results
    And I should not see "wish_3" in the results

Scenario: Search for Wishlist with wishlist_name
    When I visit the "Home Page"
    And I set the "Wishlist name" to "wish_1"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "wish_1" in the results
    And I should not see "wish_2" in the results

Scenario: Update a Wishlist
    When I visit the "Home Page"
    And I set the "Wishlist Name" to "wish_1"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "wish_1" in the "Wishlist Name" field
    And I should see "3" in the "Customer Id" field
    When I change "Wishlist Name" to "wish_rename"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Wishlist Id" field
    And I press the "Clear" button
    And I paste the "Wishlist Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "wish_rename" in the "Wishlist Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "wish_rename" in the results
    And I should not see "wish_1" in the results

Scenario: Delete a Wishlist
    When I visit the "Home Page"
    And I set the "Customer ID" to "4"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "wish_3" in the "Wishlist Name" field
    When I press the "Delete" button
    Then I should see the message "Wishlist has been Deleted!"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "wish_1" in the results
    And I should not see "wish_3" in the results

Scenario: Clear a Wishlist
    When I visit the "Home Page"
    And I set the "Wishlist Name" to "wish_2"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "3" in the "Customer Id" field
    When I press the "Empty" button
    Then I should see the message "Wishlist has been cleared!"
    When I press the "Search-Item" button
    Then I should see the message "Success"
    And I should not see "item_3" in the item results

Scenario: Create a Wishlist Item
    When I visit the "Home Page"
    And I set the "Customer Id" to "5"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Wishlist Id" field
    And I press the "Clear" button
    Then the "Wishlist Id" field should be empty
    And the "Wishlist Name" field should be empty
    And the "Customer Id" field should be empty
    When I paste the "Wishlist Id" field
    And I set the "Item ID" to "15"
    And I set the "Wishlist ID" to "111"
    And I set the "Item Count" to "50"
    And I set the "Item Available" to "1"
    And I press the "Create-Item" button
    Then I should see the message "Success"
    When I copy the "Item Id" field
    And I press the "Clear" button
    Then the "Item ID" field should be empty
    And the "Wishlist ID" field should be empty
    And the "Item Count" field should be empty
    When I paste the "Item Id" field
    And I press the "Retrieve-Item" button
    Then I should see the message "Success"
    And I should see "5" in the "Item ID" field

 Scenario: Update a Wishlist Item
    When I visit the "Home Page"
    And I set the "Wishlist name" to "wish_2"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Wishlist Id" field
    And I press the "Clear" button
    When I paste the "Wishlist Id" field
    And I set the "Item ID" to "3"
    And I press the "Search-Item" button
    Then I should see the message "Success"
    And I should see "3" in the "Item ID" field
    When I change "Item ID" to "6"
    And I press the "Update-Item" button
    Then I should see the message "Success"
    When I set the "Wishlist name" to "wish_2"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Wishlist Id" field
    And I press the "Clear" button
    When I paste the "Wishlist Id" field
    And I press the "Search-Item" button
    Then I should see the message "Success"
    And I should see "6" in the item results
    And I should not see "3" in the item results

Scenario: List all Wishlists Items in a Wishlist
    When I visit the "Home Page"
    And I set the "Wishlist name" to "wish_1"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Wishlist Id" field
    And I press the "Clear" button
    When I paste the "Wishlist Id" field
    And I press the "Search-Item" button
    Then I should see the message "Success"
    And I should see "1" in the item results
    And I should not see "3" in the results


Scenario: Search for Wishlist Item with given name
    When I visit the "Home Page"
    And I set the "Wishlist name" to "wish_1"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Wishlist Id" field
    And I press the "Clear" button
    When I paste the "Wishlist Id" field
    And I set the "Item ID" to "1"
    And I press the "Search-Item" button
    Then I should see the message "Success"
    And I should see "1" in the item results
    And I should not see "2" in the item results
    And I should not see "3" in the item results


Scenario: Delete a Wishlist
    When I visit the "Home Page"
    And I set the "Wishlist name" to "wish_1"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Wishlist Id" field
    And I press the "Clear" button
    When I paste the "Wishlist Id" field
    And I set the "Item ID" to "1"
    And I press the "Search-Item" button
    Then I should see the message "Success"
    And I should see "1" in the "Item ID" field
    When I press the "Delete-Item" button
    Then I should see the message "Item has been Deleted!"
    When I press the "Clear" button
    And I set the "Wishlist name" to "wish_1"
    And I press the "Search" button
    Then I should see the message "Success"
    When I copy the "Wishlist Id" field
    And I press the "Clear" button
    When I paste the "Wishlist Id" field
    And I press the "Search-Item" button
    Then I should see the message "Success"
    And I should not see "1" in the item results
    And I should see "2" in the item results
    And I should not see "3" in the results
