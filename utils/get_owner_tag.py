from flask import Flask, request, render_template, jsonify

def get_owner_tag(tag_list, info):
    response = dict()

    for tag in tag_list:
        if tag['Key'] == 'Owner':
            response.update(dict(Info = "{}".format(info)))
            response.update(tag)
            
    return response
