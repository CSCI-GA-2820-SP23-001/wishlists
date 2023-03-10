"""
Models for Wishlists

All of the models are stored in this module
"""
import logging
from datetime import date
from abc import abstractmethod
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


def init_db(app):
    """Initialize the SQLAlchemy app"""
    Wishlist.init_db(app)


######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase:
    """Base class added persistent methods"""

    def __init__(self):
        self.id = None  # pylint: disable=invalid-name

    @abstractmethod
    def serialize(self) -> dict:
        """Convert an object into a dictionary"""

    @abstractmethod
    def deserialize(self, data: dict) -> None:
        """Convert a dictionary into an object"""

    def create(self):
        """
        Creates a Account to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Account to the database
        """
        logger.info("Updating %s", self.name)
        db.session.commit()

    def delete(self):
        """Removes a Account from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the records in the database"""
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a record by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)


######################################################################
#  I T E M   M O D E L
######################################################################
class Item(db.Model, PersistentBase):
    """
    Class that represents an Item
    """

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    wishlist_id = db.Column(db.Integer, db.ForeignKey("wishlist.id", ondelete="CASCADE"), nullable=False)
    item_id = db.Column(db.Integer)
    count = db.Column(db.Integer)


    def __repr__(self):
        return f"<Item {self.item_id} id=[{self.id}] wishlist[{self.wishlist_id}]>"

    def __str__(self):
        return f"{self.id}: {self.item_id}, {self.wishlist_id}, {self.count}"

    def serialize(self) -> dict:
        """Converts an Item into a dictionary"""
        return {
            "id": self.id,
            "wishlist_id": self.wishlist_id,
            "item_id": self.item_id,
            "count": self.count
        }

    def deserialize(self, data: dict) -> None:
        """
        Populates an Address from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.id = data["id"]
            self.wishlist_id = data["wishlist_id"]
            self.item_id = data["item_id"]
            self.count = data["count"]
        except KeyError as error:
            raise DataValidationError("Invalid Wishlist: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Wishlist: body of request contained "
                "bad or no data " + error.args[0]
            ) from error
        return self


######################################################################
#  W I S H L I S T   M O D E L
######################################################################
class Wishlist(db.Model, PersistentBase):
    """
    Class that represents an Wishlist
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    items = db.relationship("Item", backref="wishlist", passive_deletes=True)

    def __repr__(self):
        return f"<Wishlists {self.name} id=[{self.id}]>"

    def serialize(self):
        """Converts an Wishlist into a dictionary"""
        wishlist = {
            "id": self.id,
            "account": self.account_id,
            "name": self.name,
            "items": [],
        }
        for item in self.items:
            wishlist["items"].append(item.serialize())
        return wishlist

    def deserialize(self, data):
        """
        Populates an Account from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.id = data["id"]
            self.account = data["account_id"]
            self.name = data["name"]
            # handle inner list of addresses
            items_list = data.get("items")
            for json_items in items_list:
                item = Item()
                item.deserialize(json_items)
                self.items.append(item)
        except KeyError as error:
            raise DataValidationError("Invalid Wishlist: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Wishlist: body of request contained "
                "bad or no data - " + error.args[0]
            ) from error
        return self

    @classmethod
    def find_by_name(cls, name):
        """Returns all Wishlists with the given name

        Args:
            name (string): the name of the Wishlists you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
