import asyncio
import websockets
import json
import datetime

async def receive_file(websocket):
    for i in range(100):
        try:
            # Receive data from the WebSocket connection
            data_received = await websocket.recv()
            # Convert received data to a Python dictionary from JSON format
            data_received = json.loads(data_received.replace("'", '"'))
            # Extract the filename to save from the received data
            filename_to_save = data_received["filename"]
            # Convert the content to bytes for writing to a file
            file_content = bytes(data_received["content"])
            # Write the content to a file with the specified filename
            with open(f"{filename_to_save}", 'wb') as file:
                file.write(file_content)
        except websockets.ConnectionClosedOK:
            break
    
async def client():
    # Establish a WebSocket connection to the specified address
    async with websockets.connect('ws://localhost:8765') as websocket:
        # Call the send_file function to send the specified file
        await receive_file(websocket)

start = datetime.datetime.now()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

loop.run_until_complete(client())
loop.close()

end = datetime.datetime.now()

print("Time elapsed:", str((end-start).microseconds))