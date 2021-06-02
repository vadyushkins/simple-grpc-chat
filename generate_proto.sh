#!/bin/bash
echo "Generating proto gRPC files..."
python3 -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. chat.proto
echo "Generating proto gRPC files... DONE"
