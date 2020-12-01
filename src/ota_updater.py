################################################################################
# filename: ota_updater.py
# date: 18. Sept. 2020
# username: winkste
# name: Stephan Wink
# description: This module support the OTA firmware update via github repo.
################################################################################

################################################################################
# Imports
import usocket
import os
import gc
import machine
from time import sleep
import src.trace as T

################################################################################
# Functions

################################################################################
# @brief    downloads, installs and updates to a new version available in github
#           Precondition needed: a wifi connection to the internet
#           When the update have been performed, the controller will be
#           restarted
# @param    github_repo     url to the github repository
# @return   none
################################################################################
def download_and_install_update_if_available(github_repo):
    o = OTAUpdater(github_repo)
    if True == o.check_for_update():
        o.download_latest_released_version()
        o.install_update()

################################################################################
# Classes
class OTAUpdater:

    ############################################################################
    # Member Functions

    ############################################################################
    # @brief    constructor of the OTAUpdater object
    # @param    github_repo    link to github repository
    # @param    module      module name to update???
    # @param    main_dir    main directory, root directory
    # @return   none
    ############################################################################
    def __init__(self, github_repo, module='', main_dir='src'):
        self.http_client = HttpClient()
        self.github_repo = github_repo.rstrip('/').replace('https://github.com', 'https://api.github.com/repos')
        self.main_dir = main_dir
        self.module = module.rstrip('/')

    ############################################################################
    # @brief    Compares the local version of the project with the latest
    #           released
    # version in the github repository.
    # @return   TRUE
    ############################################################################
    def check_for_update(self):
        current_version = self.get_local_version(self.modulepath(self.main_dir))
        latest_version = self.get_latest_released_version()

        T.trace(__name__, T.INFO, 'checking versions... ')
        T.trace(__name__, T.INFO, '\tcurrent local version: ' + current_version)
        T.trace(__name__, T.INFO, '\tlatest released version: ' + latest_version)
        if latest_version > current_version:
            T.trace(__name__, T.INFO, 'new version available...')
            return True
        else:
            return False

    ############################################################################
    # @brief    Returns the version of the current installed firmware
    # @param    directory   directory of the version file
    # @param    version_file_name   file name with the content of actual version
    # @return   none
    ############################################################################
    def get_local_version(self, directory, version_file_name='.version'):
        try:
            version_file_name in os.listdir(directory)
            f = open(directory + '/' + version_file_name)
            version = f.read()
            f.close()
            return version
        except OSError:
            return '0.0'

    ############################################################################
    # @brief    Returns the latest release version of the git repository
    # @param    directory   directory of the version file
    # @return   none
    ############################################################################
    def get_latest_released_version(self):
        latest_release = self.http_client.get(self.github_repo + '/releases/latest')
        version = latest_release.json()['tag_name']
        latest_release.close()
        return version

    ############################################################################
    # @brief    This function downloads and updates if a new version is
    #           available indicated by latest_version
    # @return   none
    ############################################################################
    def download_latest_released_version(self):
        T.trace(__name__, T.INFO, 'Updating...')
        latest_version = self.get_latest_released_version()
        self.rmtree('next')
        os.mkdir(self.modulepath('next'))
        self.download_all_files(self.github_repo + '/contents/' + self.main_dir, latest_version)
        with open(self.modulepath('next/.version'), 'w') as versionfile:
            versionfile.write(latest_version)
            versionfile.close()

    ############################################################################
    # @brief    Install the latest downloaded version of the github repo
    # @return   none
    ############################################################################
    def install_update(self):
        self.rmtree(self.modulepath(self.main_dir))
        os.rename(self.modulepath('next'), self.modulepath(self.main_dir))
        T.trace(__name__, T.INFO, 'rebooting...')
        sleep(1)
        machine.reset()

    ############################################################################
    # @brief    This function removes the existing directory structure
    # @ param   directory structure to delete
    # @return   true if folder was succesful removed, else false
    ############################################################################
    def rmtree(self, directory):
        try:
            for entry in os.ilistdir(directory):
                is_dir = entry[1] == 0x4000
                if is_dir:
                    self.rmtree(directory + '/' + entry[0])

                else:
                    os.remove(directory + '/' + entry[0])
            os.rmdir(directory)
            return True
        except OSError:
            return False

    ############################################################################
    # @brief    downloads all files specified by a version in a root url
    # @param    root_url   root url of file repository
    # @param    version   version to download
    # @return   none
    ############################################################################
    def download_all_files(self, root_url, version):
        file_list = self.http_client.get(root_url + '?ref=refs/tags/' + version)
        for file in file_list.json():
            if file['type'] == 'file':
                download_url = file['download_url']
                download_path = self.modulepath('next/' + file['path'].replace(self.main_dir + '/', ''))
                self.download_file(download_url.replace('refs/tags/', ''), download_path)
            elif file['type'] == 'dir':
                path = self.modulepath('next/' + file['path'].replace(self.main_dir + '/', ''))
                os.mkdir(path)
                self.download_all_files(root_url + '/' + file['name'], version)

        file_list.close()

    ############################################################################
    # @brief    downloads  file specified by a uarl to a dedicated location
    # @param    url   location of file
    # @param    path   destination location of the downloaded file
    # @return   none
    ############################################################################
    def download_file(self, url, path):
        T.trace(__name__, T.INFO, '\tDownloading: ' + path)
        with open(path, 'w') as outfile:
            try:
                response = self.http_client.get(url)
                outfile.write(response.text)
            finally:
                response.close()
                outfile.close()
                gc.collect()

    ############################################################################
    # @brief    returns the absolute module path
    # @param    path   relative path to the module path
    # @return   absolute module path
    ############################################################################
    def modulepath(self, path):
        return self.module + '/' + path if self.module else path

################################################################################
# @brief    This is the Response class
################################################################################
class Response:

    def __init__(self, f):
        self.raw = f
        self.encoding = 'utf-8'
        self._cached = None

    def close(self):
        if self.raw:
            self.raw.close()
            self.raw = None
        self._cached = None

    @property
    def content(self):
        if self._cached is None:
            try:
                self._cached = self.raw.read()
            finally:
                self.raw.close()
                self.raw = None
        return self._cached

    @property
    def text(self):
        return str(self.content, self.encoding)

    def json(self):
        import ujson
        return ujson.loads(self.content)

################################################################################
# @brief    This is the HTTP client class
################################################################################
class HttpClient:

    def request(self, method, url, data=None, json=None, headers={}, stream=None):
        try:
            proto, dummy, host, path = url.split('/', 3)
        except ValueError:
            proto, dummy, host = url.split('/', 2)
            path = ''
        if proto == 'http:':
            port = 80
        elif proto == 'https:':
            import ussl
            port = 443
        else:
            raise ValueError('Unsupported protocol: ' + proto)

        if ':' in host:
            host, port = host.split(':', 1)
            port = int(port)

        ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
        ai = ai[0]

        s = usocket.socket(ai[0], ai[1], ai[2])
        try:
            s.connect(ai[-1])
            if proto == 'https:':
                s = ussl.wrap_socket(s, server_hostname=host)
            s.write(b'%s /%s HTTP/1.0\r\n' % (method, path))
            if not 'Host' in headers:
                s.write(b'Host: %s\r\n' % host)
            # Iterate over keys to avoid tuple alloc
            for k in headers:
                s.write(k)
                s.write(b': ')
                s.write(headers[k])
                s.write(b'\r\n')
            # add user agent
            s.write('User-Agent')
            s.write(b': ')
            s.write('MicroPython OTAUpdater')
            s.write(b'\r\n')
            if json is not None:
                assert data is None
                import ujson
                data = ujson.dumps(json)
                s.write(b'Content-Type: application/json\r\n')
            if data:
                s.write(b'Content-Length: %d\r\n' % len(data))
            s.write(b'\r\n')
            if data:
                s.write(data)

            l = s.readline()
            l = l.split(None, 2)
            status = int(l[1])
            reason = ''
            if len(l) > 2:
                reason = l[2].rstrip()
            while True:
                l = s.readline()
                if not l or l == b'\r\n':
                    break
                if l.startswith(b'Transfer-Encoding:'):
                    if b'chunked' in l:
                        raise ValueError('Unsupported ' + l)
                elif l.startswith(b'Location:') and not 200 <= status <= 299:
                    raise NotImplementedError('Redirects not yet supported')
        except OSError:
            s.close()
            raise

        resp = Response(s)
        resp.status_code = status
        resp.reason = reason
        return resp

    def head(self, url, **kw):
        return self.request('HEAD', url, **kw)

    def get(self, url, **kw):
        return self.request('GET', url, **kw)

    def post(self, url, **kw):
        return self.request('POST', url, **kw)

    def put(self, url, **kw):
        return self.request('PUT', url, **kw)

    def patch(self, url, **kw):
        return self.request('PATCH', url, **kw)

    def delete(self, url, **kw):
        return self.request('DELETE', url, **kw)

################################################################################
# Scripts

T.configure(__name__, T.INFO)
