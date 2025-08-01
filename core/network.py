import socket
import threading
import logging
from core.messages import create_profile_message, create_post_message, create_dm_message 
from queue import Queue

UDP_IP = "10.171.53.157"
UDP_PORT = 50999 


message_queue = Queue()

def setup_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT)) 
    logging.debug(f"Socket bound to {UDP_IP}:{UDP_PORT}")
    return sock

def receive_messages(sock):
    while True:
        data, addr = sock.recvfrom(1024) 
        logging.debug(f"Received message from {addr}")  
        message_queue.put((data.decode(), addr))

def process_messages():
    while True:
        message, addr = message_queue.get()  
        logging.debug(f"Processing message from {addr}: {message}")  

        parsed_message = parse_message(message)
        logging.debug(f"Parsed message: {parsed_message}")

        # Handle the PROFILE message
        if parsed_message["TYPE"] == "PROFILE":
            if not logging.getLogger().isEnabledFor(logging.DEBUG):  # Check if verbose is off
                logging.info(f"Profile received: {parsed_message['DISPLAY_NAME']} - {parsed_message['STATUS']}")
            else:
                logging.info(f"Profile received: {parsed_message['DISPLAY_NAME']} - {parsed_message['STATUS']}")
                if "AVATAR_TYPE" in parsed_message:
                    logging.info(f"Avatar type: {parsed_message['AVATAR_TYPE']}")
                    logging.info(f"Avatar data (base64): {parsed_message['AVATAR_DATA'][:20]}...")  # Log first 20 characters of avatar data
        
        # Handle the POST message
        elif parsed_message["TYPE"] == "POST":
        
            if not logging.getLogger().isEnabledFor(logging.DEBUG):  # Check if verbose is off
                logging.info(f"Post received: {parsed_message['USER_ID']} - {parsed_message['CONTENT']}")
            else:
                logging.info(f"Post received: {parsed_message['USER_ID']} - {parsed_message['CONTENT']}")
                logging.info(f"Message ID: {parsed_message['MESSAGE_ID']}")
                logging.info(f"TTL: {parsed_message['TTL']}")
                logging.info(f"Token: {parsed_message['TOKEN']}")

        elif parsed_message["TYPE"] == "DM":
           
            if not logging.getLogger().isEnabledFor(logging.DEBUG):  # Check if verbose is off
                logging.info(f"DM received: {parsed_message['FROM']} -> {parsed_message['TO']} - {parsed_message['CONTENT']}")
            else: 
                logging.info(f"DM received: {parsed_message['FROM']} -> {parsed_message['TO']} - {parsed_message['CONTENT']}")
                logging.info(f"Message ID: {parsed_message['MESSAGE_ID']}")
                logging.info(f"Timestamp: {parsed_message['TIMESTAMP']}")
                logging.info(f"Token: {parsed_message['TOKEN']}")

def start_server():
    sock = setup_socket()
    logging.info("Server is running...")

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
    threading.Thread(target=process_messages, daemon=True).start()

    # Keep the server alive by using a blocking operation or loop
    try:
        while True:
            pass  
    except KeyboardInterrupt:
        logging.info("Server stopped by user.")
        exit(0)

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # --modify-- MESSAGE TYPES
    #profile_message = create_profile_message("andre@192.168.1.8", "Andre", "Exploring LSNP!")
    #post_message = create_post_message(
    #     "andre@192.168.1.8",
    #     "Hello from LSNP!",  
    #    ttl=3600  
    #)
    dm_message = create_dm_message(
        "andre@192.168.1.8",  
        "gwen@192.168.1.12",    
        "Hi Gwen!"             
    )

    # verbose mode
    logging.debug("Creating and sending PROFILE message")
    logging.debug(f"Profile message: {dm_message}")

    # --modify-- MESSAGE SENDING
    send_message(sock, dm_message, (UDP_IP, UDP_PORT))

    # --modify-- 
    logging.info(f"Profile message sent to server: {dm_message}")

def send_message(sock, message, addr):
    sock.sendto(message.encode(), addr)
    logging.debug(f"Sent message: {message} to {addr}")
    print(f"Sent message: {message} to {addr}")

def parse_message(message):
    parsed_message = {}
    lines = message.split("\n")
    for line in lines:
        if line:
            key, value = line.split(": ", 1)
            parsed_message[key] = value
    return parsed_message
