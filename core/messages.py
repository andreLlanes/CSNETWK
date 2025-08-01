import random
import time

def parse_message(message):
    parsed_message = {}
    lines = message.split("\n")
    for line in lines:
        if line:
            key, value = line.split(": ", 1)
            parsed_message[key] = value
    return parsed_message

def create_profile_message(user_id, display_name, status, avatar_type=None, avatar_encoding="base64", avatar_data=None):
  
    profile_message = f"TYPE: PROFILE\nUSER_ID: {user_id}\nDISPLAY_NAME: {display_name}\nSTATUS: {status}"
    
    # Add avatar fields if provided
    if avatar_type and avatar_data:
        profile_message += f"\nAVATAR_TYPE: {avatar_type}\nAVATAR_ENCODING: {avatar_encoding}\nAVATAR_DATA: {avatar_data}"

    return profile_message


def create_post_message(user_id, content, ttl=3600):
    message_id = hex(random.getrandbits(64))[2:]
    timestamp = int(time.time())

    token = f"{user_id}|{timestamp + ttl}|broadcast"
    post_message = f"TYPE: POST\nUSER_ID: {user_id}\nCONTENT: {content}\nTTL: {ttl}\nMESSAGE_ID: {message_id}\nTOKEN: {token}"
    return post_message

def create_dm_message(from_user, to_user, content):
    message_id = hex(random.getrandbits(64))[2:]
    timestamp = int(time.time())
    ttl = 3600  
    token = f"{from_user}|{timestamp + ttl}|chat"

    dm_message = f"TYPE: DM\nFROM: {from_user}\nTO: {to_user}\nCONTENT: {content}\nTIMESTAMP: {timestamp}\nMESSAGE_ID: {message_id}\nTOKEN: {token}"

    return dm_message