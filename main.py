import asyncio
from pystun3 import stun

class STUNServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print(f"Received {data} from {addr}")
        # Process STUN request
        response = stun.build_binding_response(data, addr)
        if response:
            self.transport.sendto(response, addr)

    def error_received(self, exc):
        print(f"Error received: {exc}")

    def connection_lost(self, exc):
        print("Connection closed")

async def main():
    loop = asyncio.get_running_loop()
    print("Starting STUN server on 0.0.0.0:3478")

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: STUNServerProtocol(),
        local_addr=('0.0.0.0', 3478))

    try:
        await asyncio.sleep(3600)  # Run for 1 hour
    finally:
        transport.close()

if __name__ == "__main__":
    asyncio.run(main())
