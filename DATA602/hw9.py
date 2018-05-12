import pandas as pd


# 21 lines include an extra double quotation mark; those lines have been dropped
epa = pd.read_csv('/Users/brucehao/Google Drive/CUNY/git/DATA602/epa-http.txt',
                    header=None, sep='\s+', error_bad_lines=False)

# assign column names
epa.columns = ['host', 'date', 'request', 'reply', 'bytes']

# convert bytes column from object to integer
# epa.head()
# epa.info()
epa['bytes'] = pd.to_numeric(epa['bytes'], errors='coerce')


# host name that made the most requests
print(epa.groupby('host')['host'].count().reset_index(name='count').sort_values(by='count', ascending=False).head(1))


# host name that received the most bytes from the server
print(epa.groupby('host')['bytes'].sum().reset_index(name='total_bytes').
      sort_values(by='total_bytes', ascending=False).head(1))


# busiest hour in terms of requests
# add hour column based on datetime split
epa['hour'] = epa['date'].str.split(":").str[1]
# epa.head()
print(epa.groupby('hour')['hour'].count().reset_index(name='count').sort_values(by='count', ascending=False).head(1))


# most downloaded gif image
# add gif column based on extracted gif name
epa['gif'] = epa['request'].str.extract("(\w+).gif")
# epa.head(10)
print(epa.loc[epa['gif'].notnull(), :].groupby('gif')['gif'].count().reset_index(name='count').
      sort_values('count', ascending=False).head(1))


#  HTTP reply codes other than 200
print(epa.loc[epa['reply'] != 200]['reply'].unique())
