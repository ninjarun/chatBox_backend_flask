
# chatBox - backend

chatBox is the backend for handling messages between users.

backend uploaded at render.com at url:
https://chatbox-fb7v.onrender.com

also included:
thunder-collection_chatBox.json
can be imported into the thunder client for tests


Coded by: Yoni Oren
## Installation

```
    please start a virtual enviroment and install the requirments.txt file
    command:
    
    pip install -r requirments.txt
```





## API Reference

#### new message

```http
  POST /newMsg
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `sender` | `string` | name of current user (sender)|
| `receiver` | `string` | name of receiver|
| `message` | `string` |text message  |
| `subject` | `string` |messgae  subject |


#### Get all messages of certin user

```http
  GET /all_msgs/${user}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `user`      | `string` | send user and recieve all messages user appears in as sender or reciever  |


#### Get all unread messages of certin user
```http
  GET /all_unread_msgs/${user}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `user`      | `string` | send user and recieve all unread messages user appears in as sender or reciever  |


####Get all messages of certin user where a cerin word of your choice appears in message
```http
  GET /return_msg/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `user`      | `string` | user varible to search messages |
| `search_phrase`      | `string` | keyword you are searching for|


