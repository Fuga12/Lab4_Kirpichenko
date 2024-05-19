import socket
import ssl
import base64

# Настройка параметров
mailserver = "smtp.gmail.com"  # Адрес почтового сервера
port = 587  # Порт для соединения

# Создание сокета и TCP-соединение
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mailserver, port))

# Приветствие сервера
recv = clientSocket.recv(1024).decode()
if recv[:3] != '220':
    print('Не удалось получить код 220 от сервера.')
    exit()

# Отправка команды HELO и вывод ответа сервера
heloCommand = "HELO Alice\r\n"
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
if recv1[:3] != '250':
    print('Не удалось получить код 250 от сервера.')
    exit()

# Начало TLS
starttlsCommand = "STARTTLS\r\n"
clientSocket.send(starttlsCommand.encode())
recv2 = clientSocket.recv(1024).decode()
if recv2[:3] != '220':
    print('Не удалось начать TLS сессии.')
    exit()

# Обертывание сокета в SSL
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

# Повторное приветствие сервера после TLS
clientSocket.send(heloCommand.encode())
recv3 = clientSocket.recv(1024).decode()
if recv3[:3] != '250':
    print('Не удалось получить код 250 от сервера после TLS.')
    exit()

# Аутентификация
username = "kcv204@gmail.com"
password = "bxnv ytdn cckl illt"

authCommand = "AUTH LOGIN\r\n"
clientSocket.send(authCommand.encode())
recv4 = clientSocket.recv(1024).decode()
if recv4[:3] != '334':
    print('Не удалось инициировать аутентификацию.')
    exit()

# Отправка закодированного имени пользователя
clientSocket.send(base64.b64encode(username.encode()) + b'\r\n')
recv5 = clientSocket.recv(1024).decode()
if recv5[:3] != '334':
    print('Неверное имя пользователя.')
    exit()

# Отправка закодированного пароля
clientSocket.send(base64.b64encode(password.encode()) + b'\r\n')
recv6 = clientSocket.recv(1024).decode()
if recv6[:3] != '235':
    print('Неверный пароль.')
    exit()

# Отправка команды MAIL FROM
mailFromCommand = f"MAIL FROM: <{username}>\r\n"
clientSocket.send(mailFromCommand.encode())
recv7 = clientSocket.recv(1024).decode()
if recv7[:3] != '250':
    print('Не удалось отправить команду MAIL FROM.')
    exit()

# Отправка команды RCPT TO
recipient = "kcv404@gmail.com"
rcptToCommand = f"RCPT TO: <{recipient}>\r\n"
clientSocket.send(rcptToCommand.encode())
recv8 = clientSocket.recv(1024).decode()
if recv8[:3] != '250':
    print('Не удалось отправить команду RCPT TO.')
    exit()

# Отправка команды DATA
dataCommand = "DATA\r\n"
clientSocket.send(dataCommand.encode())
recv9 = clientSocket.recv(1024).decode()
if recv9[:3] != '354':
    print('Не удалось отправить команду DATA.')
    exit()

# Формирование MIME сообщения
subject = "4 лаба"
body = "Я люблю компьютерные сети!"
image_path = "./test.jpg"

with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

message = f"""Subject: {subject}
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="sep"

--sep
Content-Type: text/plain; charset="utf-8"

{body}

--sep
Content-Type: image/jpeg; name="image.jpg"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="image.jpg"

{encoded_image}
--sep--
"""

# Отправка данных сообщения
clientSocket.send(message.encode())

# Завершение сообщения
clientSocket.send("\r\n.\r\n".encode())
recv10 = clientSocket.recv(1024).decode()
if recv10[:3] != '250':
    print('Ошибка при отправке сообщения.')
    exit()

# Отправка команды QUIT
quitCommand = "QUIT\r\n"
clientSocket.send(quitCommand.encode())
recv11 = clientSocket.recv(1024).decode()

# Закрытие соединения
clientSocket.close()

print('Сообщение отправлено')