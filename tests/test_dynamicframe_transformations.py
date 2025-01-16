import os

import pytest
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, StructField, StructType


@pytest.fixture(scope="session")
def glue_context():
    """Fixture for creating a Glue context"""
    sc = SparkContext()
    sc.setLogLevel("ERROR")
    glue_context = GlueContext(sc)
    spark = glue_context.spark_session

    return spark, glue_context


@pytest.fixture
def sample_dyf(glue_context):
    """Fixture for creating sample DynamicFrame"""

    schema = StructType(
        [
            StructField("id", IntegerType(), False),
            StructField("name", StringType(), True),
            StructField("department", StringType(), True),
        ]
    )

    data = [
        (1, "John Doe", "Engineering"),
        (2, "Jane Smith", "Marketing"),
        (3, "Bob Wilson", "Engineering"),
    ]
    spark_sesssion, glue_context = glue_context
    df = spark_sesssion.createDataFrame(data, schema)
    dyf = DynamicFrame.fromDF(df, glue_context, "sample_dyf")

    return dyf


def test_dyf_filter_by_department(glue_context, sample_dyf):
    """Test filtering DynamicFrame by department"""
    # Filter for Engineering department using DynamicFrame's filter
    filtered_dyf = sample_dyf.filter(f=lambda x: x["department"] == "Engineering")

    # Convert to DataFrame for easier assertions
    filtered_df = filtered_dyf.toDF()

    # Assert the count
    assert filtered_df.count() == 2

    # Assert the results contain expected names
    engineers = [row.name for row in filtered_df.collect()]
    assert "John Doe" in engineers
    assert "Bob Wilson" in engineers
    assert "Jane Smith" not in engineers


def test_dyf_mapping_transformation(glue_context, sample_dyf):
    """Test applying mapping transformation to DynamicFrame"""

    # Define mapping to create email addresses
    def add_email(rec):
        rec["email"] = f"{rec['name'].lower().replace(' ', '.')}@company.com"
        return rec

    # Apply mapping
    mapped_dyf = sample_dyf.map(f=add_email)

    # Convert to DataFrame for assertions
    result_df = mapped_dyf.toDF()

    # Assert new column exists
    assert "email" in result_df.columns

    # Assert email was created correctly
    first_row = result_df.first()
    assert first_row.email == "john.doe@company.com"


def test_dyf_join_operation(glue_context, sample_dyf):
    """Test joining two DynamicFrames"""
    # Create another DynamicFrame with department info
    spark_sesssion, glue_context = glue_context
    dept_data = spark_sesssion.createDataFrame(
        [("Engineering", "Tech"), ("Marketing", "Business")], ["department", "division"]
    )

    dept_dyf = DynamicFrame.fromDF(dept_data, glue_context, "dept_dyf")

    # Join DynamicFrames
    joined_dyf = sample_dyf.join(["department"], ["department"], dept_dyf)

    # Convert to DataFrame for assertions
    result_df = joined_dyf.toDF()

    # Assert join was successful
    assert "division" in result_df.columns
    assert (
        result_df.filter(result_df.department == "Engineering").first().division
        == "Tech"
    )


def test_dyf_drop_fields(glue_context, sample_dyf):
    """Test dropping fields from DynamicFrame"""
    # Drop the gender field
    reduced_dyf = sample_dyf.drop_fields(["gender"])

    # Convert to DataFrame for assertions
    result_df = reduced_dyf.toDF()

    # Assert field was dropped
    assert "gender" not in result_df.columns
    assert "name" in result_df.columns
    assert "department" in result_df.columns
