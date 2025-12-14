from flask import request, Response, jsonify
import dicttoxml
import json


def row_to_dict(row, columns):

    #Convert a database row tuple to a dictionary.

    if row is None:
        return None
    return dict(zip(columns, row))


def rows_to_dict_list(rows, columns):
    #Convert a list of database row tuples to a list of dictionaries.

    return [dict(zip(columns, row)) for row in rows]


def json_response(data, status_code=200):
    #Create a JSON response.
    
    return jsonify(data), status_code


def xml_response(data, status_code=200):

    # Convert data to XML
    xml_data = dicttoxml.dicttoxml(data, custom_root='response', attr_type=False)
    
    # Create response with XML content type
    return Response(xml_data, mimetype='application/xml', status=status_code)


def format_response(data, status_code=200):
    """
    Format response based on the 'format' query parameter.
    Supports both JSON and XML formats.
    """
    # Get format parameter from query string (default to 'json')
    format_type = request.args.get('format', 'json').lower()
    
    if format_type == 'xml':
        return xml_response(data, status_code)
    else:
        # Default to JSON 
        return json_response(data, status_code)
