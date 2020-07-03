from utils.connection import connect_aws_service
from utils.get_owner_tag import get_owner_tag
from flask import Flask, request, render_template, jsonify


app = Flask(__name__)


#Maing page
@app.route('/', methods=['GET', 'POST'])
def mainpage():
    return 'Not today nibs, not today'


#Healthcheck
@app.route('/health', methods=['GET'])
def health():
    response = {"Status":"Ok"}
    return jsonify(response)


########### EC2 Tasks ###########
# Get tags Based on Filter Applied
# Example Filters (instance-id, ip-address)
@app.route('/ec2/<ec2_filter>/', methods=['GET', 'POST'])
def ec2_info(region='us-east-1', instance_id='', ec2_filter=''):

    aws_info = list()
    data = request.json

    client = connect_aws_service(region, 'ec2')

    for info in data:
        response = client.describe_instances(
            Filters=[
                {
                    'Name': ec2_filter,
                    'Values': [
                        info
                    ]
                },
            ],
        )

        for instances in response['Reservations']:
            for tag in instances.get('Instances'):
                tag_list = tag['Tags']
        
                aws_info.append(get_owner_tag(tag_list, info))

    return jsonify(aws_info)            


########### RDS Tasks ###########
# Get tags Based on Filter Applied
# Example Filters (db-instance-id, db-cluster-id)
@app.route('/rds/<rds_filter>/', methods=['GET', 'POST'])
def rds_info(region='us-east-1', instance_id='', rds_filter=''):

    aws_info = list()
    data = request.json

    client = connect_aws_service(region, 'rds')

    for info in data:
        response = client.describe_db_instances(
            Filters=[
                {
                    'Name': rds_filter,
                    'Values': [
                        info
                    ]
                },
            ],
        )

        for instances in response['DBInstances']:
            arn = instances.get('DBInstanceArn')
            tag_list = client.list_tags_for_resource(ResourceName=arn).get('TagList')

            aws_info.append(get_owner_tag(tag_list, info))

    return jsonify(aws_info)            


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')
