# Datei: ./modules/argument_parser.py
  ## Klasse: ArgumentParser
    Docstring: Klasse zur Analyse von Befehlszeilenargumenten für das Skript.

Attributes:
    help (bool): Gibt an, ob die Hilfe angezeigt werden soll.
    edit_filename (str): Der Name der Datei, die bearbeitet werden soll.
    run_mode (bool): Gibt an, ob der Run-Modus aktiviert ist.
    ki (bool): Gibt an, ob der OpenAI-Modus aktiviert ist.
    server_mode (bool): Gibt an, ob der Server-Modus aktiviert ist.
    example_mode (bool): Gibt an, ob der Beispielmodus aktiviert ist.
    client_id (str): Die ID des Clients.
    prompt (str): Der benutzerdefinierte Prompt.
    ### Methode: __init__(self)
      Docstring: Initialisiert die ArgumentParser-Klasse und analysiert die Argumente.
    ### Methode: parse_arguments(self)
      Docstring: Analysiert die Befehlszeilenargumente und setzt die entsprechenden Attribute.
    ### Methode: print_help(self)
      Docstring: Gibt die Hilfenachricht für das Skript aus.

# Datei: ./modules/backup_manager.py
  ## Klasse: BackupManager
    Docstring: Klasse zur Verwaltung von Datei-Backups.

Diese Klasse erstellt Backups von Dateien, indem sie bis zu drei Versionen
der Backup-Datei speichert und sicherstellt, dass die älteste Version überschrieben
wird, wenn eine neue Backup-Datei erstellt wird.

Attributes:
    backup_dir (str): Das Verzeichnis, in dem die Backup-Dateien gespeichert werden.
    ### Methode: __init__(self, backup_dir)
      Docstring: Initialisiert die BackupManager-Klasse.

Parameters:
    backup_dir (str): Das Verzeichnis, in dem die Backup-Dateien gespeichert werden. 
                      Standardmäßig 'bak'.
    ### Methode: manage_backups(self, filename)
      Docstring: Verwalte die Backups für die angegebene Datei.

Diese Methode erstellt Backups der Datei und verschiebt ältere
Backups auf eine höhere Version (z.B. .bak1 wird zu .bak2).

Parameters:
    filename (str): Der Pfad zur Datei, für die das Backup erstellt werden soll.

# Datei: ./modules/beispiel.py
  ## Klasse: ExampleClient
    Docstring: Beispielklasse zum Senden und Empfangen von Nachrichten.

Diese Klasse ermöglicht es, Nachrichten an einen Server zu senden und
empfangene Nachrichten in einem separaten Thread zu verarbeiten.

Attributes:
    client_id (str): Die ID des Clients.
    client (Client): Die Client-Instanz zur Kommunikation mit dem Server.
    running (bool): Gibt an, ob der Client aktiv ist.
    ### Methode: __init__(self, host, port, client_id)
      Docstring: Initialisiert die ExampleClient-Klasse.

Parameters:
    host (str): Der Hostname des Servers.
    port (int): Der Port des Servers.
    client_id (str): Die eindeutige ID des Clients.
    ### Methode: start_receiving(self)
      Docstring: Wartet auf eingehende Nachrichten und verarbeitet diese.
    ### Methode: send_message_input(self)
      Docstring: Ermöglicht dem Benutzer das Senden von Nachrichten an einen Empfänger.
    ### Methode: run(self)
      Docstring: Startet den Empfangsthread und die Eingabeaufforderung zum Senden von Nachrichten.

# Datei: ./modules/client.py
  ## Klasse: Client
    Docstring: Klasse zur Kommunikation mit einem ZMQ-Server.

Diese Klasse verwaltet die Verbindung zu einem Server, registriert den Client
und ermöglicht das Senden und Empfangen von Nachrichten.

Attributes:
    host (str): Der Hostname des Servers.
    port (int): Der Port des Servers.
    client_id (str): Die eindeutige ID des Clients.
    context: Der ZMQ-Kontext.
    server_socket: Socket zum Senden von Nachrichten an den Server.
    unique_port (int): Einzigartiger Port für den Client.
    listener_socket: Socket zum Empfangen von Nachrichten.
    ### Methode: __init__(self, host, port, client_id)
      Docstring: Initialisiert die Client-Klasse.

Parameters:
    host (str): Der Hostname des Servers.
    port (int): Der Port des Servers.
    client_id (str): Die eindeutige ID des Clients.
    ### Methode: generate_unique_port(self)
      Docstring: Generiert einen einzigartigen Port für den Client.

Returns:
    int: Ein verfügbarer Port für den Client.
    ### Methode: is_port_available(self, port)
      Docstring: Überprüft, ob ein gegebener Port verfügbar ist.

Parameters:
    port (int): Der zu überprüfende Port.

Returns:
    bool: True, wenn der Port verfügbar ist, sonst False.
    ### Methode: register(self)
      Docstring: Registriert den Client beim Server.

Sendet eine Registrierungsnachricht an den Server und wartet auf eine Antwort.
    ### Methode: receive_message(self)
      Docstring: Empfängt eine Nachricht vom Listener-Socket.

Returns:
    Message: Das empfangene Message-Objekt.

Raises:
    Exception: Wenn ein Fehler beim Empfangen der Nachricht auftritt.
    ### Methode: send_message(self, recipient, sender, message_type, content)
      Docstring: Sendet eine Nachricht an den Server.

Parameters:
    recipient (str): Der Empfänger der Nachricht.
    sender (str): Der Absender der Nachricht.
    message_type (str): Der Typ der Nachricht.
    content (str): Der Inhalt der Nachricht.

# Datei: ./modules/code_generator.py
  ## Klasse: CodeGenerator
    Docstring: Klasse zur Generierung von Code mithilfe der OpenAI API.

Diese Klasse ermöglicht es, Anfragen an die OpenAI API zu stellen und
generierten Code zurückzugeben.

Attributes:
    api_key (str): Der API-Schlüssel für die OpenAI-Integration.
    organization (str): Die Organisation für die OpenAI-Integration.
    ### Methode: __init__(self, api_key, organization)
      Docstring: Initialisiert die CodeGenerator-Klasse.

Parameters:
    api_key (str): Der API-Schlüssel für die OpenAI-Integration.
    organization (str): Die Organisation für die OpenAI-Integration.
    ### Methode: generiere_code(self, messages, model, temperature, max_tokens, frequency_penalty)
      Docstring: Generiert Code basierend auf den übergebenen Nachrichten.

Parameters:
    messages (list): Eine Liste von Nachrichten, die als Eingabe an das Modell gesendet werden.
    model (str): Das verwendete Modell. Standardmäßig "gpt-4".
    temperature (float): Steuerung der Kreativität der Ausgabe. Standardmäßig 0.2.
    max_tokens (int): Maximale Anzahl der Tokens für die Antwort. Standardmäßig 4096.
    frequency_penalty (float): Bestrafung für die Wiederholung von Tokens. Standardmäßig 0.2.

Returns:
    str: Der generierte Code oder None, wenn ein Fehler auftritt.

# Datei: ./modules/conversation_manager.py
  ## Klasse: ConversationManager
    Docstring: Klasse zur Verwaltung der Konversationshistorie und zur Extraktion von Codeblöcken.

Attributes:
    conversation_history (list): Liste der Nachrichten in der Konversation.
    max_tokens (int): Maximale Anzahl der Tokens, die in der Historie erlaubt sind.
    encoding: Tokenizer für das GPT-4-Modell.
    content_list (list): Liste zum Speichern von Textinhalten und Codeblöcken.
    log_directory (str): Verzeichnis zum Speichern von Logdateien.
    ### Methode: __init__(self, max_tokens)
      Docstring: Initialisiert die ConversationManager-Klasse.

Parameters:
    max_tokens (int): Maximale Anzahl der Tokens für die Konversationshistorie.
    ### Methode: add_message(self, role, content)
      Docstring: Füge eine Nachricht zur Unterhaltung hinzu.

Parameters:
    role (str): Rolle des Senders (z.B. "user", "system").
    content (str): Inhalt der Nachricht.
    ### Methode: trim_history(self)
      Docstring: Kürze die Historie, um die maximale Tokenanzahl zu beachten.
    ### Methode: count_tokens(self, text)
      Docstring: Zähle die Anzahl der Tokens in einem Text.

Parameters:
    text (str): Der Text, dessen Tokens gezählt werden sollen.

Returns:
    int: Die Anzahl der Tokens.
    ### Methode: get_history(self)
      Docstring: Gibt die gesamte Gesprächshistorie zurück.

Returns:
    list: Die Liste der Nachrichten in der Konversation.
    ### Methode: extract_code_blocks(self, text)
      Docstring: Extrahiere Codeblöcke aus dem gegebenen Text.

Parameters:
    text (str): Der Text, aus dem Codeblöcke extrahiert werden sollen.

Returns:
    tuple: Eine Liste von Codeblöcken und der verbleibende Text.
    ### Methode: log_ki_antwort(self, generierter_code)
      Docstring: Logge die Antwort der KI in eine Datei.

Parameters:
    generierter_code (str): Die von der KI generierte Antwort, die geloggt werden soll.
    ### Methode: save_content(self, text, code_blocks)
      Docstring: Speichere den Text und die Codeblöcke.

Parameters:
    text (str): Der Text, der gespeichert werden soll.
    code_blocks (list): Eine Liste von Codeblöcken, die gespeichert werden sollen.
    ### Methode: remove_empty_codeblocks(self, text)
      Docstring: Entferne leere Codeblöcke aus dem Text.

Parameters:
    text (str): Der Text, aus dem leere Codeblöcke entfernt werden sollen.

Returns:
    str: Der bereinigte Text ohne leere Codeblöcke.

# Datei: ./modules/file_manager.py
  ## Klasse: FileManager
    Docstring: Klasse zur Verwaltung von Dateien und Nachrichten.

Diese Klasse ermöglicht das Speichern und Verarbeiten von Code,
das Empfangen von Nachrichten über ZMQ und das Erstellen von Backups.

Attributes:
    backup_manager (BackupManager): Die Instanz zur Verwaltung von Backups.
    file_operations (FileOperations): Die Instanz zur Durchführung von Dateioperationen.
    format_code_util (FormatCode): Die Instanz zur Formatierung von Code.
    terminal (Terminal): Die Instanz zur Verwaltung der Benutzereingabe.
    args: Argumente, die beim Starten des FileManagers übergeben wurden.
    running (bool): Gibt an, ob der FileManager aktiv ist.
    main_filename (str): Der Name der Hauptdatei, die verwaltet wird.
    current_code (str): Der aktuell bearbeitete Code.
    client (Client): Die Instanz zur Kommunikation mit dem Server.
    message_thread (threading.Thread): Der Thread zum Empfangen von Nachrichten.
    ### Methode: __init__(self, args, host, port, main_filename, client_id)
      Docstring: Initialisiert die FileManager-Klasse.

Parameters:
    args: Argumente, die beim Starten des FileManagers übergeben werden.
    host (str): Der Hostname des Servers.
    port (int): Der Port des Servers.
    main_filename (str): Der Name der Hauptdatei, die verwaltet wird.
    client_id (str): Die eindeutige ID des Clients.
    ### Methode: run(self)
      Docstring: Startet den FileManager-Modus und verarbeitet Benutzereingaben.
    ### Methode: receive_messages(self)
      Docstring: Empfängt Nachrichten über den ZMQ-Socket und verarbeitet sie.
    ### Methode: save_received_code(self, code)
      Docstring: Speichert den empfangenen Code nach Formatierung.

Parameters:
    code (str): Der empfangene Code, der gespeichert werden soll.
    ### Methode: signal_handler(self, sig, frame)
      Docstring: Behandelt das Signal zum Beenden des FileManagers.

Parameters:
    sig: Das empfangene Signal.
    frame: Der aktuelle Stack-Frame.

# Datei: ./modules/file_operations.py
  ## Klasse: FileOperations
    Docstring: Klasse zur Durchführung von Dateioperationen.

Diese Klasse ermöglicht das Erstellen, Lesen, Schreiben, Löschen und Verwalten von Dateien und Verzeichnissen,
sowie das Verwalten von Backups.

Attributes:
    backup_manager (BackupManager): Die Instanz zur Verwaltung von Backups.
    ### Methode: __init__(self, backup_manager)
      Docstring: Initialisiert die FileOperations-Klasse.

Parameters:
    backup_manager (BackupManager): Die Instanz zur Verwaltung von Backups.
    ### Methode: ensure_directory(self, filepath)
      Docstring: Stellt sicher, dass das Verzeichnis für den angegebenen Dateipfad existiert.

Parameters:
    filepath (str): Der Pfad zur Datei, für die das Verzeichnis überprüft wird.
    ### Methode: save_file(self, filename, content)
      Docstring: Speichert den angegebenen Inhalt in der Datei.

Parameters:
    filename (str): Der Name der Datei, in die der Inhalt geschrieben werden soll.
    content (str): Der Inhalt, der in die Datei geschrieben werden soll.
    ### Methode: delete_file(self, filename)
      Docstring: Löscht die angegebene Datei.

Parameters:
    filename (str): Der Name der Datei, die gelöscht werden soll.
    ### Methode: create_directory(self, directory)
      Docstring: Erstellt das angegebene Verzeichnis.

Parameters:
    directory (str): Der Name des Verzeichnisses, das erstellt werden soll.
    ### Methode: delete_directory(self, directory)
      Docstring: Löscht das angegebene Verzeichnis und seinen Inhalt.

Parameters:
    directory (str): Der Name des Verzeichnisses, das gelöscht werden soll.
    ### Methode: read_file(self, filename)
      Docstring: Liest den Inhalt der angegebenen Datei.

Parameters:
    filename (str): Der Name der Datei, die gelesen werden soll.

Returns:
    str: Der Inhalt der Datei oder None, wenn ein Fehler auftritt.
    ### Methode: list_directory_files(self, directory)
      Docstring: Listet die Dateien im angegebenen Verzeichnis auf.

Parameters:
    directory (str): Der Pfad zum Verzeichnis, dessen Dateien aufgelistet werden sollen.

Returns:
    list: Eine Liste der Dateien im Verzeichnis oder eine leere Liste, wenn das Verzeichnis nicht existiert.
    ### Methode: list_project_files(self)
      Docstring: Listet die Projektdateien im aktuellen Verzeichnis auf.

Diese Methode sucht im Hauptverzeichnis nach der Datei main.py und
im modules-Verzeichnis nach allen Python-Dateien.

# Datei: ./modules/format_code.py
  ## Klasse: FormatCode
    Docstring: Klasse zur Formatierung von Code und zur Extraktion von Dateinamen.

Diese Klasse verwendet das 'black'-Modul zur Formatierung von Python-Code
und stellt Methoden zur Verfügung, um Dateinamen aus Kommentaren im Code
zu extrahieren.

Attributes:
    None
    ### Methode: format_code(self, code)
      Docstring: Formatiert den gegebenen Code mit dem 'black'-Formatter.

Parameters:
    code (str): Der zu formatierende Python-Code.

Returns:
    str: Der formatierte Code oder der ursprüngliche Code, 
          falls das Formatieren nicht möglich war.
    ### Methode: extract_filename(self, code)
      Docstring: Extrahiert den Dateinamen aus dem gegebenen Code.

Sucht nach einem Kommentar im Format '# Filename: <Dateiname>' oder
'# filename: <Dateiname>' und gibt den Dateinamen zurück.

Parameters:
    code (str): Der Code, aus dem der Dateiname extrahiert werden soll.

Returns:
    str: Der extrahierte Dateiname oder None, wenn kein Dateiname gefunden wurde.

# Datei: ./modules/logger.py
  ## Klasse: Logger
    Docstring: Klasse zur Protokollierung von Ereignissen in einer Anwendung.

Diese Klasse konfiguriert den Logger, um Nachrichten in eine Logdatei zu schreiben
und umgeleitete Standardausgaben zu protokollieren.

Attributes:
    logger (Logger): Die Logger-Instanz.
    ### Methode: __init__(self, log_file)
      Docstring: Initialisiert die Logger-Klasse.

Parameters:
    log_file (str): Der Pfad zur Logdatei. Standardmäßig 'log/app.log'.
    ### Methode: get_logger(self)
      Docstring: Gibt die Logger-Instanz zurück.

Returns:
    Logger: Die Logger-Instanz.
  ## Klasse: StreamToLogger
    Docstring: Hilfsklasse zum Umleiten von Standardausgaben an den Logger.

Attributes:
    logger (Logger): Die Logger-Instanz.
    log_level (int): Der Log-Level für die Umleitung.
    linebuf (str): Buffer für die Zeilen, die geschrieben werden.
    ### Methode: __init__(self, logger, log_level)
      Docstring: Initialisiert die StreamToLogger-Klasse.

Parameters:
    logger (Logger): Die Logger-Instanz.
    log_level (int): Der Log-Level für die Umleitung.
    ### Methode: write(self, buf)
      Docstring: Schreibt den gegebenen Puffer in den Logger.

Parameters:
    buf (str): Der Puffer mit den zu protokollierenden Nachrichten.
    ### Methode: flush(self)
      Docstring: Stellt sicher, dass alle gepufferten Ausgaben geschrieben werden.

# Datei: ./modules/message.py
  ## Klasse: Message
    Docstring: Klasse zur Darstellung einer Nachricht zwischen Clients und Servern.

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
    ### Methode: __init__(self, recipient, sender, message_type, content)
      Docstring: Initialisiert die Message-Klasse.

Parameters:
    recipient (str): Der Empfänger der Nachricht.
    sender (str): Der Absender der Nachricht.
    message_type (str): Der Typ der Nachricht.
    content (str): Der Inhalt der Nachricht.
    ### Methode: to_dict(self)
      Docstring: Wandelt die Nachricht in ein Wörterbuch um.

Returns:
    dict: Ein Wörterbuch mit den Attributen der Nachricht.
    ### Methode: serialize(self)
      Docstring: Serialisiert die Nachricht in ein Byte-Format.

Returns:
    bytes: Die serialisierte Nachricht.
    ### Methode: deserialize(serialized_message)
      Docstring: Deserialisiert eine Byte-Nachricht zurück in ein Message-Objekt.

Parameters:
    serialized_message (bytes): Die serialisierte Nachricht.

Returns:
    Message: Das deserialisierte Message-Objekt.

# Datei: ./modules/openai.py
  ## Klasse: OpenAIIntegration
    Docstring: Klasse zur Integration mit OpenAI, die die Kommunikation mit der OpenAI-API verwaltet
und die Verarbeitung von Benutzeranfragen sowie die Extraktion von Codeblöcken übernimmt.

Attributes:
    api_key (str): Der API-Schlüssel für die OpenAI-Integration.
    organization (str): Die Organisation für die OpenAI-Integration.
    prompt (str): Der Start-Prompt für die Konversation.
    total_tokens (int): Die Gesamtanzahl der bisher verwendeten Tokens.
    client (CodeGenerator): Der CodeGenerator zur Generierung von Code.
    conversation_manager (ConversationManager): Verwaltet die Konversationshistorie.
    encoding: Tokenizer für das GPT-4-Modell.
    running (bool): Gibt an, ob die Instanz aktiv ist.
    receiver_thread (threading.Thread): Thread zum Empfang von Nachrichten.
    ### Methode: __init__(self, args, host, port, api_key, organization, prompt, client_id)
      Docstring: Initialisiert die OpenAIIntegration-Klasse.

Parameters:
    args: Die Argumente, die beim Start der Anwendung übergeben wurden.
    host (str): Der Hostname des Servers.
    port (int): Der Port des Servers.
    api_key (str): Der API-Schlüssel für die OpenAI-Integration.
    organization (str): Die Organisation für die OpenAI-Integration.
    prompt (str): Der Start-Prompt für die Konversation.
    client_id (str): Die eindeutige ID des Clients.
    ### Methode: start_receiving(self)
      Docstring: Wartet auf eingehende Nachrichten über ZMQ und verarbeitet diese.
    ### Methode: process_file_content(self, file_content)
      Docstring: Verarbeitet den empfangenen Datei-Inhalt und generiert eine Antwort von OpenAI.

Parameters:
    file_content (str): Der Inhalt der empfangenen Datei.
    ### Methode: send_code_blocks(self, code_blocks)
      Docstring: Sendet die extrahierten Codeblöcke einzeln an den FileManager.

Parameters:
    code_blocks (list): Eine Liste von Codeblöcken, die gesendet werden sollen.
    ### Methode: run_interactive_mode(self)
      Docstring: Startet den interaktiven Modus zur Verarbeitung von Benutzeranfragen.
    ### Methode: read_multiline_input(self, prompt)
      Docstring: Liest mehrzeilige Benutzereingaben.

Parameters:
    prompt (str): Der Text, der als Eingabeaufforderung angezeigt wird.

Returns:
    str: Der eingegebene mehrzeilige Text.
    ### Methode: count_tokens(self, text)
      Docstring: Zählt die Anzahl der Tokens in einem gegebenen Text.

Parameters:
    text (str): Der Text, dessen Tokens gezählt werden sollen.

Returns:
    int: Die Anzahl der Tokens.

# Datei: ./modules/run.py
  ## Klasse: Run
    Docstring: Klasse zur Ausführung eines Clients, der mit einem Server kommuniziert.

Diese Klasse ermöglicht das Empfangen von Befehlen über einen Client
und deren Ausführung im System.

Attributes:
    server_address (tuple): Die Adresse des Servers (Host, Port).
    running (bool): Status, ob der Client aktiv ist oder nicht.
    client_id (str): Die ID des Clients.
    client (Client): Die Instanz des Clients zur Kommunikation mit dem Server.
    message_thread (threading.Thread): Der Thread zum Empfangen von Nachrichten.
    ### Methode: __init__(self, args, host, port, client_id)
      Docstring: Initialisiert die Run-Klasse und registriert den Client.

Parameters:
    args: Die übergebenen Argumente.
    host (str): Der Hostname des Servers.
    port (int): Der Port, auf dem der Server lauscht.
    client_id (str): Die ID des Clients.
    ### Methode: signal_handler(self, sig, frame)
      Docstring: Behandelt das Signal für Strg+C, um den Client zu beenden.

Parameters:
    sig: Das empfangene Signal.
    frame: Der aktuelle Stack-Frame.
    ### Methode: handle_message(self, message)
      Docstring: Verarbeitet die empfangene Nachricht.

Parameters:
    message (bytes): Die empfangene serialisierte Nachricht.
    ### Methode: receive_messages(self)
      Docstring: Wartet auf eingehende Nachrichten und verarbeitet diese.
    ### Methode: start(self)
      Docstring: Startet den Run-Client und wartet auf Befehle.

# Datei: ./modules/server.py
  ## Klasse: ServerHandler
    Docstring: Klasse zur Verwaltung eines ZMQ-Servers.

Diese Klasse ermöglicht das Empfangen von Nachrichten von Clients,
die Verarbeitung dieser Nachrichten und das Senden von Antworten.

Attributes:
    host (str): Der Hostname des Servers.
    port (int): Der Port, auf dem der Server lauscht.
    context (zmq.Context): Der ZMQ-Kontext.
    socket (zmq.REP): Der ZMQ-Socket, der für den Empfang von Nachrichten verwendet wird.
    clients (dict): Ein Dictionary zur Speicherung der registrierten Clients.
    ### Methode: __init__(self, host, port)
      Docstring: Initialisiert die ServerHandler-Klasse.

Parameters:
    host (str): Der Hostname des Servers.
    port (int): Der Port, auf dem der Server lauscht.
    ### Methode: start_server(self)
      Docstring: Startet den Server und wartet auf eingehende Nachrichten.
    ### Methode: process_message(self, message)
      Docstring: Verarbeitet die empfangene Nachricht und gibt eine Antwort zurück.

Parameters:
    message (Message): Die empfangene Nachricht.

Returns:
    Message: Die Antwortnachricht.
    ### Methode: send_to_client(self, address, message)
      Docstring: Sendet eine Nachricht an den angegebenen Client.

Parameters:
    address (str): Die Adresse des Clients.
    message (Message): Die zu sendende Nachricht.
    ### Methode: signal_handler(self, sig, frame)
      Docstring: Behandelt das Signal zum Beenden des Servers.

Parameters:
    sig: Das empfangene Signal.
    frame: Der aktuelle Stack-Frame.
    ### Methode: shutdown_server(self)
      Docstring: Schließt den Server und gibt Ressourcen frei.

# Datei: ./modules/terminal.py
  ## Klasse: Terminal
    Docstring: Klasse zur Verwaltung der Terminal-Eingaben.

Diese Klasse ermöglicht das Lesen von Benutzereingaben im Terminal
und behandelt spezielle Steuerbefehle wie Strg+C, Strg+D, Strg+F und Strg+L.

Attributes:
    file_operations (FileOperations): Instanz der FileOperations-Klasse.
    old_settings: Alte Terminal-Einstellungen zur Wiederherstellung.
    running (bool): Status, ob das Terminal aktiv ist oder nicht.
    ### Methode: __init__(self, file_operations)
      Docstring: Initialisiert die Terminal-Klasse.

Parameters:
    file_operations (FileOperations): Instanz der FileOperations-Klasse.
    ### Methode: signal_handler(self, sig, frame)
      Docstring: Behandelt das Signal für Strg+C, um das Programm zu beenden.

Parameters:
    sig: Das empfangene Signal.
    frame: Der aktuelle Stack-Frame.
    ### Methode: reset_terminal(self)
      Docstring: Setzt die Terminal-Einstellungen auf die alten Werte zurück.
    ### Methode: read_input(self)
      Docstring: Liest Benutzereingaben im Terminal und verarbeitet Steuerbefehle.

Returns:
    tuple: Ein Tuple, das den eingegebenen Code (oder None) und die Aktion enthält.

