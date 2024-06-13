# encoding: utf-8

from ckan.logic.schema import validator_args

# The main purpose of this file is to modify CKAN's user-related schemas,
# replacing the username validators for endpoints where username changes user to
# be allowed.

def user_edit_form_schema(old_user_edit_form_schema):
    @validator_args
    def ckanext_security_user_edit_form_schema(
        ignore_missing,
        old_username_validator,
        unicode_safe,
        user_passwords_match,
        user_password_validator,
    ):
        schema = old_user_edit_form_schema()

        schema['name'] += [old_username_validator]

        return schema

    return ckanext_security_user_edit_form_schema
