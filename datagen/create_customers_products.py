import pandas as pd
import numpy as np

num_customers = 100000 #1000000

customers_df = pd.DataFrame(
    {
    "cust_id": range(1000000, 1000000 + num_customers),
    "is_male": np.tile([True, False], int(num_customers / 2)),
    "location": np.tile([1, 2, 3, 4], int(num_customers / 4))
    }
)

num_products =  10000

productsdf = pd.DataFrame(
    {
    "product_id": range(10000, 10000 + num_products),
    "food": np.tile([True, False], int(num_products / 2)),
    "price": np.clip(np.round(np.random.normal(100, 25, size=num_products)*100) / 100, a_min = 0, a_max=1000),
    "brand": np.random.choice(["basic", "premium", "luxury"], num_products),
    "at_location": np.tile([[1], [1,2], [1,2,3], [1,2,3,4]], int(num_products / 4))
    }
)

print("Eporting customers")
customers_df.to_csv("../data/customers{}.csv".format(num_customers), index=False)
print("Eporting products")
productsdf.to_csv("../data/products{}.csv".format(num_products), index=False)
