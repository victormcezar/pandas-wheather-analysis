import os
import logging
import awswrangler as wr
from datetime import datetime

BUCKET_NAME = os.getenv("BUCKET_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")
TABLE_NAME = os.getenv("TABLE_NAME")
PARTITION_COLUMN = os.getenv("PARTITION_COLUMN")


def handler(event, context):
    df = wr.s3.read_csv(f"s3://{BUCKET_NAME}/incoming/",
                        dataset=True,
                        na_values=['null', 'none'],
                        parse_dates=["ObservationDate"])

    df = add_etl_metadata_to_df(df)
    df["ObservationDate"] = df["ObservationDate"].dt.date

    wr.s3.copy_objects(
        paths=wr.s3.list_objects(f"s3://{BUCKET_NAME}/incoming"),
        source_path=f"s3://{BUCKET_NAME}/incoming",
        target_path=f"s3://{BUCKET_NAME}/processed/{datetime.today()}")
    wr.s3.delete_objects(f"s3://{BUCKET_NAME}/incoming/")

    wr.s3.to_parquet(df=df,
                     path=f"s3://{BUCKET_NAME}/dataset/",
                     dataset=True,
                     database=DATABASE_NAME,
                     table=TABLE_NAME,
                     mode="overwrite_partitions",
                     partition_cols=[PARTITION_COLUMN],
                     dtype={'ObservationDate': 'date'})


def add_etl_metadata_to_df(dataframe):
    logging.info('Adding ETL metadata.')
    dataframe['dl_creation_date'] = datetime.today().date()
    return dataframe


def setup_logging():
    root = logging.getLogger()
    if root.handlers:
        for h in root.handlers:
            root.removeHandler(h)
    logging.basicConfig(
        format='[%(asctime)s][%(name)s][%(funcName)s] %(message)s',
        level='INFO')
