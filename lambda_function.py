import json
import xmltodict
import boto3

# boto3 S3 initialization
s3_client = boto3.client("s3")
bucket = "BUCKET-NAME"

def lambda_handler(event, context):
    filename = event['Records'][0]['s3']['object']['key']
    print("Filename", filename)
    boto3.resource('s3').meta.client.download_file(bucket, filename, '/tmp/xml_file.xml')
    #print("Event :", event)
    
    with open('/tmp/xml_file.xml') as xml_file:
	      
	    data_dict = xmltodict.parse(xml_file.read())
	    xml_file.close()
	    
	    # generate the object using json.dumps() 
	    # corresponding to json data
	    
    json_data = json.dumps(data_dict)
    splitstring= (filename.split('/')[-1]).split('.')[0]
    s3_object = 'jsonconverted/' + splitstring + '.json'
    s3_client.put_object(Bucket=bucket, Key=s3_object, Body=json_data)
    print("File", splitstring ,"converted")
