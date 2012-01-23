from collective.readunread.extender import READBY_FIELDNAME

def get_readby(obj):
    """ return the value of readby field
    """
    return obj.getField(READBY_FIELDNAME).get(obj)

def _set_readby(obj,readby):
    obj.getField(READBY_FIELDNAME).set(obj,readby)

def set_readby(obj, userids=[], reindex=True):
    """ add user ids to readby field.
    if no userid is provided creator's will be used
    """
    readby = list(get_readby(obj))
    if not userids:
        userids = [obj.Creator(),]
    new_readby = tuple(set(readby + userids))
    _set_readby(obj,new_readby)
    if reindex:
        obj.reindexObject(idxs='readBy')

def set_unreadby(obj, userids=[]):
    readby = set(get_readby(obj))
    new_readby = tuple(readby.difference(set(userids)))
    _set_readby(obj,new_readby)

def get_status(obj, userid):
    if userid in get_readby(obj):
        return 'read'
    return 'unread'
