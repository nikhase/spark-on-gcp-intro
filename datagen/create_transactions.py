"""Perform this via
```
gcloud dataproc jobs submit pyspark datagen/create_transactions.py \
--cluster=YOUR_CLUSTER_NAME \
--region=YOUR_REGION \
```
"""
from pyspark.sql import SparkSession
import pyspark.sql.functions as sqlf
from datetime import datetime

DATADIR = "gs://spark-intro/data/"
CUSTOMER_SAMPLE = 0.5
print("User Sample Size: ", CUSTOMER_SAMPLE)

ss = SparkSession.builder.enableHiveSupport().getOrCreate()

customers = ss.read.option("header", True).option("inferSchema", True).csv(DATADIR + "customers100000.csv")
customers.printSchema()
customers.show()
num_customers = customers.count()

products = ss.read.option("header", True).option("inferSchema", True).csv(DATADIR + "products10000.csv")
products.printSchema()
products.show(5)
num_products = products.count()

# # Common Task: Do a crossJoin

# How many rows to expect?
# num_customers * num_products * 2 columns * 8byte precision / 10**9 = memory footprint in GB
print("Expected in-memory footprint in GB: ", CUSTOMER_SAMPLE * num_customers * num_products * 2 * 8 / 10**9)


# Do the cross join. .repartition is crucial here
transactions = customers.sample(CUSTOMER_SAMPLE).repartition(int(100*CUSTOMER_SAMPLE)).crossJoin(products)
transactions.createOrReplaceTempView("transactions")

# Add a random date between January and December 2018
jan18 = datetime.strptime("2018-01-01", "%Y-%m-%d")
dec18 = datetime.strptime("2018-12-31", "%Y-%m-%d")

print("Create artificial timestamp ...")
tmp = transactions.limit(1000)
tmp.withColumn("date", (jan18.timestamp() + sqlf.rand() * (dec18.timestamp()-jan18.timestamp())).cast("timestamp")).show()

transactions_w_date = transactions.withColumn("date", (jan18.timestamp() + sqlf.rand() * (dec18.timestamp()-jan18.timestamp())).cast("timestamp"))

print("Writing to Parquet")
transactions_w_date.select(["cust_id", "product_id", "date"]).write.mode("overwrite").parquet(DATADIR + "transactions_sample_{}_pq".format(CUSTOMER_SAMPLE))

print("Writing to CSV")
ss.read.parquet(DATADIR + "transactions_sample_{}_pq".format(CUSTOMER_SAMPLE)).write.option("header", True).csv(
    DATADIR + "transactions_sample_{}_csv".format(CUSTOMER_SAMPLE)
    )
