import pandas as pd
import numpy as np

import plotly.offline as pyo
import plotly.graph_objs as go

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import Window
from pyspark.sql.types import StructType, StructField, IntegerType, LongType, StringType
import pyspark.sql.functions as F

from . import configure_logger
logger = configure_logger("dist")

def start_spark():
    spark = (
        SparkSession
        .builder
        .appName("train")
        .master("local[*]")
        .getOrCreate()
    )

    return spark

def read_file(
    spark : pyspark.sql.SparkSession,
    csv_f : str) -> pyspark.sql.DataFrame:

    # Create schema of the dataset
    schema = StructType(
        [
            StructField("session", IntegerType(), True),
            StructField("aid", IntegerType(), True),
            StructField("ts", LongType(), True),
            StructField("type", StringType(), True)
        ]
    )

    df = (
        spark.read
        .option("delimiter", ',')
        .option("header", "true")
        .schema(schema)
        .csv(csv_f)
    )

    return df

def get_type_dist(df : pyspark.sql.DataFrame) -> pd.DataFrame:
   
    df = (
        df.groupBy("type")
        .agg(F.count("session").alias("type_count"))
    )

    pd_df = df.toPandas()

    n_count = pd_df["type_count"].sum()

    pd_df["type_dist"] = (100 * pd_df["type_count"] / n_count).round(2)

    return pd_df

def indicate_types(df : pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:

    # df = (
    #     df.groupBy("session")
    #     .agg(
    #         F.collect_set("type").alias("type_set")
    #     )
    #     .select(
    #         "session",
    #         F.when(F.lit("clicks").isin("type_set"), 1).otherwise(0).alias("has_click"),
    #         F.when(F.lit("carts").isin("type_set"), 1).otherwise(0).alias("has_cart"),
    #         F.when(F.lit("orders").isin("type_set"), 1).otherwise(0).alias("has_order")
    #     )
    # )
    df = (
        df.groupBy("session")
        .agg(
            F.collect_set("type").alias("type_set")
        )
        .select(
            "session",
            F.when(F.array_contains("type_set", "clicks"), 1).otherwise(0).alias("has_click"),
            F.when(F.array_contains("type_set", "carts"), 1).otherwise(0).alias("has_cart"),
            F.when(F.array_contains("type_set", "orders"), 1).otherwise(0).alias("has_order")
        )
    )

    return df


def make_bar(train_pd : pd.DataFrame, test_pd : pd.DataFrame, html_f : str):
    data = [
        go.Bar(x=train_pd["type"], y=train_pd["type_dist"], text=train_pd["type_count"], name="train"),
        go.Bar(x=test_pd["type"], y=test_pd["type_dist"], text=test_pd["type_count"], name="test")
    ]

    layout = go.Layout(
        title="Event Types", 
        barmode="group",
        xaxis=dict(title="Type"),
        yaxis=dict(title="Proportion(%)")
        )

    fig = go.Figure(data=data, layout=layout)

    pyo.plot(fig, filename=html_f)


if __name__ == "__main__":
    import os
    from . import CONF_DATA
    from . import HTML_DIR

    # train_csv = CONF_DATA["train"]["raw_csv"]
    # test_csv = CONF_DATA["test"]["raw_csv"]
    # logger.info("Train data : %s", train_csv)
    # logger.info("Test data : %s", test_csv)

    # spark = start_spark()
    # logger.debug("SQL spark session initiated.")

    # df_train = read_file(spark, train_csv)
    # pd_train = get_type_dist(df_train)
    # logger.info("Distribution of event types in train data:\n" + str(pd_train.head()))

    # df_test = read_file(spark, test_csv)
    # pd_test = get_type_dist(df_test)
    # logger.info("Distribution of event types in test data:\n" + str(pd_test.head()))
    
    # html_f = os.path.join(HTML_DIR, "dist.html")
    # make_bar(pd_train, pd_test, html_f)
    # logger.info("Distribution barcharts for train and test data generated in %s", html_f)

    spark = start_spark()
    
    train_csv = CONF_DATA["test"]["raw_csv"]

    train_df = read_file(spark, train_csv)

    train_df = indicate_types(train_df) 

    train_df.show(20)

    spark.stop()