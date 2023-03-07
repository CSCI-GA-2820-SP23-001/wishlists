"""
Delete an Item

This endpoint will delete an Item from the wishlist based on the ID specified in the path
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from service.common import status  # HTTP Status Codes
from service.models import YourResourceModel

# Import Flask application
from . import app


######################################################################
# DELETE AN EXISTING ITEM
######################################################################
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_items(item_id):
    """ 
    Delete an Item
    
    This endpoint will delete an Item from the wishlist based on the ID specified in the path
    """
    app.logger.info("Request to delete item with ID: %s", item_id)
    item = Item.find(item_id)
    if item:
        item.delete()
    
    app.logger.info("Item with ID [%s] delete complete.", item_id)
    return "", status.HTTP_204_NO_CONTENT

######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Place your REST API code here ...
