# -*- coding: utf-8 -*-
def build_json_form(cookiecutter_conf):
    json_form = {'schema': {}}
    for input_name, default_value in cookiecutter_conf.iteritems():
        field_type = len(default_value) > 20 and 'textarea' or 'string'
        json_form['schema'][input_name] = {
            'type': field_type,
            'required': True,
            'title': input_name.replace('_', ' ')
                               .replace('-', ' ')
                               .capitalize(),
            'default': default_value
        }
    return json_form
