# -*- coding: utf-8 -*-
"""TCP/UDP server module"""
# standard library
import logging
import os
import socketserver


class TestSyslogServers:
    """Test Syslog Server."""

    def __init__(self, address: str, log_directory: str) -> None:
        """Initialize Class properties.

        Args:
            address: The address for the server to listen.
            log_directory: The directory to write the log file.
        """
        self.address = address
        self.log_directory = log_directory

        # properties
        self._logger = None

    @property
    def logger(self) -> object:
        """Return logger instance."""
        if self._logger is None:
            logfile: str = os.path.join(self.log_directory, 'syslog_server.log')

            # create logger
            self._logger = logging.getLogger('pytest_testing')
            self._logger.setLevel(logging.DEBUG)
            fh = logging.FileHandler(logfile)
            fh.setLevel(logging.DEBUG)
            self._logger.addHandler(fh)

        return self._logger

    def start_tcp_server(self, port: str) -> object:
        """Start TCP servers.

        Args:
            port: The port for the server to listen.

        Returns:
            TCPServer: The TCP server instance.
        """
        tcp_server = None
        logger = self.logger  # add logger to local scope

        class TCPHandler(socketserver.BaseRequestHandler):
            """TCP Handler"""

            def handle(self):
                while True:
                    data = self.request.recv(1024).strip()
                    for d in data.split(b'\0'):
                        if not d:
                            continue
                        logger.info(d.decode())

        try:
            self.logger.info(f'starting TCP server - server: {self.address}, port: {port}')
            tcp_server = socketserver.TCPServer((self.address, port), TCPHandler)
        except Exception:
            print('Failed to start tcp syslog servers.')
            raise

        return tcp_server

    def start_udp_server(self, port: str) -> object:
        """Start UDP servers.

        Args:
            port: The port for the server to listen.

        Returns:
            UDPServer: The UDP server instance.
        """
        udp_server = None
        logger = self.logger  # add logger to local scope

        class UDPHandler(socketserver.DatagramRequestHandler):
            """UDP Handler"""

            def handle(self):
                """Handle UDP message."""
                data = self.rfile.readline().strip()
                logger.info(data.decode())

        try:
            self.logger.info(f'starting UDP server - server: {self.address}, port: {port}')
            udp_server = socketserver.UDPServer((self.address, port), UDPHandler)
        except Exception:
            print('Failed to start udp syslog servers.')
            raise

        return udp_server
