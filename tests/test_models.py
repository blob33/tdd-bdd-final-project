import logging
import unittest
from service.models import Product, Category, db
from tests.factories import ProductFactory

logger = logging.getLogger("flask.app")

class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    def setUp(self):
        """Initialize database for testing"""
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()

    def test_create_product(self):
        """Test creating a product"""
        product = ProductFactory()
        logger.debug("Created Product: %s", product)
        self.assertTrue(product)
        self.assertIsInstance(product, Product)
        self.assertIsNotNone(product.name)

    def test_read_product(self):
        """Test reading a product from the database"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)

        found = Product.find(product.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, product.id)
        self.assertEqual(found.name, product.name)
        self.assertEqual(found.description, product.description)
        self.assertEqual(found.price, product.price)
        self.assertEqual(found.available, product.available)
        self.assertEqual(found.category, product.category)

    def test_update_product(self):
        """Test updating a product"""
        product = ProductFactory()
        product.id = None
        product.create()
        logger.debug("Created Product: %s", product)
        old_id = product.id
        product.description = "Updated description"
        product.update()

        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, old_id)
        self.assertEqual(products[0].description, "Updated description")

    def test_delete_product(self):
        """Test deleting a product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertEqual(len(Product.all()), 1)

        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """Test listing all products"""
        self.assertEqual(len(Product.all()), 0)
        for _ in range(5):
            product = ProductFactory()
            product.id = None
            product.create()
        self.assertEqual(len(Product.all()), 5)

    def test_find_by_name(self):
        """Test finding products by name"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.id = None
            product.create()

        target_name = products[0].name
        expected_count = sum(1 for p in products if p.name == target_name)
        found = Product.find_by_name(target_name)
        self.assertEqual(len(found), expected_count)
        for product in found:
            self.assertEqual(product.name, target_name)

    def test_find_by_availability(self):
        """Test finding products by availability"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.id = None
            product.create()

        target_availability = products[0].available
        expected_count = sum(1 for p in products if p.available == target_availability)
        found = Product.find_by_availability(target_availability)
        self.assertEqual(len(found), expected_count)
        for product in found:
            self.assertEqual(product.available, target_availability)

    def test_find_by_category(self):
        """Test finding products by category"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.id = None
            product.create()

        target_category = products[0].category
        expected_count = sum(1 for p in products if p.category == target_category)
        found = Product.find_by_category(target_category)
        self.assertEqual(len(found), expected_count)
        for product in found:
            self.assertEqual(product.category, target_category)
