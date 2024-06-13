# encoding: utf-8

import six

from ckan.logic.schema import validator_args

# The main purpose of this file is to modify CKAN's user-related schemas, and
# to replace the default password validators everywhere. We are also replacing
# the username validators for endpoints where username changes user to be
# allowed.

def default_user_schema(old_default_user_schema):
    @validator_args
    def ckanext_security_default_user_schema(
        ignore_missing,
        unicode_safe,
        user_password_not_empty,
        user_password_validator,
    ):
        schema = old_default_user_schema()
        schema['password'] = [
            user_password_validator,
            user_password_not_empty,
            ignore_missing,
            unicode_safe,
        ]

        return schema
    return ckanext_security_default_user_schema

def user_new_form_schema(old_user_new_form_schema):
    @validator_args
    def ckanext_security_user_new_form_schema(
        user_both_passwords_entered,
        user_passwords_match,
        user_password_validator
    ):
        schema = old_user_new_form_schema()

        schema['password1'] = [
            six.text_type,
            user_both_passwords_entered,
            user_password_validator,
            user_passwords_match,
        ]
        return schema

    return ckanext_security_user_new_form_schema

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
        schema['password1'] = [ignore_missing, unicode_safe,
                               user_password_validator,
                               user_passwords_match]

        return schema

    return ckanext_security_user_edit_form_schema

def default_update_user_schema(old_default_update_user_schema):
    @validator_args
    def ckanext_security_default_update_user_schema(
        ignore_missing,
        unicode_safe,
        user_password_validator,
    ):
        schema = old_default_update_user_schema()

        schema['password'] = [user_password_validator,
                              ignore_missing, unicode_safe]

        return schema

    return ckanext_security_default_update_user_schema
