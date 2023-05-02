# pylint: disable=function-redefined

"""
Wishlists Steps

Steps file for wishlists.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import os
import requests
from behave import given, when, then
from compare import expect


@given('the server is started')
def step_impl(context):
    context.base_url = os.getenv(
        'BASE_URL',
        'http://localhost:8000'
    )
    context.resp = requests.get(context.base_url + '/')
    assert context.resp.status_code == 200


@when(u'I visit the "Home Page"')
def step_impl(context):
    context.resp = requests.get(context.base_url + '/')
    assert context.resp.status_code == 200


@then(u'I should see "{message}" in the title')
def step_impl(context, message):
    assert message in str(context.resp.text)


@then('I should not see "{message}"')
def step_impl(context, message):
    assert message not in str(context.resp.text)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id =  element_name.lower().replace(' ', '_')
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)


@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = element_name.lower().replace(' ', '_')
    element = Select(context.driver.find_element_by_id(element_id))
    element.select_by_visible_text(text)


@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = element_name.lower().replace(' ', '_')
    element = Select(context.driver.find_element_by_id(element_id))
    expect(element.first_selected_option.text).to_equal(text)


@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(' ', '_')
    element = context.driver.find_element_by_id(element_id)
    expect(element.get_attribute("value")).to_be("")

@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute("value")
    logging.info("Clipboard contains: %s", context.clipboard)


@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + "-btn"
    context.driver.find_element_by_id(button_id).click()


@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "search_results"), name
        )
    )
    expect(found).to_be(True)

@then('I should see "{name}" in the item results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "search_item_results"), name
        )
    )
    expect(found).to_be(True)


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element_by_id("search_results")
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(name in element.text, False, error_msg)

@then('I should not see "{name}" in the item results')
def step_impl(context, name):
    element = context.driver.find_element_by_id("search_item_results")
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(name in element.text, False, error_msg)


@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "flash_message"), message
        )
    )
    expect(found).to_be(True)

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = element_name.lower().replace(' ', '_')
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id), text_string
        )
    )
    expect(found).to_be(True)


@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)

#Building database of wishlists and items

@given('the following wishlists')
def step_impl(context):
    """ Delete all Wishlists and load new ones """
    rest_endpoint = f"{context.BASE_URL}/wishlists"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for wishlist in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{wishlist['id']}")
        expect(context.resp.status_code).to_equal(204)

    # load the database with new wishlists
    for row in context.table:
        payload = {
            "name": row['name'],
            "account_id": int(row['account_id'])
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)


@given('the following wishlist items')
def step_impl(context):
    """ Load new wishlist items, delete wishlists already deleted all items """
    for row in context.table:
        wishlist_id = row['wishlist_id']
        queryString = 'name=' + wishlist_name
        rest_endpoint = f"{context.BASE_URL}/wishlists?{queryString}"
        context.resp = requests.get(rest_endpoint)
        print(context.resp.json())
        wishlist_id = context.resp.json()[0]['id']
        payload = {
            "Item ID": row['id'],
            "wishlist_id": int(row['wishlist_id']),
            "SKU": int(row['sku']),
            "Item Availability": row['item_available'],
            "Item Count": int(row['count'])
        }
        endpoint = f"{context.BASE_URL}/wishlists/{wishlist_id}/items"
        print(endpoint)
        context.resp = requests.post(endpoint, json=payload)
        print(context.resp.json())
        expect(context.resp.status_code).to_equal(201)