Keine Kommandozeilen gefunden

# Übersicht der gescannten Dateien

- ../codeGenerator/main.py
- ../codeGenerator/README-CR-md.py
- ../codeGenerator/modules/argument_parser.py
- ../codeGenerator/modules/backup_manager.py
- ../codeGenerator/modules/beispiel.py
- ../codeGenerator/modules/client.py
- ../codeGenerator/modules/code_generator.py
- ../codeGenerator/modules/conversation_manager.py
- ../codeGenerator/modules/file_manager.py
- ../codeGenerator/modules/file_operations.py
- ../codeGenerator/modules/format_code.py
- ../codeGenerator/modules/logger.py
- ../codeGenerator/modules/message.py
- ../codeGenerator/modules/openai.py
- ../codeGenerator/modules/run.py
- ../codeGenerator/modules/server.py
- ../codeGenerator/modules/terminal.py

# Dokumentation der Dateien

# Datei: ../codeGenerator/main.py
  ## Funktion: clear_screen()
    Docstring: Clears the terminal screen based on the operating system.

- On Windows, it uses the 'cls' command.
- On Unix-based systems, it uses the 'clear' command.

:return: None
  ## Funktion: load_config(file_path)
    Docstring: Loads configuration settings from a JSON file.

:param file_path: The path to the configuration file (default: 'etc/config.json').
:return: A dictionary containing the configuration data.
  ## Funktion: load_prompts(file_path)
    Docstring: Loads prompts from a text file with a custom format. The text file must follow a specific structure,
with prompts indicated by 'PROMPT:' and corresponding text between 'TEXT:' and 'END:'.

:param file_path: The path to the prompts file (default: 'etc/prompt.txt').
:return: A dictionary mapping prompt names to their corresponding prompt text.
  ## Funktion: load_overview_json(file_path)
    Docstring: Läd die Datei overview.json aus dem Verzeichnis 'doc/overview' und gibt den Inhalt zurück.

Falls die Datei nicht existiert, wird eine Fehlermeldung ausgegeben.

:param file_path: Der Pfad zur overview.json-Datei (standardmäßig im Verzeichnis doc/overview).
:return: Der Inhalt der Datei als Dictionary.
  ## Funktion: main()
    Docstring: Main entry point of the application. This function clears the screen, loads the configuration and prompt files,
parses command-line arguments, and starts the appropriate mode based on the arguments provided.

Supported modes:
- **OpenAI Mode**: Uses OpenAI API for AI-based interaction.
- **Server Mode**: Starts the application in server mode.
- **Run Mode**: Runs a client in a custom mode.
- **File Manager Mode**: Opens the file manager for a given file.
- **Example Mode**: Runs a sample client as an example.

:return: None
  ## Funktion: signal_handler(sig, frame)
    Docstring: Handles system signals, allowing graceful shutdown when the application runs in server mode.

:param sig: The signal received.
:param frame: The current stack frame.
:return: None
# Datei: ../codeGenerator/README-CR-md.py
  Keine Dokumentation
# Datei: ../codeGenerator/modules/argument_parser.py
  ## Klasse: ArgumentParser
    Docstring: Klasse zur Analyse von Befehlszeilenargumenten für das Skript.

Diese Klasse analysiert die Befehlszeilenargumente und setzt die entsprechenden Attribute,
um verschiedene Modi und Parameter des Programms zu steuern.

Attributes:
    help (bool): Gibt an, ob die Hilfe angezeigt werden soll.
    edit_filename (str): Der Name der Datei, die bearbeitet werden soll.
    run_mode (bool): Gibt an, ob der Run-Modus aktiviert ist.
    ki (bool): Gibt an, ob der OpenAI-Modus aktiviert ist.
    server_mode (bool): Gibt an, ob der Server-Modus aktiviert ist.
    example_mode (bool): Gibt an, ob der Beispielmodus aktiviert ist.
    client_id (str): Die ID des Clients, die an den Beispielmodus übergeben wird.
    prompt (str): Der benutzerdefinierte Prompt, der an den KI-Modus übergeben wird.
    ### Methode: __init__(self)
      Docstring: Initialisiert die ArgumentParser-Klasse und analysiert die übergebenen Argumente.

Die Argumente, die verarbeitet werden, umfassen:
- '-h' oder '--help' zur Anzeige der Hilfe
- '-d <filename>' zum Bearbeiten einer Datei
- '-r' zum Starten des Run-Modus
- '-s' zum Starten des Server-Modus
- '-ki -p <prompt>' zum Starten des OpenAI-Modus mit einem Prompt
- '-bsp <client_id>' zum Starten des Beispielmodus mit einer Client-ID
    ### Methode: parse_arguments(self)
      Docstring: Analysiert die Befehlszeilenargumente und setzt die entsprechenden Attribute.

Die Argumente, die erkannt und verarbeitet werden, umfassen:
- '-h' oder '--help' zur Anzeige der Hilfe
- '-d <filename>' zum Bearbeiten einer Datei
- '-r' zum Starten des Run-Modus
- '-s' zum Starten des Server-Modus
- '-ki -p <prompt>' zum Starten des OpenAI-Modus mit einem Prompt
- '-bsp <client_id>' zum Starten des Beispielmodus mit einer Client-ID

:return: None
    ### Methode: print_help(self)
      Docstring: Gibt die Hilfenachricht für das Skript aus.

Diese Methode zeigt eine Übersicht der verfügbaren Befehlszeilenoptionen an,
die der Benutzer verwenden kann.

:return: None
  ## Funktion: __init__(self)
    Docstring: Initialisiert die ArgumentParser-Klasse und analysiert die übergebenen Argumente.

Die Argumente, die verarbeitet werden, umfassen:
- '-h' oder '--help' zur Anzeige der Hilfe
- '-d <filename>' zum Bearbeiten einer Datei
- '-r' zum Starten des Run-Modus
- '-s' zum Starten des Server-Modus
- '-ki -p <prompt>' zum Starten des OpenAI-Modus mit einem Prompt
- '-bsp <client_id>' zum Starten des Beispielmodus mit einer Client-ID
  ## Funktion: parse_arguments(self)
    Docstring: Analysiert die Befehlszeilenargumente und setzt die entsprechenden Attribute.

Die Argumente, die erkannt und verarbeitet werden, umfassen:
- '-h' oder '--help' zur Anzeige der Hilfe
- '-d <filename>' zum Bearbeiten einer Datei
- '-r' zum Starten des Run-Modus
- '-s' zum Starten des Server-Modus
- '-ki -p <prompt>' zum Starten des OpenAI-Modus mit einem Prompt
- '-bsp <client_id>' zum Starten des Beispielmodus mit einer Client-ID

:return: None
  ## Funktion: print_help(self)
    Docstring: Gibt die Hilfenachricht für das Skript aus.

Diese Methode zeigt eine Übersicht der verfügbaren Befehlszeilenoptionen an,
die der Benutzer verwenden kann.

:return: None
# Datei: ../codeGenerator/modules/backup_manager.py
  ## Klasse: BackupManager
    Docstring: Klasse zur Verwaltung von Datei-Backups.

Diese Klasse erstellt und verwaltet Backups von Dateien, wobei bis zu drei Versionen
der Backup-Datei gespeichert werden. Die älteste Backup-Version wird überschrieben,
wenn eine neue Backup-Datei erstellt wird.

Attributes:
    backup_dir (str): Das Verzeichnis, in dem die Backup-Dateien gespeichert werden.
    ### Methode: __init__(self, backup_dir)
      Docstring: Initialisiert die BackupManager-Klasse und erstellt das Backup-Verzeichnis,
falls es noch nicht existiert.

:param backup_dir: Das Verzeichnis, in dem die Backups gespeichert werden sollen.
                   Standardmäßig 'bak'.
    ### Methode: manage_backups(self, filename)
      Docstring: Verwalte die Backups für die angegebene Datei.

Diese Methode verwaltet bis zu drei Backup-Versionen einer Datei. Das älteste Backup
(Backup3) wird gelöscht, Backup2 wird auf Backup3 verschoben, Backup1 auf Backup2,
und die neue Backup-Datei wird als Backup1 erstellt.

:param filename: Der Pfad zur Datei, für die das Backup erstellt werden soll.
:return: None
  ## Funktion: __init__(self, backup_dir)
    Docstring: Initialisiert die BackupManager-Klasse und erstellt das Backup-Verzeichnis,
falls es noch nicht existiert.

:param backup_dir: Das Verzeichnis, in dem die Backups gespeichert werden sollen.
                   Standardmäßig 'bak'.
  ## Funktion: manage_backups(self, filename)
    Docstring: Verwalte die Backups für die angegebene Datei.

Diese Methode verwaltet bis zu drei Backup-Versionen einer Datei. Das älteste Backup
(Backup3) wird gelöscht, Backup2 wird auf Backup3 verschoben, Backup1 auf Backup2,
und die neue Backup-Datei wird als Backup1 erstellt.

:param filename: Der Pfad zur Datei, für die das Backup erstellt werden soll.
:return: None
# Datei: ../codeGenerator/modules/beispiel.py
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

:param host: Der Hostname des Servers.
:param port: Der Port des Servers.
:param client_id: Die eindeutige ID des Clients.
    ### Methode: start_receiving(self)
      Docstring: Wartet auf eingehende Nachrichten und verarbeitet diese.

:return: None
    ### Methode: send_message_input(self)
      Docstring: Ermöglicht dem Benutzer das Senden von Nachrichten an einen Empfänger.

:return: None
    ### Methode: run(self)
      Docstring: Startet den Empfangsthread und die Eingabeaufforderung zum Senden von Nachrichten.

:return: None
  ## Funktion: __init__(self, host, port, client_id)
    Docstring: Initialisiert die ExampleClient-Klasse.

:param host: Der Hostname des Servers.
:param port: Der Port des Servers.
:param client_id: Die eindeutige ID des Clients.
  ## Funktion: start_receiving(self)
    Docstring: Wartet auf eingehende Nachrichten und verarbeitet diese.

:return: None
  ## Funktion: send_message_input(self)
    Docstring: Ermöglicht dem Benutzer das Senden von Nachrichten an einen Empfänger.

:return: None
  ## Funktion: run(self)
    Docstring: Startet den Empfangsthread und die Eingabeaufforderung zum Senden von Nachrichten.

:return: None
# Datei: ../codeGenerator/modules/client.py
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
      Docstring: Initialisiert die Client-Klasse und erstellt die ZMQ-Sockets für die
Kommunikation mit dem Server.

:param host: Der Hostname des Servers.
:param port: Der Port des Servers.
:param client_id: Die eindeutige ID des Clients.
    ### Methode: generate_unique_port(self)
      Docstring: Generiert einen einzigartigen Port für den Client, indem ein verfügbarer Port
im Bereich von 1024 bis 65535 ausgewählt wird.

:return: Ein verfügbarer Port für den Client.
    ### Methode: is_port_available(self, port)
      Docstring: Überprüft, ob ein gegebener Port verfügbar ist.

:param port: Der zu überprüfende Port.
:return: True, wenn der Port verfügbar ist, sonst False.
    ### Methode: register(self)
      Docstring: Registriert den Client beim Server, indem eine Registrierungsnachricht an den Server gesendet wird.
Wartet auf eine Bestätigung vom Server.

:return: None
    ### Methode: receive_message(self)
      Docstring: Empfängt eine Nachricht vom Listener-Socket.

:return: Das empfangene Message-Objekt.
:raises Exception: Wenn ein Fehler beim Empfangen der Nachricht auftritt.
    ### Methode: send_message(self, recipient, sender, message_type, content)
      Docstring: Sendet eine Nachricht an den Server.

:param recipient: Der Empfänger der Nachricht.
:param sender: Der Absender der Nachricht.
:param message_type: Der Typ der Nachricht.
:param content: Der Inhalt der Nachricht.
:return: None
  ## Funktion: __init__(self, host, port, client_id)
    Docstring: Initialisiert die Client-Klasse und erstellt die ZMQ-Sockets für die
Kommunikation mit dem Server.

:param host: Der Hostname des Servers.
:param port: Der Port des Servers.
:param client_id: Die eindeutige ID des Clients.
  ## Funktion: generate_unique_port(self)
    Docstring: Generiert einen einzigartigen Port für den Client, indem ein verfügbarer Port
im Bereich von 1024 bis 65535 ausgewählt wird.

:return: Ein verfügbarer Port für den Client.
  ## Funktion: is_port_available(self, port)
    Docstring: Überprüft, ob ein gegebener Port verfügbar ist.

:param port: Der zu überprüfende Port.
:return: True, wenn der Port verfügbar ist, sonst False.
  ## Funktion: register(self)
    Docstring: Registriert den Client beim Server, indem eine Registrierungsnachricht an den Server gesendet wird.
Wartet auf eine Bestätigung vom Server.

:return: None
  ## Funktion: receive_message(self)
    Docstring: Empfängt eine Nachricht vom Listener-Socket.

:return: Das empfangene Message-Objekt.
:raises Exception: Wenn ein Fehler beim Empfangen der Nachricht auftritt.
  ## Funktion: send_message(self, recipient, sender, message_type, content)
    Docstring: Sendet eine Nachricht an den Server.

:param recipient: Der Empfänger der Nachricht.
:param sender: Der Absender der Nachricht.
:param message_type: Der Typ der Nachricht.
:param content: Der Inhalt der Nachricht.
:return: None
# Datei: ../codeGenerator/modules/code_generator.py
  ## Klasse: CodeGenerator
    Docstring: Klasse zur Generierung von Code mithilfe der OpenAI API.

Diese Klasse ermöglicht es, Anfragen an die OpenAI API zu stellen und
generierten Code zurückzugeben.

Attributes:
    api_key (str): Der API-Schlüssel für die OpenAI-Integration.
    organization (str): Die Organisation für die OpenAI-Integration.
    ### Methode: __init__(self, api_key, organization)
      Docstring: Initialisiert die CodeGenerator-Klasse.

:param api_key: Der API-Schlüssel für die OpenAI-Integration.
:param organization: Die Organisation für die OpenAI-Integration.
    ### Methode: generiere_code(self, messages, model, temperature, max_tokens, frequency_penalty)
      Docstring: Generiert Code basierend auf den übergebenen Nachrichten.

:param messages: Eine Liste von Nachrichten, die als Eingabe an das Modell gesendet werden.
:param model: Das verwendete Modell. Standardmäßig "gpt-4".
:param temperature: Steuerung der Kreativität der Ausgabe. Standardmäßig 0.2.
:param max_tokens: Maximale Anzahl der Tokens für die Antwort. Standardmäßig 4096.
:param frequency_penalty: Bestrafung für die Wiederholung von Tokens. Standardmäßig 0.2.
:return: Der generierte Code oder None, wenn ein Fehler auftritt.
  ## Funktion: __init__(self, api_key, organization)
    Docstring: Initialisiert die CodeGenerator-Klasse.

:param api_key: Der API-Schlüssel für die OpenAI-Integration.
:param organization: Die Organisation für die OpenAI-Integration.
  ## Funktion: generiere_code(self, messages, model, temperature, max_tokens, frequency_penalty)
    Docstring: Generiert Code basierend auf den übergebenen Nachrichten.

:param messages: Eine Liste von Nachrichten, die als Eingabe an das Modell gesendet werden.
:param model: Das verwendete Modell. Standardmäßig "gpt-4".
:param temperature: Steuerung der Kreativität der Ausgabe. Standardmäßig 0.2.
:param max_tokens: Maximale Anzahl der Tokens für die Antwort. Standardmäßig 4096.
:param frequency_penalty: Bestrafung für die Wiederholung von Tokens. Standardmäßig 0.2.
:return: Der generierte Code oder None, wenn ein Fehler auftritt.
# Datei: ../codeGenerator/modules/conversation_manager.py
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

:param max_tokens: Maximale Anzahl der Tokens für die Konversationshistorie.
    ### Methode: add_message(self, role, content)
      Docstring: Füge eine Nachricht zur Unterhaltung hinzu.

:param role: Rolle des Senders (z.B. "user", "system").
:param content: Inhalt der Nachricht.
:return: None
    ### Methode: trim_history(self)
      Docstring: Kürze die Historie, um die maximale Tokenanzahl zu beachten.

:return: None
    ### Methode: count_tokens(self, text)
      Docstring: Zähle die Anzahl der Tokens in einem Text.

:param text: Der Text, dessen Tokens gezählt werden sollen.
:return: Die Anzahl der Tokens.
    ### Methode: get_history(self)
      Docstring: Gibt die gesamte Gesprächshistorie zurück.

:return: Die Liste der Nachrichten in der Konversation.
    ### Methode: extract_code_blocks(self, text)
      Docstring: Extrahiere Codeblöcke aus dem gegebenen Text.

Diese Methode sucht nach Codeblöcken, die mit "#Filename:" beginnen und mit "#EOF" enden.
Zusätzlich entfernt sie Markierungen wie ```python, die eventuell von der KI-Antwort mitgesendet werden.

:param text: Der Text, aus dem Codeblöcke extrahiert werden sollen.
:return: Eine Liste von Codeblöcken und der verbleibende Text.
    ### Methode: log_ki_antwort(self, generierter_code)
      Docstring: Logge die Antwort der KI in eine Datei.

:param generierter_code: Die von der KI generierte Antwort, die geloggt werden soll.
:return: None
    ### Methode: save_content(self, text, code_blocks)
      Docstring: Speichere den Text und die Codeblöcke.

:param text: Der Text, der gespeichert werden soll.
:param code_blocks: Eine Liste von Codeblöcken, die gespeichert werden sollen.
:return: None
    ### Methode: remove_empty_codeblocks(self, text)
      Docstring: Entferne leere Codeblöcke aus dem Text.

:param text: Der Text, aus dem leere Codeblöcke entfernt werden sollen.
:return: Der bereinigte Text ohne leere Codeblöcke.
  ## Funktion: __init__(self, max_tokens)
    Docstring: Initialisiert die ConversationManager-Klasse.

:param max_tokens: Maximale Anzahl der Tokens für die Konversationshistorie.
  ## Funktion: add_message(self, role, content)
    Docstring: Füge eine Nachricht zur Unterhaltung hinzu.

:param role: Rolle des Senders (z.B. "user", "system").
:param content: Inhalt der Nachricht.
:return: None
  ## Funktion: trim_history(self)
    Docstring: Kürze die Historie, um die maximale Tokenanzahl zu beachten.

:return: None
  ## Funktion: count_tokens(self, text)
    Docstring: Zähle die Anzahl der Tokens in einem Text.

:param text: Der Text, dessen Tokens gezählt werden sollen.
:return: Die Anzahl der Tokens.
  ## Funktion: get_history(self)
    Docstring: Gibt die gesamte Gesprächshistorie zurück.

:return: Die Liste der Nachrichten in der Konversation.
  ## Funktion: extract_code_blocks(self, text)
    Docstring: Extrahiere Codeblöcke aus dem gegebenen Text.

Diese Methode sucht nach Codeblöcken, die mit "#Filename:" beginnen und mit "#EOF" enden.
Zusätzlich entfernt sie Markierungen wie ```python, die eventuell von der KI-Antwort mitgesendet werden.

:param text: Der Text, aus dem Codeblöcke extrahiert werden sollen.
:return: Eine Liste von Codeblöcken und der verbleibende Text.
  ## Funktion: log_ki_antwort(self, generierter_code)
    Docstring: Logge die Antwort der KI in eine Datei.

:param generierter_code: Die von der KI generierte Antwort, die geloggt werden soll.
:return: None
  ## Funktion: save_content(self, text, code_blocks)
    Docstring: Speichere den Text und die Codeblöcke.

:param text: Der Text, der gespeichert werden soll.
:param code_blocks: Eine Liste von Codeblöcken, die gespeichert werden sollen.
:return: None
  ## Funktion: remove_empty_codeblocks(self, text)
    Docstring: Entferne leere Codeblöcke aus dem Text.

:param text: Der Text, aus dem leere Codeblöcke entfernt werden sollen.
:return: Der bereinigte Text ohne leere Codeblöcke.
# Datei: ../codeGenerator/modules/file_manager.py
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

:param args: Argumente, die beim Starten des FileManagers übergeben werden.
:param host: Der Hostname des Servers.
:param port: Der Port des Servers.
:param main_filename: Der Name der Hauptdatei, die verwaltet wird.
:param client_id: Die eindeutige ID des Clients.
    ### Methode: run(self)
      Docstring: Startet den FileManager-Modus und verarbeitet Benutzereingaben.

:return: None
    ### Methode: receive_messages(self)
      Docstring: Empfängt Nachrichten über den ZMQ-Socket und verarbeitet sie.

:return: None
    ### Methode: save_received_code(self, code)
      Docstring: Speichert den empfangenen Code nach Formatierung.

:param code: Der empfangene Code, der gespeichert werden soll.
:return: None
    ### Methode: signal_handler(self, sig, frame)
      Docstring: Behandelt das Signal zum Beenden des FileManagers.

:param sig: Das empfangene Signal.
:param frame: Der aktuelle Stack-Frame.
:return: None
  ## Funktion: __init__(self, args, host, port, main_filename, client_id)
    Docstring: Initialisiert die FileManager-Klasse.

:param args: Argumente, die beim Starten des FileManagers übergeben werden.
:param host: Der Hostname des Servers.
:param port: Der Port des Servers.
:param main_filename: Der Name der Hauptdatei, die verwaltet wird.
:param client_id: Die eindeutige ID des Clients.
  ## Funktion: run(self)
    Docstring: Startet den FileManager-Modus und verarbeitet Benutzereingaben.

:return: None
  ## Funktion: receive_messages(self)
    Docstring: Empfängt Nachrichten über den ZMQ-Socket und verarbeitet sie.

:return: None
  ## Funktion: save_received_code(self, code)
    Docstring: Speichert den empfangenen Code nach Formatierung.

:param code: Der empfangene Code, der gespeichert werden soll.
:return: None
  ## Funktion: signal_handler(self, sig, frame)
    Docstring: Behandelt das Signal zum Beenden des FileManagers.

:param sig: Das empfangene Signal.
:param frame: Der aktuelle Stack-Frame.
:return: None
# Datei: ../codeGenerator/modules/file_operations.py
  ## Klasse: FileOperations
    Docstring: Klasse zur Durchführung von Dateioperationen.

Diese Klasse ermöglicht das Erstellen, Lesen, Schreiben, Löschen und Verwalten von Dateien und Verzeichnissen,
sowie das Verwalten von Backups.

Attributes:
    backup_manager (BackupManager): Die Instanz zur Verwaltung von Backups.
    ### Methode: __init__(self, backup_manager)
      Docstring: Initialisiert die FileOperations-Klasse.

:param backup_manager: Die Instanz zur Verwaltung von Backups.
    ### Methode: ensure_directory(self, filepath)
      Docstring: Stellt sicher, dass das Verzeichnis für den angegebenen Dateipfad existiert.

:param filepath: Der Pfad zur Datei, für die das Verzeichnis überprüft wird.
:return: None
    ### Methode: save_file(self, filename, content)
      Docstring: Speichert den angegebenen Inhalt in der Datei.

:param filename: Der Name der Datei, in die der Inhalt geschrieben werden soll.
:param content: Der Inhalt, der in die Datei geschrieben werden soll.
:return: None
    ### Methode: delete_file(self, filename)
      Docstring: Löscht die angegebene Datei.

:param filename: Der Name der Datei, die gelöscht werden soll.
:return: None
    ### Methode: create_directory(self, directory)
      Docstring: Erstellt das angegebene Verzeichnis.

:param directory: Der Name des Verzeichnisses, das erstellt werden soll.
:return: None
    ### Methode: delete_directory(self, directory)
      Docstring: Löscht das angegebene Verzeichnis und seinen Inhalt.

:param directory: Der Name des Verzeichnisses, das gelöscht werden soll.
:return: None
    ### Methode: read_file(self, filename)
      Docstring: Liest den Inhalt der angegebenen Datei.

:param filename: Der Name der Datei, die gelesen werden soll.
:return: Der Inhalt der Datei oder None, wenn ein Fehler auftritt.
    ### Methode: list_directory_files(self, directory)
      Docstring: Listet die Dateien im angegebenen Verzeichnis auf.

:param directory: Der Pfad zum Verzeichnis, dessen Dateien aufgelistet werden sollen.
:return: Eine Liste der Dateien im Verzeichnis oder eine leere Liste, wenn das Verzeichnis nicht existiert.
    ### Methode: list_project_files(self)
      Docstring: Listet die Projektdateien im aktuellen Verzeichnis auf.

Diese Methode sucht im Hauptverzeichnis nach der Datei main.py und
im modules-Verzeichnis nach allen Python-Dateien.

:return: None
  ## Funktion: __init__(self, backup_manager)
    Docstring: Initialisiert die FileOperations-Klasse.

:param backup_manager: Die Instanz zur Verwaltung von Backups.
  ## Funktion: ensure_directory(self, filepath)
    Docstring: Stellt sicher, dass das Verzeichnis für den angegebenen Dateipfad existiert.

:param filepath: Der Pfad zur Datei, für die das Verzeichnis überprüft wird.
:return: None
  ## Funktion: save_file(self, filename, content)
    Docstring: Speichert den angegebenen Inhalt in der Datei.

:param filename: Der Name der Datei, in die der Inhalt geschrieben werden soll.
:param content: Der Inhalt, der in die Datei geschrieben werden soll.
:return: None
  ## Funktion: delete_file(self, filename)
    Docstring: Löscht die angegebene Datei.

:param filename: Der Name der Datei, die gelöscht werden soll.
:return: None
  ## Funktion: create_directory(self, directory)
    Docstring: Erstellt das angegebene Verzeichnis.

:param directory: Der Name des Verzeichnisses, das erstellt werden soll.
:return: None
  ## Funktion: delete_directory(self, directory)
    Docstring: Löscht das angegebene Verzeichnis und seinen Inhalt.

:param directory: Der Name des Verzeichnisses, das gelöscht werden soll.
:return: None
  ## Funktion: read_file(self, filename)
    Docstring: Liest den Inhalt der angegebenen Datei.

:param filename: Der Name der Datei, die gelesen werden soll.
:return: Der Inhalt der Datei oder None, wenn ein Fehler auftritt.
  ## Funktion: list_directory_files(self, directory)
    Docstring: Listet die Dateien im angegebenen Verzeichnis auf.

:param directory: Der Pfad zum Verzeichnis, dessen Dateien aufgelistet werden sollen.
:return: Eine Liste der Dateien im Verzeichnis oder eine leere Liste, wenn das Verzeichnis nicht existiert.
  ## Funktion: list_project_files(self)
    Docstring: Listet die Projektdateien im aktuellen Verzeichnis auf.

Diese Methode sucht im Hauptverzeichnis nach der Datei main.py und
im modules-Verzeichnis nach allen Python-Dateien.

:return: None
# Datei: ../codeGenerator/modules/format_code.py
  ## Klasse: FormatCode
    Docstring: Klasse zur Formatierung von Code und zur Extraktion von Dateinamen.

Diese Klasse verwendet das 'black'-Modul zur Formatierung von Python-Code
und stellt Methoden zur Verfügung, um Dateinamen aus Kommentaren im Code
zu extrahieren.

Attributes:
    None
    ### Methode: format_code(self, code)
      Docstring: Formatiert den gegebenen Code mit dem 'black'-Formatter.

:param code: Der zu formatierende Python-Code.
:return: Der formatierte Code oder der ursprüngliche Code, 
         falls das Formatieren nicht möglich war.
    ### Methode: extract_filename(self, code)
      Docstring: Extrahiert den Dateinamen aus dem gegebenen Code.

Sucht nach einem Kommentar im Format '# Filename: <Dateiname>' oder
'# filename: <Dateiname>' und gibt den Dateinamen zurück.

:param code: Der Code, aus dem der Dateiname extrahiert werden soll.
:return: Der extrahierte Dateiname oder None, wenn kein Dateiname gefunden wurde.
  ## Funktion: format_code(self, code)
    Docstring: Formatiert den gegebenen Code mit dem 'black'-Formatter.

:param code: Der zu formatierende Python-Code.
:return: Der formatierte Code oder der ursprüngliche Code, 
         falls das Formatieren nicht möglich war.
  ## Funktion: extract_filename(self, code)
    Docstring: Extrahiert den Dateinamen aus dem gegebenen Code.

Sucht nach einem Kommentar im Format '# Filename: <Dateiname>' oder
'# filename: <Dateiname>' und gibt den Dateinamen zurück.

:param code: Der Code, aus dem der Dateiname extrahiert werden soll.
:return: Der extrahierte Dateiname oder None, wenn kein Dateiname gefunden wurde.
# Datei: ../codeGenerator/modules/logger.py
  ## Klasse: Logger
    Docstring: Klasse zur Protokollierung von Ereignissen in einer Anwendung.

Diese Klasse konfiguriert den Logger, um Nachrichten in eine Logdatei zu schreiben
und umgeleitete Standardausgaben zu protokollieren.

Attributes:
    logger (Logger): Die Logger-Instanz.
    ### Methode: __init__(self, log_file)
      Docstring: Initialisiert die Logger-Klasse.

:param log_file: Der Pfad zur Logdatei. Standardmäßig 'log/app.log'.
    ### Methode: get_logger(self)
      Docstring: Gibt die Logger-Instanz zurück.

:return: Die Logger-Instanz.
  ## Funktion: __init__(self, log_file)
    Docstring: Initialisiert die Logger-Klasse.

:param log_file: Der Pfad zur Logdatei. Standardmäßig 'log/app.log'.
  ## Klasse: StreamToLogger
    Docstring: Hilfsklasse zum Umleiten von Standardausgaben an den Logger.

Attributes:
    logger (Logger): Die Logger-Instanz.
    log_level (int): Der Log-Level für die Umleitung.
    linebuf (str): Buffer für die Zeilen, die geschrieben werden.
    ### Methode: __init__(self, logger, log_level)
      Docstring: Initialisiert die StreamToLogger-Klasse.

:param logger: Die Logger-Instanz.
:param log_level: Der Log-Level für die Umleitung.
    ### Methode: write(self, buf)
      Docstring: Schreibt den gegebenen Puffer in den Logger.

:param buf: Der Puffer mit den zu protokollierenden Nachrichten.
:return: None
    ### Methode: flush(self)
      Docstring: Stellt sicher, dass alle gepufferten Ausgaben geschrieben werden.

:return: None
  ## Funktion: get_logger(self)
    Docstring: Gibt die Logger-Instanz zurück.

:return: Die Logger-Instanz.
  ## Funktion: __init__(self, logger, log_level)
    Docstring: Initialisiert die StreamToLogger-Klasse.

:param logger: Die Logger-Instanz.
:param log_level: Der Log-Level für die Umleitung.
  ## Funktion: write(self, buf)
    Docstring: Schreibt den gegebenen Puffer in den Logger.

:param buf: Der Puffer mit den zu protokollierenden Nachrichten.
:return: None
  ## Funktion: flush(self)
    Docstring: Stellt sicher, dass alle gepufferten Ausgaben geschrieben werden.

:return: None
# Datei: ../codeGenerator/modules/message.py
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

:param recipient: Der Empfänger der Nachricht.
:param sender: Der Absender der Nachricht.
:param message_type: Der Typ der Nachricht.
:param content: Der Inhalt der Nachricht.
    ### Methode: to_dict(self)
      Docstring: Wandelt die Nachricht in ein Wörterbuch um.

:return: Ein Wörterbuch mit den Attributen der Nachricht.
    ### Methode: serialize(self)
      Docstring: Serialisiert die Nachricht in ein Byte-Format.

:return: Die serialisierte Nachricht.
    ### Methode: deserialize(serialized_message)
      Docstring: Deserialisiert eine Byte-Nachricht zurück in ein Message-Objekt.

:param serialized_message: Die serialisierte Nachricht.
:return: Das deserialisierte Message-Objekt.
  ## Funktion: __init__(self, recipient, sender, message_type, content)
    Docstring: Initialisiert die Message-Klasse.

:param recipient: Der Empfänger der Nachricht.
:param sender: Der Absender der Nachricht.
:param message_type: Der Typ der Nachricht.
:param content: Der Inhalt der Nachricht.
  ## Funktion: to_dict(self)
    Docstring: Wandelt die Nachricht in ein Wörterbuch um.

:return: Ein Wörterbuch mit den Attributen der Nachricht.
  ## Funktion: serialize(self)
    Docstring: Serialisiert die Nachricht in ein Byte-Format.

:return: Die serialisierte Nachricht.
  ## Funktion: deserialize(serialized_message)
    Docstring: Deserialisiert eine Byte-Nachricht zurück in ein Message-Objekt.

:param serialized_message: Die serialisierte Nachricht.
:return: Das deserialisierte Message-Objekt.
# Datei: ../codeGenerator/modules/openai.py
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
    overview_data (dict): Enthält Daten aus der overview.json, falls vorhanden.
    first_prompt_sent (bool): Indikator, ob der erste Prompt bereits an die KI gesendet wurde.
    ### Methode: __init__(self, args, host, port, api_key, organization, prompt, client_id, overview_data)
      Docstring: Initialisiert die OpenAIIntegration-Klasse.

:param args: Die Argumente, die beim Start der Anwendung übergeben wurden.
:param host: Der Hostname des Servers.
:param port: Der Port des Servers.
:param api_key: Der API-Schlüssel für die OpenAI-Integration.
:param organization: Die Organisation für die OpenAI-Integration.
:param prompt: Der Start-Prompt für die Konversation.
:param client_id: Die eindeutige ID des Clients.
:param overview_data: Daten aus der overview.json, falls vorhanden.
    ### Methode: start_receiving(self)
      Docstring: Wartet auf eingehende Nachrichten über ZMQ und verarbeitet diese.

:return: None
    ### Methode: process_file_content(self, file_content)
      Docstring: Verarbeitet den empfangenen Datei-Inhalt und generiert eine Antwort von OpenAI.

:param file_content: Der Inhalt der empfangenen Datei.
:return: None
    ### Methode: _append_overview_to_prompt(self, file_content)
      Docstring: Hängt den Inhalt von overview.json an den ersten Prompt an.

:param file_content: Der ursprüngliche Prompt-Inhalt.
:return: Der erweiterte Prompt-Inhalt mit der overview.json.
    ### Methode: send_code_blocks(self, code_blocks)
      Docstring: Sendet die extrahierten Codeblöcke einzeln an den FileManager.

:param code_blocks: Eine Liste von Codeblöcken, die gesendet werden sollen.
:return: None
    ### Methode: run_interactive_mode(self)
      Docstring: Startet den interaktiven Modus zur Verarbeitung von Benutzeranfragen.

:return: None
    ### Methode: read_multiline_input(self, prompt)
      Docstring: Liest mehrzeilige Benutzereingaben.

:param prompt: Der Text, der als Eingabeaufforderung angezeigt wird.
:return: Der eingegebene mehrzeilige Text.
    ### Methode: count_tokens(self, text)
      Docstring: Zählt die Anzahl der Tokens in einem gegebenen Text.

:param text: Der Text, dessen Tokens gezählt werden sollen.
:return: Die Anzahl der Tokens.
  ## Funktion: __init__(self, args, host, port, api_key, organization, prompt, client_id, overview_data)
    Docstring: Initialisiert die OpenAIIntegration-Klasse.

:param args: Die Argumente, die beim Start der Anwendung übergeben wurden.
:param host: Der Hostname des Servers.
:param port: Der Port des Servers.
:param api_key: Der API-Schlüssel für die OpenAI-Integration.
:param organization: Die Organisation für die OpenAI-Integration.
:param prompt: Der Start-Prompt für die Konversation.
:param client_id: Die eindeutige ID des Clients.
:param overview_data: Daten aus der overview.json, falls vorhanden.
  ## Funktion: start_receiving(self)
    Docstring: Wartet auf eingehende Nachrichten über ZMQ und verarbeitet diese.

:return: None
  ## Funktion: process_file_content(self, file_content)
    Docstring: Verarbeitet den empfangenen Datei-Inhalt und generiert eine Antwort von OpenAI.

:param file_content: Der Inhalt der empfangenen Datei.
:return: None
  ## Funktion: _append_overview_to_prompt(self, file_content)
    Docstring: Hängt den Inhalt von overview.json an den ersten Prompt an.

:param file_content: Der ursprüngliche Prompt-Inhalt.
:return: Der erweiterte Prompt-Inhalt mit der overview.json.
  ## Funktion: send_code_blocks(self, code_blocks)
    Docstring: Sendet die extrahierten Codeblöcke einzeln an den FileManager.

:param code_blocks: Eine Liste von Codeblöcken, die gesendet werden sollen.
:return: None
  ## Funktion: run_interactive_mode(self)
    Docstring: Startet den interaktiven Modus zur Verarbeitung von Benutzeranfragen.

:return: None
  ## Funktion: read_multiline_input(self, prompt)
    Docstring: Liest mehrzeilige Benutzereingaben.

:param prompt: Der Text, der als Eingabeaufforderung angezeigt wird.
:return: Der eingegebene mehrzeilige Text.
  ## Funktion: count_tokens(self, text)
    Docstring: Zählt die Anzahl der Tokens in einem gegebenen Text.

:param text: Der Text, dessen Tokens gezählt werden sollen.
:return: Die Anzahl der Tokens.
# Datei: ../codeGenerator/modules/run.py
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

:param args: Die übergebenen Argumente.
:param host: Der Hostname des Servers.
:param port: Der Port, auf dem der Server lauscht.
:param client_id: Die ID des Clients.
    ### Methode: signal_handler(self, sig, frame)
      Docstring: Behandelt das Signal für Strg+C, um den Client zu beenden.

:param sig: Das empfangene Signal.
:param frame: Der aktuelle Stack-Frame.
:return: None
    ### Methode: handle_message(self, message)
      Docstring: Verarbeitet die empfangene Nachricht.

:param message: Die empfangene serialisierte Nachricht.
:return: None
    ### Methode: receive_messages(self)
      Docstring: Wartet auf eingehende Nachrichten und verarbeitet diese.

:return: None
    ### Methode: start(self)
      Docstring: Startet den Run-Client und wartet auf Befehle.

:return: None
  ## Funktion: __init__(self, args, host, port, client_id)
    Docstring: Initialisiert die Run-Klasse und registriert den Client.

:param args: Die übergebenen Argumente.
:param host: Der Hostname des Servers.
:param port: Der Port, auf dem der Server lauscht.
:param client_id: Die ID des Clients.
  ## Funktion: signal_handler(self, sig, frame)
    Docstring: Behandelt das Signal für Strg+C, um den Client zu beenden.

:param sig: Das empfangene Signal.
:param frame: Der aktuelle Stack-Frame.
:return: None
  ## Funktion: handle_message(self, message)
    Docstring: Verarbeitet die empfangene Nachricht.

:param message: Die empfangene serialisierte Nachricht.
:return: None
  ## Funktion: receive_messages(self)
    Docstring: Wartet auf eingehende Nachrichten und verarbeitet diese.

:return: None
  ## Funktion: start(self)
    Docstring: Startet den Run-Client und wartet auf Befehle.

:return: None
# Datei: ../codeGenerator/modules/server.py
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

:param host: Der Hostname des Servers.
:param port: Der Port, auf dem der Server lauscht.
    ### Methode: start_server(self)
      Docstring: Startet den Server und wartet auf eingehende Nachrichten.

:return: None
    ### Methode: process_message(self, message)
      Docstring: Verarbeitet die empfangene Nachricht und gibt eine Antwort zurück.

:param message: Die empfangene Nachricht.
:return: Die Antwortnachricht.
    ### Methode: send_to_client(self, address, message)
      Docstring: Sendet eine Nachricht an den angegebenen Client.

:param address: Die Adresse des Clients.
:param message: Die zu sendende Nachricht.
:return: None
    ### Methode: signal_handler(self, sig, frame)
      Docstring: Behandelt das Signal zum Beenden des Servers.

:param sig: Das empfangene Signal.
:param frame: Der aktuelle Stack-Frame.
:return: None
    ### Methode: shutdown_server(self)
      Docstring: Schließt den Server und gibt Ressourcen frei.

:return: None
  ## Funktion: __init__(self, host, port)
    Docstring: Initialisiert die ServerHandler-Klasse.

:param host: Der Hostname des Servers.
:param port: Der Port, auf dem der Server lauscht.
  ## Funktion: start_server(self)
    Docstring: Startet den Server und wartet auf eingehende Nachrichten.

:return: None
  ## Funktion: process_message(self, message)
    Docstring: Verarbeitet die empfangene Nachricht und gibt eine Antwort zurück.

:param message: Die empfangene Nachricht.
:return: Die Antwortnachricht.
  ## Funktion: send_to_client(self, address, message)
    Docstring: Sendet eine Nachricht an den angegebenen Client.

:param address: Die Adresse des Clients.
:param message: Die zu sendende Nachricht.
:return: None
  ## Funktion: signal_handler(self, sig, frame)
    Docstring: Behandelt das Signal zum Beenden des Servers.

:param sig: Das empfangene Signal.
:param frame: Der aktuelle Stack-Frame.
:return: None
  ## Funktion: shutdown_server(self)
    Docstring: Schließt den Server und gibt Ressourcen frei.

:return: None
# Datei: ../codeGenerator/modules/terminal.py
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

:param file_operations: Instanz der FileOperations-Klasse.
    ### Methode: signal_handler(self, sig, frame)
      Docstring: Behandelt das Signal für Strg+C, um das Programm zu beenden.

:param sig: Das empfangene Signal.
:param frame: Der aktuelle Stack-Frame.
:return: None
    ### Methode: reset_terminal(self)
      Docstring: Setzt die Terminal-Einstellungen auf die alten Werte zurück.

:return: None
    ### Methode: read_input(self)
      Docstring: Liest Benutzereingaben im Terminal und verarbeitet Steuerbefehle.

:return: Ein Tuple, das den eingegebenen Code (oder None) und die Aktion enthält.
  ## Funktion: __init__(self, file_operations)
    Docstring: Initialisiert die Terminal-Klasse.

:param file_operations: Instanz der FileOperations-Klasse.
  ## Funktion: signal_handler(self, sig, frame)
    Docstring: Behandelt das Signal für Strg+C, um das Programm zu beenden.

:param sig: Das empfangene Signal.
:param frame: Der aktuelle Stack-Frame.
:return: None
  ## Funktion: reset_terminal(self)
    Docstring: Setzt die Terminal-Einstellungen auf die alten Werte zurück.

:return: None
  ## Funktion: read_input(self)
    Docstring: Liest Benutzereingaben im Terminal und verarbeitet Steuerbefehle.

:return: Ein Tuple, das den eingegebenen Code (oder None) und die Aktion enthält.
