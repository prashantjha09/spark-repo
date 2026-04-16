from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("K8sDemo").getOrCreate()

data = [(i, i*10) for i in range(1, 100)]
df = spark.createDataFrame(data, ["id", "value"])

# Force distribution
df = df.repartition(4)

df.groupBy().sum("value").show()

import time
time.sleep(300)  # keep pod alive to observe
