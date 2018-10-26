import unittest
from app.models import Product
from app import db, create_app


class ProductModelTestCase(unittest.TestCase):
    def setUp(self):
        self.product = Product()
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def test_product_add(self):
        self.product.name = "name_test"
        self.product.description = "description_test"

        db.session.add(self.product)
        db.session.commit()

        print(self.product.id)

    def test_product_cn_add(self):
        """
        测试中文插入
        :return:
        """
        self.product.name = "中文名"
        self.product.description = "中文描述"

        db.session.add(self.product)
        db.session.commit()

    def test_generate_prodoct(self):
        """生成假数据"""
        Product.generate_fake(100)

    def tearDown(self):
        pass
