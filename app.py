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


#adding variables
@app.route('/instance_ip/<region>/<ip_address>')
def ip_to_ec2(region, ip_address=''):
    client = connect_aws_service(region, 'ec2')

    response = client.describe_instances(
        Filters=[
            {
                'Name': 'ip-address',
                'Values': [ip_address]
            },
        ],
    )

    for instances in response['Reservations']:
        for tag in instances.get('Instances'):
            tag_list = tag['Tags']
    
    return get_owner_tag(tag_list)
  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='80')