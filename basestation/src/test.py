#!/usr/bin/env python3
while True :
    ser.write(command.encode())
    print("Sent "+command)
            
    print(ser.read(9).decode())