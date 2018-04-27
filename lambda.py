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
destination_bucket = 'aimeeb-datasets-public'
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
    city = '-'.join(row['city'].split(' '))
    location = '-'.join(row['location'].split(' '))
    city_location = '_'.join([city, location])
    # TODO: Update locations.json file
    parameter = row['parameter']
    value = float(row['value'])
    cityDatime = row['local'][0:19]
    timestamp = int(1000*time.mktime(datetime.datetime.strptime(cityDatime, "%Y-%m-%dT%H:%M:%S").timetuple()))
    if city_location not in data_grouped:
      data_grouped[city_location] = {}
    if parameter not in data_grouped[city_location]:
      data_grouped[city_location][parameter] = []
    data_grouped[city_location][parameter].append([timestamp, value])
  
  # load existing highcharts data
  # city = 'Delhi'
  print(json.dumps(data_grouped, indent=2))
  for location in data_grouped.keys():
    for parameter in data_grouped[location].keys():
      s3Key = 'openaq/timeseries/{0}/{1}/all-highcharts.json'.format(location, parameter)
      obj = s3.Object(destination_bucket, s3Key)
      try:
        existing_data = json.loads(obj.get()['Body'].read().decode('utf-8'))
      except Exception as err:
        existing_data = []
        print('Got error: {0}'.format(err))
      for idx, measurement in enumerate(location[parameter]):
        if measurement not in existing_data:
          existing_data.append(measurement)
      obj.put(Bucket=destination_bucket, Key=s3Key, Body=json.dumps(existing_data, indent=2), ACL='public-read')
  return 'Success'

lambda_handler(event, {})
