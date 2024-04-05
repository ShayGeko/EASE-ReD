import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('models').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

demographics_directory = sys.argv[1]
# restaurants_directory = sys.argv[2]

demographics = spark.read.option('header', True).csv(demographics_directory)
demographics = demographics.filter(
                demographics['nationality'] != 'Total Classes in CSV')
grouped = demographics.groupby(demographics['nationality'])
demographics = grouped.agg(functions.avg(demographics['percentage']).alias('percentage'))

Central_Asia = ['Kazakhstan', 'Kyrgyzstan', 'Tajikistan', 'Turkmenistan', 'Uzbekistan']
Eastern_Asia = ['China', 'North Korea', 'Japan', 'Mongolia', 'South Korea']
Southern_Asia = ['Afghanistan', 'Bangladesh', 'Bhutan', 'India', 'Iran', 'Maldives', 'Nepal', 'Pakistan', 'Sri Lanka']
Southeast_Asia = ['Brunei', 'Cambodia', 'Indonesia', 'Laos', 'Malaysia', 'Myanmar', 'Philippines', 'Singapore', 'Thailand', 
                  'East Timor', 'Vietnam']
Western_Asia = ['Armenia', 'Azerbaijan', 'Bahrain', 'Cyprus', 'Georgia', 'Iraq', 'Israel', 'Jordan', 'Kuwait', 'Lebanon', 
                'Oman', 'Qatar', 'Saudi Arabia', 'Syria', 'Turkey', 'United Arab Emirates', 'Yemen']
Asia = Central_Asia + Eastern_Asia + Southern_Asia + Southeast_Asia + Western_Asia
Africa = ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cape Verde', 'Cameroon', 'Central African Republic', 
          'Chad', 'Comoros', 'Congo', 'Ivory Coast', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia',
          'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi',
          'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe',
          'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia',
          'Uganda', 'Zambia', 'Zimbabwe']
Europe = ['Albania', 'Andorra', 'Latvia', 'Liechtenstein', 'Armenia', 'Austria', 'Lithuania', 'Luxembourg', 'Belarus', 'Malta', 'Moldova',
           'Belgium', 'Bosnia and Herzegovina', 'Monaco', 'Montenegro', 'Bulgaria', 'Croatia', 'Netherlands', 'Norway', 'Cyprus', 
           'Czech Republic', 'Poland', 'Portugal', 'Denmark', 'Estonia', 'Romania', 'Russia', 'Finland', 'Macedonia', 'San Marino', 'Serbia',
             'France', 'Georgia', 'Slovakia', 'Slovenia', 'Germany', 'Greece', 'Spain', 'Sweden', 'Hungary', 'Iceland', 'Sweden', 'Switzerland', 
             'Ireland', 'Italy', 'Turkey', 'Ukraine', 'United Kingdom']
North_America = ['Antigua and Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada', 'Costa Rica', 'Cuba' 'Dominica', 'Dominican Republic', 
                 'El Salvador', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 
                 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States of America']
South_America = ['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 
                 'Venezuela']
Oceania = ['Australia', 'Fiji', 'Tonga', 'Kiribati', 'Marshall Islands', 'Federated States of Micronesia', 'Nauru', 'New Zealand', 'Palau',
           'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tuvalu', 'Vanuatu']
def continentize(country):
    if country in Asia:
        return 'Asia'
    elif country in Africa:
        return 'Africa'
    elif country in Europe:
        return 'Europe'
    elif country in North_America:
        return 'North America'
    elif country in South_America:
        return 'South America'
    elif country in Oceania:
        return 'Oceania'
    else:
        return None

to_continent = functions.udf(lambda x: continentize(x), returnType = types.StringType())
demographics = demographics.select(
                demographics['nationality'],
                demographics['percentage'],
                to_continent(demographics['nationality']).alias('continent'))

demographics = demographics.filter(demographics['continent'] != None)
demographics.show(demographics.count(), truncate = False)