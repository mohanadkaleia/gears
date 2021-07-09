import tinydb

from pathlib import Path
from dataclasses import dataclass
from slugify import slugify
from app import util
from app.forms import FormNewServices


class ErrNotFound(Exception):
    pass


class ErrInvalidParameters(Exception):
    pass


class ServiceRepo:

    def __init__(self, db: tinydb.TinyDB):
        self.db = db
        self.services = db.table('services')

    def insert(self, id="",
               shop_id="",
               name="",
               slug="",
               description="",
               price="",
               images=None):

        doc = {"shop_id": shop_id,
               "id": id,
               "name": name,
               "slug": slug,
               "description": description,
               "price": price,
               "images": images if images is not None else []}
        self.services.insert(doc)
        return id

    def update(self, id="",
               name="",
               slug="",
               description="",
               price="",
               images=None):
        query = tinydb.Query()
        doc = {"name": name,
               "slug": slug,
               "description": description,
               "price": price,
               "images": images if images is not None else []}
        self.services.update(doc, query.id == id)
        return id

    def delete(self, id):
        query = tinydb.Query()
        self.db.table('services').remove(query.id == id)

    def all(self):
        results = self.services.all()

        if not results:
            raise ErrNotFound("oops.. no service found in the db")

        return [Service(**doc) for doc in results]

    def get(self, id: str):
        service = tinydb.Query()
        result = self.services.search(service.id == id)

        if not result:
            raise ErrNotFound(f"no service found for the provided id: {id}")

        return Service(**result.pop())

    def get_by_name(self, name=""):
        if not name:
            raise ErrInvalidParameters("service name must be provided")

        service = tinydb.Query()
        result = self.services.search(service.name == name)

        if not result:
            raise ErrNotFound(f"no service found for the provided name: {name}")

        return result[0]


class Service:
    UPLOADED_DIR_PATH: str = str(Path.cwd() / Path("app/static/uploaded"))

    def __init__(self,
                 shop_id: str = None,
                 id: str = None,
                 name: str = None,
                 slug: str = None,
                 description: str = None,
                 price: float = None,
                 images: list = None):
        self.shop_id = shop_id
        self.id = id or util.random_id(initial="sh")
        self.name = name
        self.slug = slug or slugify(name)
        self.description = description
        self.price = price
        self.images = images


    @property
    def upload_dir(self):
        directory = Path(Service.UPLOADED_DIR_PATH) / Path(self.id)
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    @property
    def prefix_images(self):
        return [Path(self.upload_dir)/Path(image) for image in self.images]

    @classmethod
    def populate(cls, form: FormNewServices):
        return cls(shop_id="FAKE ID:FIX ME",
                   name=form.name.data,
                   slug=slugify(form.name.data),
                   description=form.description.data,
                   price=form.price.data)

    @classmethod
    def populate_edit(cls, service, form: FormNewServices):
        return cls(shop_id="FAKE ID:FIX ME",
                   id=service.id,
                   images=service.images,
                   name=form.name.data,
                   slug=slugify(form.name.data),
                   description=form.description.data,
                   price=form.price.data)
