import tinydb

from app import util


class ErrNotFound(Exception):
    pass


class ErrInvalidParameters(Exception):
    pass


class ShopRepo:

    def __init__(self, db: tinydb.TinyDB):
        self.db = db
        self.shops = db.table('shops')

    def insert(self, id="",
               name="",
               description="",
               logo="",
               phone="",
               email="",
               hours=""):
        # TODO: validate the information, for example we can't have two shops with same name
        pass

        # TODO: upload the logo as an image
        pass

        self.shops.insert({"id": id,
                           "name": name,
                           "description": description,
                           "logo": logo,
                           "phone": phone,
                           "email": email,
                           "hours": hours})
        return id

    def get_by_name(self, name: str):
        if not name:
            raise ErrInvalidParameters("name parameter is required")

        shop = tinydb.Query()
        result = self.shops.search(shop.name == name)

        if not result:
            raise ErrNotFound(f"no data found for the provided name: {name}")
        return Shop(**result.pop())


class Shop:
    def __init__(self, id: str = None,
                 name: str = None,
                 description: str = None,
                 logo: str = None,
                 email: str = None,
                 phone: str = None,
                 hours: list = []):
        self.id = id or util.random_id(initial="s")
        self.name = name
        self.description = description
        self.logo = logo
        self.email = email
        self.phone = phone
        self.hours = hours
