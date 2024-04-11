import asyncio
import os
import json
import datetime

import aiohttp

HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 8080))

URL = f'http://{HOST}:{PORT}/ws'


async def main():
    session = aiohttp.ClientSession()
    async with session.ws_connect(URL) as ws:

        async for msg in ws:
            data_received = msg.data
            # Convert received data to a Python dictionary from JSON format
            data_received = json.loads(data_received.replace("'", '"'))
            # Extract the filename to save from the received data
            filename_to_save = data_received["filename"]
            # Convert the content to bytes for writing to a file
            file_content = bytes(data_received["content"])
            # Write the content to a file with the specified filename
            with open(f"{filename_to_save}", 'wb') as file:
                file.write(file_content)
    await session.close()

start = datetime.datetime.now()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
end = datetime.datetime.now()

print("Time elapsed:", str((end-start).microseconds))