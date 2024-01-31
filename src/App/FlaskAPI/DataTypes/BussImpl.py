
class DisplayItem:
    def __init__(self,
                 product_id,
                 product_link,
                 product_is_on_sale,
                 product_name,
                 product_image_link,
                 product_history_minimum_price,
                 product_current_price,
                 product_current_price_range,
                 product_category):
        self.product_id = product_id
        self.product_link = product_link
        self.product_is_on_sale = product_is_on_sale
        self.product_name = product_name
        self.product_image_link = product_image_link
        self.product_history_minimum_price = product_history_minimum_price
        self.product_current_price = product_current_price
        self.product_current_price_range = product_current_price_range
        self.product_category = product_category

    def __str__(self):
        return " ".join(
            [
                self.product_id,
                self.product_category,
                self.product_name,
                self.product_current_price,
                "is on sale" if self.product_is_on_sale else "not on sale",
                self.product_link,
                self.product_image_link, "\n"
            ]
        )

    def obj_dict(obj):
        return obj.__dict__
