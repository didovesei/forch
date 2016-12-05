#!/usr/bin/python

"""Standalone utility functions for Mininet tests."""

import os
import socket


PORTS_SOCKET = '/tmp/faucet-ports-server-socket'
RESERVED_FOR_TESTS_PORTS = (179, 5001, 5002, 9179)


def str_int_dpid(hex_dpid):
    """Return stringed-int DPID, from a stringed-hex DPID."""
    return str(int(hex_dpid, 16))


def find_free_port():
    """Retrieve a free TCP port from test server."""
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(PORTS_SOCKET)
    return int(sock.recv(16))


def serve_ports():
    """Implement a TCP server to dispense free TCP ports."""
    if os.path.exists(PORTS_SOCKET):
        os.unlink(PORTS_SOCKET)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(PORTS_SOCKET)
    sock.listen(1)
    ports_served = set()

    while True:
        connection, _ = sock.accept()
        while True:
            free_socket = socket.socket()
            free_socket.bind(('', 0))
            free_port = free_socket.getsockname()[1]
            free_socket.close()
            if free_port < 1024:
                continue
            if free_port in RESERVED_FOR_TESTS_PORTS:
                continue
            if free_port in ports_served:
                continue
            break
        ports_served.add(free_port)
        connection.sendall('%16.16u' % free_port)
        connection.close()
