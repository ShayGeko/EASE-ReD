import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('models').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5)  # make sure we have Python 3.5+
assert spark.version >= '2.3'  # make sure we have Spark 2.3+

demographics_directory = sys.argv[1]
# restaurants_directory = sys.argv[2]

def filename_to_city(filename):
    pos_start = filename.find('cleanedcensus/') + 14  # first occurence of substring
    pos_end = filename.find('.csv')
    if pos_start > -1:
        return filename[pos_start:pos_end].replace("%20", " ")

def residency(country):
    if country != 'Canada':
        return 'foreign'
    else:
        return 'Canada'

demographics = spark.read.option('header', True).csv(demographics_directory).withColumn('filename', functions.input_file_name())
to_city = functions.udf(lambda x: filename_to_city(x), returnType=types.StringType())
foreign = functions.udf(lambda x: residency(x), returnType=types.StringType())
demographics = demographics.select(
                foreign(demographics['origin']).alias('origin'),
                demographics['population'],
                to_city(demographics['filename']).alias('city'))

#get canadian and foreign population
grouped = demographics.groupby(demographics['city'], demographics['origin'])
demographics = grouped.agg(functions.sum(demographics['population']).alias('population'))
demographics = demographics.cache()
demographics = demographics.sort(demographics['city'])

#get the percentage, of foreign population
pivot = demographics.groupby(demographics['city'])
demographics = pivot.pivot('origin').sum('population').fillna(0)
demographics = demographics.cache()
demographics = demographics.withColumn('percentage of foreign population', functions.round(demographics['foreign']/(demographics['Canada'] + demographics['foreign'])*100, 2))
demographics = demographics.select(
                demographics['city'],
                demographics['percentage of foreign population'])
demographics.show()
