
class CostcoItem:
    def __init__(self, item_id, name, price, price_range, is_on_sale, product_link, image_link, category):
        self.id = item_id
        self.price = price
        self.price_range = price_range
        self.name = name
        self.category = category
        self.link = product_link
        self.is_on_sale = is_on_sale
        self.image_link = image_link

    def __str__(self):
        return " ".join(
            [
                self.id,
                self.category,
                self.name,
                self.price,
                "is on sale" if self.is_on_sale else "not on sale",
                self.link,
                self.image_link,"\n"
            ]
        )
