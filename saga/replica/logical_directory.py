
__author__    = "Andre Merzky"
__copyright__ = "Copyright 2012-2013, The SAGA Project"
__license__   = "MIT"


import saga.adaptors.base        as sab
import saga.attributes           as sa
from   saga.constants            import SYNC, ASYNC, TASK
from   saga.filesystem.constants import *
import saga.namespace.directory  as nsdir
import saga.session              as ss
import saga.task                 as st
import saga.url                  as surl
import saga.utils.signatures     as sus


# ------------------------------------------------------------------------------
#
class LogicalDirectory (nsdir.Directory, sa.Attributes) :

    # --------------------------------------------------------------------------
    #
    @sus.takes   ('LogicalDirectory', 
                  sus.optional ((surl.Url, basestring)), 
                  sus.optional (int), 
                  sus.optional (ss.Session),
                  sus.optional (sab.Base), 
                  sus.optional (dict), 
                  sus.optional (sus.one_of (SYNC, ASYNC, TASK)))
    @sus.returns (sus.nothing)
    def __init__ (self, url=None, flags=READ, session=None, 
                  _adaptor=None, _adaptor_state={}, _ttype=None) : 
        '''
        __init__(url, flags=READ, session=None)

        Create a new Logical Directory instance.

        url:       saga.Url
        flags:     flags enum
        session:   saga.Session
        ret:       obj
        '''

        # param checks
        url = surl.Url (url)

        self._nsdirec = super  (LogicalDirectory, self)
        self._nsdirec.__init__ (url, flags, session, 
                                _adaptor, _adaptor_state, _ttype=_ttype)


    # --------------------------------------------------------------------------
    #
    @classmethod
    @sus.takes   ('LogicalDirectory', 
                  sus.one_of (surl.Url, basestring), 
                  sus.optional (int), 
                  sus.optional (ss.Session),
                  sus.optional (sus.one_of (SYNC, ASYNC, TASK)))
    @sus.returns (st.Task)
    def create (cls, url, flags=READ, session=None, ttype=None) :
        '''
        url:       saga.Url
        flags:     saga.replica.flags enum
        session:   saga.Session
        ttype:     saga.task.type enum
        ret:       saga.Task
        '''

        _nsdirec = super (LogicalDirectory, cls)
        return _nsdirec.create (url, flags, session, ttype=ttype)


    @sus.takes   ('LogicalDirectory', 
                  sus.one_of (surl.Url, basestring), 
                  sus.optional (sus.one_of (SYNC, ASYNC, TASK)))
    @sus.returns ((bool, st.Task))
    def is_file (self, tgt=None, ttype=None) :
        '''
        is_file(tgt=None)

        tgt:           saga.Url / string
        ttype:          saga.task.type enum
        ret:            bool / saga.Task
        '''
        if    tgt  :  return self._adaptor.is_file      (tgt, ttype=ttype)
        else       :  return self._nsdirec.is_file_self (      ttype=ttype)


    @sus.takes   ('LogicalDirectory', 
                  sus.one_of (surl.Url, basestring), 
                  sus.optional (int),
                  sus.optional (sus.one_of (SYNC, ASYNC, TASK)))
    @sus.returns (('LogicalFile', st.Task))
    def open (self, tgt, flags=READ, ttype=None) :
        '''
        open(tgt, flags=READ)

        tgt:      saga.Url
        flags:    saga.namespace.flags enum
        ttype:    saga.task.type enum
        ret:      saga.namespace.Entry / saga.Task
        '''
        tgt_url = surl.Url (tgt)
        return self._adaptor.open (tgt_url, flags, ttype=ttype)


    @sus.takes   ('LogicalDirectory', 
                  sus.one_of (surl.Url, basestring), 
                  sus.optional (int),
                  sus.optional (sus.one_of (SYNC, ASYNC, TASK)))
    @sus.returns (('LogicalDirectory', st.Task))
    def open_dir (self, tgt, flags=READ, ttype=None) :
        '''
        open_dir(tgt, flags=READ)

        :param tgt:   name/path of the directory to open
        :param flags: directory creation flags

        ttype:    saga.task.type enum
        ret:      saga.namespace.Directory / saga.Task
        
        Open and return a new directoy

           The call opens and returns a directory at the given location.

           Example::

               # create a subdir 'data' in /tmp
               dir = saga.namespace.Directory("sftp://localhost/tmp/")
               data = dir.open_dir ('data/', saga.namespace.Create)
        '''
        tgt_url = surl.Url (tgt)
        return self._adaptor.open_dir (tgt_url, flags, ttype=ttype)


    # ----------------------------------------------------------------
    #
    # replica methods
    #
    # --------------------------------------------------------------------------
    #
    @sus.takes   ('LogicalDirectory', 
                  sus.one_of (surl.Url, basestring),
                  sus.optional (sus.one_of (SYNC, ASYNC, TASK)))
    @sus.returns ((int, st.Task))
    def get_size (self, tgt, ttype=None) :
        '''
        get_size(tgt)

        tgt:     logical file to get size for
        ttype:    saga.task.type enum
        ret:      int / saga.Task
        
        Returns the size of the physical file represented by the given logical file (in bytes)

           Example::

               # get a logical directory handle
               lf = saga.replica.LogicalFile("irods://localhost/tmp/data/")
    
               # print a logical file's size
               print lf.get_size ('data.dat')

        '''
        tgt_url = surl.Url (tgt)
        return self._adaptor.get_size (tgt_url, ttype=ttype)

  
    @sus.takes   ('LogicalDirectory', 
                  sus.optional (basestring),
                  sus.optional (basestring),
                  sus.optional (int),
                  sus.optional (sus.one_of (SYNC, ASYNC, TASK)))
    @sus.returns ((sus.list_of (surl.Url), st.Task))
    def find (self, name_pattern, attr_pattern=None, flags=RECURSIVE, ttype=None) :
        '''
        find(name_pattern, attr_pattern=None, flags=RECURSIVE)

        name_pattern:   string 
        attr_pattern:   string
        flags:          flags enum
        ttype:          saga.task.type enum
        ret:            list [saga.Url] / saga.Task

        '''
        if attr_pattern  :  return self._adaptor.find_replicas (name_pattern, attr_pattern, flags, ttype=ttype)
        else             :  return self._nsdirec.find          (name_pattern,               flags, ttype=ttype)

    
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

