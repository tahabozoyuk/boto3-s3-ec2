# import the necessary libraries
# - need boto3 for AWS API
# - use JSON to do all JSON processing
# - need datetime for checking current time
# - need pytz to set the time zone accurately
import boto3
import json
from datetime import datetime 
import pytz



#Crete boto3 clients
ec2 = boto3.client('ec2')
# Define ec2 schedular tag values
scheduler_start_key = 'SchedulerStartTime'
scheduler_stop_key = 'SchedulerStopTime'

# define the tag key/value pair to look for
#   Name: SchedulerStartTime
#   Value: 0-23 (any other value is considered invalid)
#   Name: SchedulerStopTime
#   Value: 0-23 (any other value is considered invalid)


# get all ec2 instances with scheduler tags
instances = ec2.instances.filter(Filters=[{'Name': 'tag-key', 'Values': [scheduler_start_key, scheduler_stop_key]}])

# get the current hour in the correct time zone
current_time = datetime.now(pytz.timezone('Your_Timezone_Here')).hour

# main processing:
# process all instances:
#   get a list of instances with start time and stop time tags
#   for each instance:
#       - if it is running
#           - if the current hour == stop time
#               - stop the instance
#       - if it is stopped
#           - if the current hour == start time
#               - start the instance
#       - in all other cases, do nothing
for instance in instances:
    # get start and stop times from tags
    start_time_tag = [tag for tag in instance.tags if tag['Key'] == scheduler_start_key]
    stop_time_tag = [tag for tag in instance.tags if tag['Key'] == scheduler_stop_key]

    if start_time_tag and stop_time_tag:
        start_time = int(start_time_tag[0]['Value'])
        stop_time = int(stop_time_tag[0]['Value'])

        # if the instance is running
        if instance.state['Name'] == 'running':
            # if the current hour == stop time
            if current_time == stop_time:
                # stop the instance
                instance.stop()
        # if the instance is stopped
        elif instance.state['Name'] == 'stopped':
            # if the current hour == start time
            if current_time == start_time:
                # start the instance
                instance.start()
# process all buckets:
#   get a list of all buckets
#   for each bucket:
#       - if bucket starts with the correct prefix
#           - if versioning is not enabled
#               - enable versioning
buckets = client.list_buckets()['Buckets']
bucket_prefix = 'your-prefix'  # Your desired bucket prefix

for bucket in buckets:
    if bucket['Name'].startswith(bucket_prefix):
        # if versioning is not enabled
        versioning_status = client.get_bucket_versioning(Bucket=bucket['Name'])
        
        if 'Status' in versioning_status and versioning_status['Status'] != 'Enabled':
            # enable versioning
            client.put_bucket_versioning(
                Bucket=bucket['Name'],
                VersioningConfiguration={'Status': 'Enabled'}
            )

