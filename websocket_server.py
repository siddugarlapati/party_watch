import asyncio
import websockets
import json
import uuid
from datetime import datetime
from typing import Dict, Set, List

class WatchRoomServer:
    def __init__(self):
        self.rooms: Dict[str, Dict] = {}
        self.clients: Dict[str, websockets.WebSocketServerProtocol] = {}
        self.client_rooms: Dict[str, str] = {}  # client_id -> room_code
        
    async def register_client(self, websocket: websockets.WebSocketServerProtocol, room_code: str, user_id: str, username: str):
        """Register a new client connection"""
        client_id = str(uuid.uuid4())
        self.clients[client_id] = websocket
        self.client_rooms[client_id] = room_code
        
        # Initialize room if it doesn't exist
        if room_code not in self.rooms:
            self.rooms[room_code] = {
                'users': [],
                'playback_state': {'playing': False, 'current_time': 0},
                'chat_messages': [],
                'host_id': None
            }
        
        # Add user to room
        user_info = {
            'id': user_id,
            'username': username,
            'client_id': client_id,
            'joined_at': datetime.now().isoformat()
        }
        
        if not self.rooms[room_code]['users']:
            # First user becomes host
            user_info['is_host'] = True
            self.rooms[room_code]['host_id'] = user_id
        else:
            user_info['is_host'] = False
        
        self.rooms[room_code]['users'].append(user_info)
        
        # Notify other users in the room
        await self.broadcast_to_room(room_code, {
            'type': 'user_joined',
            'user': user_info
        }, exclude_client=client_id)
        
        # Send current room state to new user
        await websocket.send(json.dumps({
            'type': 'room_state',
            'room': self.rooms[room_code],
            'your_id': user_id
        }))
        
        return client_id
    
    async def unregister_client(self, client_id: str):
        """Unregister a client connection"""
        if client_id in self.client_rooms:
            room_code = self.client_rooms[client_id]
            
            # Remove user from room
            if room_code in self.rooms:
                self.rooms[room_code]['users'] = [
                    user for user in self.rooms[room_code]['users']
                    if user.get('client_id') != client_id
                ]
                
                # If room is empty, remove it
                if not self.rooms[room_code]['users']:
                    del self.rooms[room_code]
                else:
                    # Notify other users
                    await self.broadcast_to_room(room_code, {
                        'type': 'user_left',
                        'client_id': client_id
                    })
            
            del self.client_rooms[client_id]
        
        if client_id in self.clients:
            del self.clients[client_id]
    
    async def broadcast_to_room(self, room_code: str, message: dict, exclude_client: str = None):
        """Broadcast message to all clients in a room"""
        if room_code not in self.rooms:
            return
        
        message_json = json.dumps(message)
        for user in self.rooms[room_code]['users']:
            client_id = user.get('client_id')
            if client_id and client_id != exclude_client and client_id in self.clients:
                try:
                    await self.clients[client_id].send(message_json)
                except websockets.exceptions.ConnectionClosed:
                    # Remove disconnected client
                    await self.unregister_client(client_id)
    
    async def handle_message(self, websocket: websockets.WebSocketServerProtocol, client_id: str, message: dict):
        """Handle incoming messages from clients"""
        room_code = self.client_rooms.get(client_id)
        if not room_code or room_code not in self.rooms:
            return
        
        msg_type = message.get('type')
        
        if msg_type == 'playback_update':
            # Update playback state
            self.rooms[room_code]['playback_state'] = message.get('playback_state', {})
            
            # Broadcast to other users
            await self.broadcast_to_room(room_code, {
                'type': 'playback_update',
                'playback_state': self.rooms[room_code]['playback_state']
            }, exclude_client=client_id)
        
        elif msg_type == 'chat_message':
            # Add chat message
            chat_msg = {
                'id': str(uuid.uuid4()),
                'user_id': message.get('user_id'),
                'username': message.get('username'),
                'message': message.get('message'),
                'timestamp': datetime.now().isoformat()
            }
            
            self.rooms[room_code]['chat_messages'].append(chat_msg)
            
            # Keep only last 100 messages
            if len(self.rooms[room_code]['chat_messages']) > 100:
                self.rooms[room_code]['chat_messages'] = self.rooms[room_code]['chat_messages'][-100:]
            
            # Broadcast to all users in room
            await self.broadcast_to_room(room_code, {
                'type': 'chat_message',
                'message': chat_msg
            })
        
        elif msg_type == 'user_action':
            # Handle user actions (like seeking, play/pause)
            await self.broadcast_to_room(room_code, {
                'type': 'user_action',
                'action': message.get('action'),
                'data': message.get('data'),
                'user_id': message.get('user_id')
            }, exclude_client=client_id)
    
    async def handle_client(self, websocket: websockets.WebSocketServerProtocol, path: str):
        """Handle individual client connections"""
        client_id = None
        try:
            # Wait for initial connection message
            initial_message = await websocket.recv()
            data = json.loads(initial_message)
            
            room_code = data.get('room_code')
            user_id = data.get('user_id')
            username = data.get('username')
            
            if not all([room_code, user_id, username]):
                await websocket.close(1008, "Missing required connection parameters")
                return
            
            # Register client
            client_id = await self.register_client(websocket, room_code, user_id, username)
            
            # Handle incoming messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_message(websocket, client_id, data)
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    print(f"Error handling message: {e}")
                    continue
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"Error in client handler: {e}")
        finally:
            if client_id:
                await self.unregister_client(client_id)

async def main():
    """Start the WebSocket server"""
    server = WatchRoomServer()
    
    print("Starting PartyWatch WebSocket server on ws://localhost:8765")
    
    async with websockets.serve(server.handle_client, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main()) 