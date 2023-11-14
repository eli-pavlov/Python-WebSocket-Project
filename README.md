<div align='center'>

<h1>Websockets and Sqlite simple app</h1>
<p>An application used to get status reports from remote appliances or sensors, using websocket and sqlite.</p>

<h4> <span> · </span> <a href="https://github.com/eli-pavlov/Python-WebSocket-Project/blob/master/README.md"> Documentation </a> <span> · </span> <a href="https://github.com/eli-pavlov/Python-WebSocket-Project/issues"> Report Bug </a> <span> · </span> <a href="https://github.com/eli-pavlov/Python-WebSocket-Project/issues"> Request Feature </a> </h4>


</div>

## :star2: About the Project
This project is a multi-client status report application, built using websockets for TCP communications and Sqlite as lightweigt database for status storage.
"Select" module was used to enable multiple simultaneous connections without each connection blocking each other. Each client sends its status stored by sensors
in status.txt to the server. The server stores the status in 'data.sqlite' database in the project directory.
- For real life usage file size limit mechanism should be added.

To execute:
1. Run server.py
2. Run client.py
3. Optionally add as many clients as needed, client2 and client3 were added for convenience.

It is possible to simulate real-time status changes of each client, by editing the corresponding status.txt file.
