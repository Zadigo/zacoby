import socket

def test_socket_connection(host, port):
    """
    Check whether a socket is still open for
    connection using a given host and port
    """
    s = None
    state = False
    try:
        s = socket.create_connection((host, port), 1)
        state = True
    except socket.error:
        state = False
    else:
        if s:
            s.close()
    return state

def get_available_ip(host, port:int = None):
    """
    Given a host name, get an IP

    Returns
    -------

        - str: IP address 
    """
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return None
    
    ip_address = None
    can_connect = True

    for family, _, _, _, socket_address in infos:
        if port:
            can_connect = test_socket_connection(socket_address[0], port)

        if can_connect and family == socket.AF_INET:
            return socket_address[0]

        if can_connect and not ip_address and family == socket.AF_INET6:
            return socket_address[0]

    return ip_address

def join_host_and_port(host, port):
    if (':' in host and not 
            host.startswith('[')):
        return f'[{host}]:{port}'
    return f'{host}:{port}'
