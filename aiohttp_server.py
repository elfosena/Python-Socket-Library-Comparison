import asyncio
import os
import json

import aiohttp.web

HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 8080))
filename = "file.xls"
save_as = "recieved.xls"

async def websocket_handler(request):
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    print('Websocket connection ready')
    
    async for msg in ws:
        file_count = int(msg.data)
        
        for i in range(file_count):
            print("sending file", str(i + 1))
            with open(filename, 'rb') as file:
                    # Read the content of the file as bytes
                    file_content = file.read()
                    # Create a dictionary with the filename and its content to send
                    data_to_send = {"filename": save_as, "content": list(file_content)}
                    # Convert the dictionary to a JSON string and send it via the WebSocket
                    await ws.send_str(json.dumps(data_to_send))
                    
        await ws.close()
        
    print('Websocket connection closed')
    return ws


app = aiohttp.web.Application()
app.router.add_route('GET', '/ws', websocket_handler)
aiohttp.web.run_app(app, host=HOST, port=PORT)

