import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('models_usa').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+
assert spark.version >= '2.3'  # make sure we have Spark 2.3+

demographics_directory = sys.argv[1]
# restaurants_directory = sys.argv[2]

def filename_to_county(filename):
    pos_start = filename.find('cleanedcounties/') + 16  # first occurence of substring
    pos_end = filename.find(',%20')
    if pos_start > -1:
        return filename[pos_start:pos_end].replace("%20", " ")

def to_int(num):
    n = num.replace(',', '')
    return int(n)

demographics = spark.read.csv(demographics_directory, header = True).withColumn('filename', functions.input_file_name())
to_county = functions.udf(lambda x: filename_to_county(x), returnType=types.StringType())
pop_int = functions.udf(lambda x: to_int(x), returnType = types.IntegerType())
demographics = demographics.select(
                demographics['origin'],
                pop_int(demographics['population']).alias('population'),
                to_county(demographics['filename']).alias('county'))
demographics = demographics.filter(demographics['origin'].isin(['Total:', 'Europe:']))

# #get the percentage, of foreign population
pivot = demographics.groupby(demographics['county'])
demographics = pivot.pivot('origin').sum('population').fillna(0)
demographics = demographics.cache()
demographics = demographics.withColumn('percent of European migrants', functions.round(demographics['Europe:']/demographics['Total:']*100, 4))
demographics = demographics.select(
                demographics['county'],
                demographics['percent of European migrants']).distinct()
demographics = demographics.sort(demographics['county'])

demographics.show(demographics.count(), truncate = False)
