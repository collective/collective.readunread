from collective.readunread.myutils import set_readby

def objectCreated(obj, event):
    """ adds creator's userid to readby
    """
    set_readby(obj)

def objectViewed(obj, event):
    """ adds creator's userid to readby
    """
    set_readby(obj,userids=[event.user.getId()])