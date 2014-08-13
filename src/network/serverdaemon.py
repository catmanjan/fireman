# gets called when fireman is started with --remote flag

# acts as a server and waits for clients to send network models

# calls core_api.add_rule() based on the models

# 1. INVESTIGATE HOW YOU ACTUALLY AUTHENTICATE CLIENTS
# 2. FIND A GOOD SSL/SOCKET LIBRARY THAT MAPS TO MODEL

# Thread 1
# have a thread that is constantly waiting for someone to connect
# connectionDetails = SSLSocket.accept()
# spawn thread N (one per client)

# Thread N
# while(alive):
# 	SSLSocket.recv(BUFFER_SIZE) -> data
#	* check if actually model and valid
#	core_api.add_rule() with data (turned into network_model)

# Find a library that does this?:
# 	library.recv() -> python class model