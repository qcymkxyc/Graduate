import unittest

from app.util import cos

class COSTestCase(unittest.TestCase):
    """
    腾讯云测试
    """
    def test_cos_upload(self):
        """
        腾讯云cos上传测试
        """
        cos.upload_binary_file(b"abcde","login_success.txt")




if __name__ == '__main__':
    unittest.main()
