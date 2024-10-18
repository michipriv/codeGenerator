# Filename: modules/message.py

import pickle

class Message:
    """
    Klasse zur Darstellung einer Nachricht zwischen Clients und Servern.

    Diese Klasse enthält Informationen über den Empfänger, den Absender,
    den Typ der Nachricht und deren Inhalt.

    Attributes:
        REGISTER (str): Nachrichtentyp für die Registrierung.
        SEND (str): Nachrichtentyp für das Senden von Nachrichten.
        RESPONSE (str): Nachrichtentyp für Antworten.
        UNKNOWN (str): Nachrichtentyp für unbekannte Nachrichten.
        recipient (str): Der Empfänger der Nachricht.
        sender (str): Der Absender der Nachricht.
        message_type (str): Der Typ der Nachricht.
        content (str): Der Inhalt der Nachricht.
    """

    REGISTER = "register"
    SEND = "send"
    RESPONSE = "response"
    UNKNOWN = "unknown"

    def __init__(self, recipient: str, sender: str, message_type: str, content: str):
        """
        Initialisiert die Message-Klasse.

        :param recipient: Der Empfänger der Nachricht.
        :param sender: Der Absender der Nachricht.
        :param message_type: Der Typ der Nachricht.
        :param content: Der Inhalt der Nachricht.
        """
        self.recipient = recipient
        self.sender = sender
        self.message_type = message_type
        self.content = content

    def to_dict(self) -> dict:
        """
        Wandelt die Nachricht in ein Wörterbuch um.

        :return: Ein Wörterbuch mit den Attributen der Nachricht.
        """
        return {
            "recipient": self.recipient,
            "sender": self.sender,
            "type": self.message_type,
            "content": self.content
        }

    def serialize(self) -> bytes:
        """
        Serialisiert die Nachricht in ein Byte-Format.

        :return: Die serialisierte Nachricht.
        """
        return pickle.dumps(self.to_dict())

    @staticmethod
    def deserialize(serialized_message: bytes):
        """
        Deserialisiert eine Byte-Nachricht zurück in ein Message-Objekt.

        :param serialized_message: Die serialisierte Nachricht.
        :return: Das deserialisierte Message-Objekt.
        """
        data = pickle.loads(serialized_message)
        return Message(data['recipient'], data['sender'], data['type'], data['content'])

#EOF
