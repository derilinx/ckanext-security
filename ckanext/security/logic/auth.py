'''
Action functions, all sysadmin-only
'''
from ckan.plugins import toolkit

def security_throttle_user_reset(context, data_dict):
    return {'success': False}

def security_throttle_address_reset(context, data_dict):
    return {'success': False}

def security_throttle_user_show(context, data_dict):
    return {'success': False}

def security_throttle_address_show(context, data_dict):
    return {'success': False}

def security_reset_totp(context, data_dict):
    return {'success': False}

@toolkit.chained_auth_function
@toolkit.auth_sysadmins_check
def user_list(next, context, data_dict):
    if toolkit.asbool(toolkit.config.get('ckanext.security.user_list_enable', 'true')):
        return next(context, data_dict) 
    return {'success': False}

