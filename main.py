#%%
# import asyncio
import socketio

sio = socketio.Client(logger=True, engineio_logger=True)

@sio.event
def connect():
    print('connection estabalished')

@sio.event
def connect_error(data):
    print("The connection failed!")

# @sio.on('handshake')
# def on_message(data):
#     print('HandShake', data)
#     # sio.emit('symbolSub', {'symbol': 'EURUSD'})

@sio.event
def message(data):
    print('message received with ', data)
    # await sio.emit('blabla')

@sio.event
def my_message(data):
    print('message received with ', data)
    # await sio.emit('blabla')

@sio.event
def disconect():
    print('disconnected')

def main():
    sio.connect('localhost:3000')
    sio.wait()

if __name__ == '__main__':
    main()

# %%
