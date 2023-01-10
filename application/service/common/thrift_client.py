from typing import Tuple
from thrift.protocol import TBinaryProtocol
from thrift.protocol.TMultiplexedProtocol import TMultiplexedProtocol
from thrift.transport import TSocket, TTransport
from application.thrifts.services.user import UserService


class ThriftClientFactory:
    @classmethod
    def createUserServiceClient(self, host, port) -> Tuple[TTransport.TBufferedTransport, UserService.Client]:
        transport = TTransport.TBufferedTransport(TSocket.TSocket(host=host, port=port))
        protocol = TMultiplexedProtocol(protocol=TBinaryProtocol.TBinaryProtocolAccelerated(transport), serviceName="user_service")
        client = UserService.Client(protocol)
        return transport, client
