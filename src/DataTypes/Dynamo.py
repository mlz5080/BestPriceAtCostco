import boto3
from .BussImpl import CostcoItem

class DynamoCostcoItem(CostcoItem):
    
    client = boto3.client('dynamodb')
    costco_db_table_name = "costco-products-info"

    def __init__(self, item_id, name, price, price_range, is_on_sale, product_link, image_link, category):
        super().__init__(item_id, name, price, price_range, is_on_sale, product_link, image_link, category)

    def update_item(self):
        try:
            ExpressionAttributeNames = {
                '#min': 'product_history_minimum_price'
            }

            ExpressionAttributeValues={
                ':price': {
                    'N': self.price,
                }
            }

            # Product update minimum price
            Key={'product_id': {'S':self.id}}
            UpdateExpression = "SET #min = :price"
            ConditionExpression ="attribute_not_exists(#min) OR #min < :price"
            ReturnValues = "NONE"
            print("Updating Minimum price", self.name)
            DynamoCostcoItem.client.update_item(
                ExpressionAttributeNames=ExpressionAttributeNames,
                ExpressionAttributeValues=ExpressionAttributeValues,
                Key=Key,
                ReturnValues=ReturnValues,
                TableName=DynamoCostcoItem.costco_db_table_name,
                UpdateExpression=UpdateExpression,
                ConditionExpression=ConditionExpression
            )
            print("Minimum Price updated")
        except Exception as e:
            print(e)
            print(self.name, "has no minimum price update")

        try:
            ExpressionAttributeValues={
                ':price': {
                    'N': self.price,
                },
                ':link': {
                    'S': self.link,
                },
                ':name': {
                    'S': self.name,
                },
                ':imageLink': {
                    'S': self.image_link,
                },
                ':onSale': {
                    'BOOL': self.is_on_sale,
                },
                ':priceRange': {
                    'N': self.price_range,
                },
                ':category': {
                    'S': self.category,
                },
            }
            ExpressionAttributeNames = {
                '#onSale': 'product_is_on_sale',
                '#link': 'product_link',
                '#name': 'product_name',
                '#imageLink': 'product_image_link',
                '#price': 'product_current_price',
                '#priceRange': 'product_current_price_range',
                '#category': 'product_category'
            }
            Key={'product_id': {'S':self.id}}
            ReturnValues = "NONE"
            UpdateExpression = "SET #price = :price, #link = :link, #name = :name, #imageLink = :imageLink, #onSale = :onSale, #priceRange = :priceRange, #category = :category"
            ConditionExpression ="attribute_not_exists(#link) OR #link <> :link"
            ConditionExpression += " OR attribute_not_exists(#price) OR #price <> :price"
            ConditionExpression += " OR attribute_not_exists(#imageLink) OR #imageLink <> :imageLink"
            ConditionExpression += " OR attribute_not_exists(#onSale) OR #onSale <> :onSale"
            ConditionExpression += " OR attribute_not_exists(#name) OR #name <> :name"
            ConditionExpression += " OR attribute_not_exists(#priceRange) OR #priceRange <> :priceRange"
            ConditionExpression += " OR attribute_not_exists(#category) OR #category <> :category"
            print("Updating other information", self.name)
            DynamoCostcoItem.client.update_item(
                ExpressionAttributeNames=ExpressionAttributeNames,
                ExpressionAttributeValues=ExpressionAttributeValues,
                Key=Key,
                ReturnValues=ReturnValues,
                TableName=DynamoCostcoItem.costco_db_table_name,
                UpdateExpression=UpdateExpression,
                ConditionExpression=ConditionExpression
            )
            print("Updated other information", self.name)
        except Exception as e:
            print(e)
            print(self.name, "has no basic information update")