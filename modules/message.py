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

    def __init__(self, recipient, sender, message_type, content):
        """
        Initialisiert die Message-Klasse.

        Parameters:
            recipient (str): Der Empfänger der Nachricht.
            sender (str): Der Absender der Nachricht.
            message_type (str): Der Typ der Nachricht.
            content (str): Der Inhalt der Nachricht.
        """
        self.recipient = recipient
        self.sender = sender
        self.message_type = message_type
        self.content = content

    def to_dict(self):
        """
        Wandelt die Nachricht in ein Wörterbuch um.

        Returns:
            dict: Ein Wörterbuch mit den Attributen der Nachricht.
        """
        return {
            "recipient": self.recipient,
            "sender": self.sender,
            "type": self.message_type,
            "content": self.content
        }

    def serialize(self):
        """
        Serialisiert die Nachricht in ein Byte-Format.

        Returns:
            bytes: Die serialisierte Nachricht.
        """
        return pickle.dumps(self.to_dict())

    @staticmethod
    def deserialize(serialized_message):
        """
        Deserialisiert eine Byte-Nachricht zurück in ein Message-Objekt.

        Parameters:
            serialized_message (bytes): Die serialisierte Nachricht.

        Returns:
            Message: Das deserialisierte Message-Objekt.
        """
        data = pickle.loads(serialized_message)
        return Message(data['recipient'], data['sender'], data['type'], data['content'])

#EOF
