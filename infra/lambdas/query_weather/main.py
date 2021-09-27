import os
import awswrangler as wr

DATABASE_NAME = os.getenv("DATABASE_NAME")
TABLE_NAME = os.getenv("TABLE_NAME")
BUCKET_NAME = os.getenv("BUCKET_NAME")


def handler(event, context):
    df = wr.athena.read_sql_query(
        f"SELECT site_name, region, country, cast(observation_date as varchar) as observation_date FROM {TABLE_NAME} where screen_temperature = (SELECT max(screen_temperature) FROM {TABLE_NAME})",  # noqa: E501
        database=DATABASE_NAME,
        s3_output=f"s3://{BUCKET_NAME}/query-results")

    return df.values.tolist()
