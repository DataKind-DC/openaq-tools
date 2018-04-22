import boto3
import json
import csv
from StringIO import StringIO
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import datetime

s3 = boto3.resource('s3')
event = {u'Records': [{u'eventVersion': u'2.0', u'eventTime': u'2018-04-22T21:32:20.599Z', u'requestParameters': {u'sourceIPAddress': u'96.83.79.65'}, u's3': {u'configurationId': u'b5349eb9-f468-42ef-a2fb-308abad33969', u'object': {u'eTag': u'f87dd447fc0b7d82b126a6b2d0b2310d', u'sequencer': u'005ADCFF64838CADCC', u'key': u'openaq/source/2015-06-29.csv', u'size': 16591}, u'bucket': {u'arn': u'arn:aws:s3:::aimeeb-datasets', u'name': u'aimeeb-datasets', u'ownerIdentity': {u'principalId': u'AP7CAEZ5UG61V'}}, u's3SchemaVersion': u'1.0'}, u'responseElements': {u'x-amz-id-2': u'hJq/BC7pFJwYX4A+jgwgno8AGPTAnQUS2ScKp30sxGi6//n2lZYs9QhtpjQnGrM3631ZCPWJdz4=', u'x-amz-request-id': u'84011303F669C3CE'}, u'awsRegion': u'us-east-1', u'eventName': u'ObjectCreated:Put', u'userIdentity': {u'principalId': u'AP7CAEZ5UG61V'}, u'eventSource': u'aws:s3'}]}

def lambda_handler(event, context):
  # load new data
  s3_data = event['Records'][0]['s3']
  bucket = s3_data['bucket']['name']
  key = s3_data['object']['key']
  obj = s3.Object(bucket, key)
  csv_data = obj.get()['Body'].read().decode('utf-8')
  f = StringIO(csv_data)
  reader = csv.DictReader(f, delimiter=',')
  
  data_grouped = {}
  for row in reader:
    city = row['city']
    value = float(row['value'])
    cityDatime = row['local'][0:19]
    timestamp = time.mktime(datetime.datetime.strptime(cityDatime, "%Y-%m-%dT%H:%M:%S").timetuple())
    if city in data_grouped:
      data_grouped[city].append([timestamp, value])
    else:
      data_grouped[city] = []
      data_grouped[city].append([timestamp, value])
  
  # load existing highcharts data
  city = 'Delhi'
  bucket = 'aimeeb-datasets-public'
  key = 'openaq/highcharts/{0}/highcharts.json'.format(city)
  obj = s3.Object(bucket, key)
  try:
    existing_data = json.loads(obj.get()['Body'].read().decode('utf-8'))
  except Exception as err:
    existing_data = []
    print('Got error: {0}'.format(err))
  for measurement in data_grouped[city]:
    if measurement not in existing_data:
      existing_data.append(measurement)
  obj.put(Bucket=bucket, Key=key, Body=json.dumps(existing_data, indent=2))
  return 'Hello from Lambda'

lambda_handler(event, {})