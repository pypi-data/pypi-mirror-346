import codecs
import os
import base64
import urllib
import keyring
import socket

import numpy as np
import scipy.sparse as sparse


class Credentials:
    """A helper class to manage the HTTP/basic credentials
    """
    def __init__(self, username, **kwargs):
        self.username = username
        self._password = kwargs.get('password', None)
        self.service = kwargs.get('service', 'nacl')
        self.realm = kwargs.get('realm', None)

    def __repr__(self):
        l = f'Credentials: realm/user: {self.realm}/{self.username}'
        if self._password is None:
            passwd = keyring.get_password(self.service, self.username)
            if passwd is None:
                l += ' | passwd: unknown'
            else:
                l += ' | passwd: <from-keyring>'
        else:
            l += ' | passwd: ******'
        return l

    @property
    def password(self):
        if self._password is not None:
            return self._password
        if self.service is not None:
            passwd = keyring.get_password(self.service, self.username)
            if not passwd:
                raise ValueError(f'no password in keyring for ({self.service}/{self.username})')
            return passwd


def _download_file(remote_url, target, credentials=None):
    """
    Accepts a URL, downloads the file to a given open file object.

    This is a modified version of sncosmo.utils.download_file that
    downloads to an open file object instead of a cache directory.
    """

    from contextlib import closing
    from urllib.request import urlopen, Request, HTTPBasicAuthHandler
    from urllib.error import URLError, HTTPError
    from astropy.utils.console import ProgressBarOrSpinner
    from sncosmo import conf

    timeout = conf.remote_timeout
    download_block_size = 32768
    try:
        # Pretend to be a web browser (IE 6.0). Some servers that we download
        # from forbid access from programs.
        headers = {'User-Agent': 'Mozilla/5.0',
                   'Accept': ('text/html,application/xhtml+xml,'
                              'application/xml;q=0.9,*/*;q=0.8')}
        req = Request(remote_url, headers=headers)

        if credentials is not None:
            #            creds = base64.base64encode(f'{credentials.username}:{credentials.password}'.encode()).decode()
            #            req.add_header('Authorization', f'Basic {creds}')
            auth_handler = HTTPBasicAuthHandler()
            auth_handler.add_password(credentials.realm,
                                      uri=remote_url,
                                      user=credentials.username,
                                      passwd=credentials.password)
            opener = urllib.request.build_opener(auth_handler)
        else:
            opener = urllib.request.build_opener()

        #  with closing(urlopen(req, timeout=timeout)) as remote:
        with closing(opener.open(req, timeout=timeout)) as remote:

            # get size of remote if available (for use in progress bar)
            info = remote.info()
            size = None
            if 'Content-Length' in info:
                try:
                    size = int(info['Content-Length'])
                except ValueError:
                    pass

            dlmsg = "Downloading {0}".format(remote_url)
            with ProgressBarOrSpinner(size, dlmsg) as p:
                bytes_read = 0
                block = remote.read(download_block_size)
                while block:
                    target.write(block)
                    bytes_read += len(block)
                    p.update(bytes_read)
                    block = remote.read(download_block_size)

    # Append a more informative error message to HTTPErrors, URLErrors.
    except HTTPError as e:
        e.msg = "{}. requested URL: {!r}".format(e.msg, remote_url)
        raise
    except URLError as e:
        append_msg = (hasattr(e, 'reason') and hasattr(e.reason, 'errno') and
                      e.reason.errno == 8)
        if append_msg:
            msg = "{0}. requested URL: {1}".format(e.reason.strerror,
                                                   remote_url)
            e.reason.strerror = msg
            e.reason.args = (e.reason.errno, msg)
        raise e

    # This isn't supposed to happen, but occasionally a socket.timeout gets
    # through.  It's supposed to be caught in `urrlib2` and raised in this
    # way, but for some reason in mysterious circumstances it doesn't. So
    # we'll just re-raise it here instead.
    except socket.timeout as e:
        # add the requested URL to the message (normally just 'timed out')
        e.args = ('requested URL {!r} timed out'.format(remote_url),)
        raise URLError(e)


def download_file(remote_url, local_name, credentials=None):
    """
    Download a remote file to local path, unzipping if the URL ends in '.gz'.

    Parameters
    ----------
    remote_url : str
        The URL of the file to download

    local_name : str
        Absolute path filename of target file.

    Raises
    ------
    URLError
        Whenever there's a problem getting the remote file.
    """

    # ensure target directory exists
    dn = os.path.dirname(local_name)
    if not os.path.exists(dn):
        os.makedirs(dn)

    if remote_url.endswith(".gz"):
        import io
        import gzip

        buf = io.BytesIO()
        _download_file(remote_url, buf, credentials=credentials)
        buf.seek(0)
        f = gzip.GzipFile(fileobj=buf, mode='rb')

        with open(local_name, 'wb') as target:
            target.write(f.read())
        f.close()

    else:
        try:
            with open(local_name, 'wb') as target:
                _download_file(remote_url, target, credentials=credentials)
        except:  # noqa
            # in case of error downloading, remove file.
            if os.path.exists(local_name):
                os.remove(local_name)
            raise


def download_dir(remote_url, dirname, credentials=None):
    """
    Download a remote tar file to a local directory.

    Parameters
    ----------
    remote_url : str
        The URL of the file to download

    dirname : str
        Directory in which to place contents of tarfile. Created if it
        doesn't exist.

    Raises
    ------
    URLError (from urllib2 on PY2, urllib.request on PY3)
        Whenever there's a problem getting the remote file.
    """

    import io
    import tarfile

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    mode = 'r:gz' if remote_url.endswith(".gz") else None

    # download file to buffer
    buf = io.BytesIO()
    _download_file(remote_url, buf, credentials=credentials)
    buf.seek(0)

    # create a tarfile with the buffer and extract
    tf = tarfile.open(fileobj=buf, mode=mode)
    tf.extractall(path=dirname)
    tf.close()
    buf.close()  # buf not closed when tf is closed.


# TODO: should inherit from DataMirror, I guess
class DataMirrorWithCredentials(object):
    """Lazy fetcher for remote data.

    When asked for local absolute path to a file or directory, DataMirror
    checks if the file or directory exists locally and, if so, returns it.

    If it doesn't exist, it first determines where to get it from.
    It first downloads the file ``{remote_root}/redirects.json`` and checks
    it for a redirect from ``{relative_path}`` to a full URL. If no redirect
    exists, it uses ``{remote_root}/{relative_path}`` as the URL.

    It downloads then downloads the URL to ``{rootdir}/{relative_path}``.

    For directories, ``.tar.gz`` is appended to the
    ``{relative_path}`` before the above is done and then the
    directory is unpacked locally.

    Parameters
    ----------
    rootdir : str or callable

        The local root directory, or a callable that returns the local root
        directory given no parameters. (The result of the call is cached.)
        Using a callable allows one to customize the discovery of the root
        directory (e.g., from a config file), and to defer that discovery
        until it is needed.

    remote_root : str
        Root URL of the remote server.
    """

    def __init__(self, rootdir, remote_root, credentials=None):
        if not remote_root.endswith('/'):
            remote_root = remote_root + '/'

        self._checked_rootdir = None
        self._rootdir = rootdir
        self._remote_root = remote_root

        self._redirects = None
        self._credentials = credentials

    def rootdir(self):
        """Return the path to the local data directory, ensuring that it
        exists"""

        if self._checked_rootdir is None:

            # If the supplied value is a string, use it. Otherwise
            # assume it is a callable that returns a string)
            rootdir = (self._rootdir
                       if isinstance(self._rootdir, str)
                       else self._rootdir())

            # Check existance
            if not os.path.isdir(rootdir):
                raise Exception("data directory {!r} not an existing "
                                "directory".format(rootdir))

            # Cache value for future calls
            self._checked_rootdir = rootdir

        return self._checked_rootdir

    def _fetch_redirects(self):
        import json
        # from urllib.request import urlopen
        if self._credentials is not None:
            from urllib.request import HTTPBasicAuthHandler
            auth_handler = HTTPBasicAuthHandler()
            auth_handler.add_password(realm=self._credentials.realm,
                                      uri=self._remote_root,
                                      user=self._credentials.username,
                                      passwd=self._credentials.password)
            opener = urllib.request.build_opener(auth_handler)
        else:
            opener = urllib.request.build_opener()

        # f = urlopen(self._remote_root + "redirects.json")
        f = opener.open(self._remote_root + "redirects.json")
        reader = codecs.getreader("utf-8")
        self._redirects = json.load(reader(f))
        f.close()

    def _get_url(self, remote_relpath):
        if self._redirects is None:
            self._fetch_redirects()

        if remote_relpath in self._redirects:
            return self._redirects[remote_relpath]
        else:
            return self._remote_root + remote_relpath

    def abspath(self, relpath, isdir=False):
        """Return absolute path to file or directory, ensuring that it exists.

        If ``isdir``, look for ``{relpath}.tar.gz`` on the remote server and
        unpackage it.

        Otherwise, just look for ``{relpath}``. If redirect points to a gz, it
        will be uncompressed."""

        abspath = os.path.join(self.rootdir(), relpath)

        if not os.path.exists(abspath):
            if isdir:
                url = self._get_url(relpath + ".tar.gz")

                # Download and unpack a directory.
                download_dir(url, os.path.dirname(abspath), credentials=self._credentials)

                # ensure that tarfile unpacked into the expected directory
                if not os.path.exists(abspath):
                    raise RuntimeError("Tarfile not unpacked into expected "
                                       "subdirectory. Please file an issue.")
            else:
                url = self._get_url(relpath)
                print(relpath, url)
                download_file(url, abspath, credentials=self._credentials)

        return abspath
