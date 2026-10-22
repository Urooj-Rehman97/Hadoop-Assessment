
from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("Penguins Analysis") \
    .getOrCreate()

# Read cleaned CSV from HDFS
df = spark.read.csv(
    "hdfs:///user/maria_dev/T3Task/penguins_clean.csv",
    header=True,
    inferSchema=True
)

# Display dataset schema
print("Penguins Dataset Schema:")
df.printSchema()

# Display first five records
df.show(5)

# Stop Spark session
spark.stop()
