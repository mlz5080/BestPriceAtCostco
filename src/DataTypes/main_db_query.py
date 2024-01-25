from MySQL import MySQLCostcoItem
from Dynamo import DynamoCostcoItem

if __name__ == '__main__':
    obj1 = MySQLCostcoItem("1", "test", "8.99", None, True, ".com", "image.com", "test_category")
    obj1.update_item()

    # obj2 = DynamoCostcoItem("1", "test", "9.99", "-1", True, ".com", "image.com", "test_category")
    # obj2.update_item()