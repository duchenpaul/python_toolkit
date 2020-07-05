import logging
import os

import paramiko

class SSHConnection(object):
    def __init__(self, host, username, password=None, pkey={'keyPath': None, 'keyPassword': None}, port=22):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._transport = None
        self._sftp = None
        self._client = None
        if pkey:
            self._pkey = paramiko.RSAKey.from_private_key_file(
                pkey.get('keyPath'), password=pkey.get('keyPassword')) if pkey.get('keyPath') else None
        else:
            self._pkey = None
        try:
            self._connect()
        except Exception as e:
            logging.exception('Failed to connect to ssh server {}'.format(self._host))
            raise
        
    def __enter__(self):
        return self

    def __exit__(self, Type, value, traceback):
        '''
        Executed after "with"
        '''
        self.close()

    def _connect(self):
        transport = paramiko.Transport((self._host, self._port))
        transport.connect(username=self._username,
                          password=self._password, pkey=self._pkey)
        self._transport = transport

    def get(self, remoteFile, localFile):
        '''Specify localfile and remotefile'''
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.get(remoteFile, localFile)

    def put(self, localFile, remoteFile):
        '''Specify localfile and remotefile'''
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.put(localFile, remoteFile)

    def exec_command(self, command):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        stdin, stdout, stderr = self._client.exec_command(command)
        data = stdout.read()
        if len(data) > 0:
            # print(data.strip())
            return data
        err = stderr.read()
        if len(err) > 0:
            # print(err.strip())
            return err

    def close(self):
        if self._transport:
            self._transport.close()
        if self._client:
            self._client.close()


if __name__ == '__main__':
    config = {
        'host': 'hostname',
        'username': 'pi',
        'password': 'pass',
        'pkey': {'keyPath': 'id_rsa_3072', 'keyPassword': None},
        'port': 500, 
        }
    with SSHConnection(**config) as ssh:
        output = ssh.exec_command('ls -l')
    print(output)
