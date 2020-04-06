import unittest
import utils


class TypeofTest(unittest.TestCase):
    def setUp(self) -> None:
        '''
        测试之前的准备工作
        :return:
        '''
        self.t1 = utils.Typeof(4)
        self.t2 = utils.Typeof([4])
    def tearDown(self) -> None:
        '''
        测试之后的收尾
        如关闭数据库
        :return:
        '''
        pass

    def test_Typeof(self):
        ret1 = self.t1
        ret2 = self.t2
        self.assertEqual(ret1, utils.INT)
        self.assertEqual(ret2, utils.LIST)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TypeofTest('test_Typeof'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
