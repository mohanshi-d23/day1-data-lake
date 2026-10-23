import sys
import re

from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

DATABASE = "ev-db"
RAW_TABLE = "raw"
OUTPUT = "s3://mohanshi-mini-datalake-2026/curated/"

# Read the raw table through the Data Catalog
df = glue_context.create_dynamic_frame.from_catalog(
    database=DATABASE, table_name=RAW_TABLE
).toDF()
print(f"Raw rows: {df.count()}")

# 1. Rename columns to snake_case, handling spaces, brackets, and hyphens
def to_snake(name):
    return re.sub(r"[^0-9a-zA-Z]+", "_", name).strip("_").lower()

df = df.toDF(*[to_snake(c) for c in df.columns])

# 2. Fix types
df = (
    df.withColumn("model_year", F.col("model_year").cast("int"))
      .withColumn("electric_range", F.col("electric_range").cast("int"))
      .withColumn("legislative_district", F.col("legislative_district").cast("int"))
      .withColumn("dol_vehicle_id", F.col("dol_vehicle_id").cast("long"))
)

# 3. Remove duplicates: exact copies first, then repeated vehicle IDs
df = df.dropDuplicates()
df = df.dropDuplicates(["dol_vehicle_id"])
print(f"Rows after dedupe: {df.count()}")

# 4. Write partitioned Parquet, one folder per model year
(df.write.mode("overwrite")
   .partitionBy("model_year")
   .parquet(OUTPUT))

job.commit()