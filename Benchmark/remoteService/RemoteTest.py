'''
Created on 26. 8. 2018

@author: Tomáš
'''

from .serviceProxy import ServiceProxy, JSONRPCException

if __name__ == '__main__':
    url = "http://localhost:8100/jsonrpc"
    service = ServiceProxy(url)
    try:
        print(service.foobar(foo='FOO', bar='BaR'))
    except JSONRPCException as e:
        print("JSONRPCException Error:")
        print(e.error)
