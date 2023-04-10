"""
My Service

Describe what your service does here
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from service.common import status  # HTTP Status Codes
from service.models import PersistentBase, Wishlist, Item
from . import app  # Import Flask application

# Import Flask application
from . import app


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return {"status": 'OK'}, status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )

######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

######################################################################
# CREATE A NEW WISHLIST
######################################################################
@app.route("/wishlists", methods=["POST"])
def create_wishlists():
    """
    Creates a wishlist
    This endpoint will create an wishlist based the data in the body that is posted
    """
    app.logger.info("Request to create an wishlist")
    check_content_type("application/json")

    # Create the wishlist
    wishlist = Wishlist()
    wishlist.deserialize(request.get_json())
    wishlist.create()

    # Create a message to return
    message = wishlist.serialize()
    # Uncomment this code once get_wishlists is implemented
    location_url = url_for("list_wishlists", wishlist_id=wishlist.id, _external=True)
    #location_url = "Unknown"
    
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# LIST ALL ACCOUNTS
######################################################################
@app.route("/wishlists", methods=["GET"])
def list_wishlists():
    """Returns all of the Wishlists"""
    app.logger.info("Request for Wishlist list")
    wishlists = []

    # Process the query string if any
    name = request.args.get("name")
    if name:
        wishlists = Wishlist.find_by_name(name)
    else:
        wishlists = Wishlist.all()

    # Return as an array of dictionaries
    results = [wishlist.serialize() for wishlist in wishlists]

    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# READ AN ITEM FROM A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["GET"])
def get_items(wishlist_id, item_id):
    """
    Get an Item
    This endpoint returns just an item
    """
    app.logger.info(
        "Request to retrieve Item %s for Wishlist id: %s", (item_id, wishlist_id)
    )

    # See if the item exists and abort if it doesn't
    item = Item.find(item_id)
    if not item:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{item_id}' could not be found.",
        )

    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# ADD AN ITEM TO A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items", methods=["POST"])
def create_items(wishlist_id):
    """
    Create an Item on an Wishlist
    This endpoint will add an item to an wishlist
    """
    app.logger.info("Request to create an Item for Wishlist with id: %s", wishlist_id)
    check_content_type("application/json")

    # See if the wishlist exists and abort if it doesn't
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' could not be found.",
        )

    # Create an item from the json data
    item = Item()
    item.deserialize(request.get_json())

    # Append the item to the wishlist
    wishlist.items.append(item)
    wishlist.update()

    # Prepare a message to return
    message = item.serialize()

    return make_response(jsonify(message), status.HTTP_201_CREATED)


######################################################################
# UPDATE AN EXISTING WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["PUT"])
def update_wishlists(wishlist_id):
    """
    Update a Wishlist
    This endpoint will update a Wishlist based the body that is posted
    """
    app.logger.info("Request to update account with id: %s", wishlist_id)
    check_content_type("application/json")

    # See if the wishlist exists and abort if it doesn't
    wishlist = Wishlist.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND, f"Wishlist with id '{wishlist_id}' was not found."
        )

    # Update from the json in the body of the request
    wishlist.deserialize(request.get_json())
    wishlist.id = wishlist_id
    wishlist.update()

    return make_response(jsonify(wishlist.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["DELETE"])
def delete_wishlists(wishlist_id):
    """
    Delete an Wishlist
    This endpoint will delete an Wishlist based the id specified in the path
    """
    app.logger.info("Request to delete wishlist with id: %s", wishlist_id)

    # Retrieve the wishlist to delete and delete it if it exists
    wishlist = Wishlist.find(wishlist_id)
    if wishlist:
        wishlist.delete()

    return make_response("", status.HTTP_204_NO_CONTENT)



######################################################################
# UPDATE AN ITEM
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["PUT"])
def update_items(wishlist_id, item_id):
    """
    Update an Item
    This endpoint will update an Item based the body that is posted
    """
    app.logger.info(
        "Request to update Item %s for Wishlist id: %s", (item_id, wishlist_id)
    )
    check_content_type("application/json")

    # See if the item exists and abort if it doesn't
    item = Item.find(item_id)
    if not item:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{item_id}' could not be found.",
        )
    # Update from the json in the body of the request
    item.deserialize(request.get_json())
    item.id = item_id
    item.update()

    return make_response(jsonify(item.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE AN ITEM
######################################################################
@app.route("/wishlists/<int:wishlist_id>/items/<int:item_id>", methods=["DELETE"])
def delete_items(wishlist_id, item_id):
    """
    Delete an Item
    This endpoint will delete an Item based the id specified in the path
    """
    app.logger.info(
        "Request to delete Item %s for Wishlist id: %s", (item_id, wishlist_id)
    )

    # See if the item exists and delete it if it does
    item = Item.find(item_id)
    if item:
        item.delete()

    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
