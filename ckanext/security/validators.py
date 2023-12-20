# encoding: utf-8
import six
import string
import collections

from ckan import authz
from ckan.common import _
from ckan.lib.navl.dictization_functions import Missing, Invalid

MIN_PASSWORD_LENGTH = 10
MIN_LEN_ERROR = (
    'Your password must be {} characters or longer, and consist of at least '
    'three of the following character sets: uppercase characters, lowercase '
    'characters, digits, punctuation & special characters, and not contain '
    'too many repeated characters.'
)

def _too_many_repeated_characters(value):
    """ does the password contain too many repeated characters 

    Returns True if the most frequent character is >= 1/3 of the characters.
    e.g. "password" is false: ct(s)==2 < 8/3
         "aaaaword" is true: ct(a)==4 > 8/3

    :param s: proposed password
    :returns: boolean, True if password is ok by this criteria
    """
    char_counts = collections.Counter(value)
    # note, will fail on empty password, but caller checks MIN_PASSWORD_LENGTH
    return (char_counts.most_common(1)[0][1] >=  (len(value)/3))


def user_password_validator(key, data, errors, context):
    value = data[key]

    if isinstance(value, Missing):
        pass  # Already handeled in core
    elif not isinstance(value, six.string_types):
        raise Invalid(_('Passwords must be strings.'))
    elif value == '':
        pass  # Already handeled in core
    else:
        # NZISM compliant password rules
        rules = [
            any(x.isupper() for x in value),
            any(x.islower() for x in value),
            any(x.isdigit() for x in value),
            any(x in string.punctuation for x in value)
        ]
        if len(value) < MIN_PASSWORD_LENGTH or sum(rules) < 3 \
           or _too_many_repeated_characters(value):
            raise Invalid(_(MIN_LEN_ERROR.format(MIN_PASSWORD_LENGTH)))


def old_username_validator(key, data, errors, context):
    # Completely prevents changing of user names
    old_user = authz._get_user(context.get('user'))
    return old_user.name
