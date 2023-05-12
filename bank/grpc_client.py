import grpc
import bank.my_proto_pb2_grpc

class MyStub:
    def __init__(self, server_address):
        channel = grpc.insecure_channel(server_address)
        self.stub = bankZHAB.my_proto_pb2_grpc.MyServiceStub(channel)

    def my_method(self, request):
        return self.stub.MyMethod(request)