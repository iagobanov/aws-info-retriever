from flask import Flask, request, render_template, jsonify

def get_owner_tag(tag_list):
    response = dict()

    for tag in tag_list:
        if tag['Key'] == 'Owner':
            response.update(tag)
    
    return jsonify(response)