import asyncio
import websockets
import json

filename = "file.xls"
save_as = "recieved.xls"

async def handler(websocket):
    fileCount = int(await websocket.recv())
    print(fileCount)
    for i in range(fileCount):
        print("sending file", str(i + 1))
        with open(filename, 'rb') as file:
            # Read the content of the file as bytes
            file_content = file.read()
            # Create a dictionary with the filename and its content to send
            data_to_send = {"filename": save_as, "content": list(file_content)}
            # Convert the dictionary to a JSON string and send it via the WebSocket
            await websocket.send(json.dumps(data_to_send))    

# Start the WebSocket server
start_server = websockets.serve(handler, 'localhost', 8765)

# Run the event loop until the server is complete
asyncio.get_event_loop().run_until_complete(start_server)

# Run the event loop forever to keep the server running
asyncio.get_event_loop().run_forever()