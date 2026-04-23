import asyncio
import websockets
import json
from pythonosc import udp_client

# Setup OSC Client (Sending to Pure Data on localhost)
OSC_IP = "127.0.0.1"
OSC_PORT = 8000
client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)

async def handler(websocket):
    print(f"Connected! Forwarding OSC to {OSC_IP}:{OSC_PORT}")
    try:
        async for message in websocket:
            data = json.loads(message)
            
            # Send each objective's distance as a separate OSC message
            # Format: /objective/[ID] [distance]
            for obj in data:
                address = f"/obj/{obj['id']}"
                client.send_message(address, float(obj['dist']))
            
            output = " | ".join([f"{obj['id']}: {obj['dist'].rjust(7)}" for obj in data])        
            print(output)
                
    except websockets.exceptions.ConnectionClosed:
        print("Disconnected.")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())