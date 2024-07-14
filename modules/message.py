# Filename: modules/message.py

import pickle

class Message:
    REGISTER = "register"
    SEND = "send"
    RESPONSE = "response"
    UNKNOWN = "unknown"

    def __init__(self, recipient, sender, message_type, content):
        self.recipient = recipient
        self.sender = sender
        self.message_type = message_type
        self.content = content

    def to_dict(self):
        return {
            "recipient": self.recipient,
            "sender": self.sender,
            "type": self.message_type,
            "content": self.content
        }

    def serialize(self):
        return pickle.dumps(self.to_dict())

    @staticmethod
    def deserialize(serialized_message):
        data = pickle.loads(serialized_message)
        return Message(data['recipient'], data['sender'], data['type'], data['content'])

#EOF
