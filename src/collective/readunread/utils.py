# -*- coding: utf-8 -*-

from plone import api
from imio.helpers.content import add_to_annotation
from imio.helpers.content import del_from_annotation
from imio.helpers.content import get_from_annotation

ANNOT_KEY = 'col.ru.users'


def current_userid(default=None):
    """ Return current userid """
    cur_user = api.user.get_current()
    if not cur_user:
        return default
    return cur_user.getId()


def get_ru_status(obj, userid=None):
    """ Return read/unread status for userid on obj """
    if userid is None:
        userid = current_userid()
    if userid and userid in get_from_annotation(ANNOT_KEY, obj=obj, default=[]):
        return 'read'
    else:
        return 'unread'


def set_ru_status(obj, userid=None, status='read'):
    """ Set read status for userid on obj """
    if userid is None:
        userid = current_userid()
    cur_status = get_ru_status(obj, userid=userid)
    if cur_status == status:
        return status
    if status == 'read':
        add_to_annotation(ANNOT_KEY, userid, obj=obj)
    elif status == 'unread':
        del_from_annotation(ANNOT_KEY, userid, obj=obj)
    return status
