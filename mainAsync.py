#%%
import asyncio
import socketio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection estabalished')

@sio.event
async def myMessage(data):
    print('message received with ', data)
    # await sio.emit('blabla')

@sio.event
async def disconect():
    print('disconnected')

async def main():
    await sio.connect('localhost:3000')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())

# %%
