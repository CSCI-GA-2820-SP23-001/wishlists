import requests
from behave import given
from compare import expect

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
            "id": row["id"],
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