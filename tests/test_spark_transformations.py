import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

@pytest.fixture(scope="session")
def spark():
    """Fixture for creating a spark session"""
    spark = (SparkSession
            .builder
            .master("local[1]")
            .appName("pytest-pyspark-local-testing")
            .getOrCreate())
    yield spark
    spark.stop()

@pytest.fixture
def sample_data(spark):
    """Fixture for creating sample data"""
    schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("name", StringType(), True),
        StructField("department", StringType(), True)
    ])
    
    data = [
        (1, "John Doe", "Engineering"),
        (2, "Jane Smith", "Marketing"),
        (3, "Bob Wilson", "Engineering")
    ]
    
    return spark.createDataFrame(data, schema)

def test_filter_by_department(spark, sample_data):
    """Test filtering dataframe by department"""
    # Filter for Engineering department
    filtered_df = sample_data.filter(sample_data.department == "Engineering")
    
    # Assert the count
    assert filtered_df.count() == 2
    
    # Assert the results contain expected names
    engineers = [row.name for row in filtered_df.collect()]
    assert "John Doe" in engineers
    assert "Bob Wilson" in engineers
    assert "Jane Smith" not in engineers

def test_add_email_column(spark, sample_data):
    """Test adding a new column with transformation"""
    from pyspark.sql.functions import lower, regexp_replace, concat, lit
    # Add email column
    df_with_email = sample_data.withColumn(
        "email",
        concat(regexp_replace(lower(sample_data.name), " ", "."), lit("@company.com"))
    )
    
    # Get the first row
    first_row = df_with_email.first()
    
    # Assert the email was created correctly
    assert first_row.email == "john.doe@company.com"
    assert "email" in df_with_email.columns

def test_department_count(spark, sample_data):
    """Test grouping and counting by department"""
    # Count employees by department
    dept_counts = (sample_data
                  .groupBy("department")
                  .count()
                  .collect())
    
    # Convert to dictionary for easier testing
    count_by_dept = {row["department"]: row["count"] for row in dept_counts}
    
    # Assert the counts
    assert count_by_dept["Engineering"] == 2
    assert count_by_dept["Marketing"] == 1
