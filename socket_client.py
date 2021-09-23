import socket
from getpass import getpass
from sys import exit
from time import sleep


class SocketClient:
    def __init__(self, ip1, port1):
        self.ip1 = ip1
        self.port1 = port1
        self.server1 = (self.ip1, self.port1)
        self.socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket1.connect(self.server1)

    def authentification(self):
        pw = getpass(prompt='パスワードを入力してください\n')
        self.socket1.send(pw.encode("UTF-8"))
        authConfirmation = str(self.socket1.recv(50).decode())
        if 'True' == authConfirmation:
            print('パスワード認証に成功しました')
        else:
            self.socket1.close()
            exit('不正なパスワードです')

    def interaction(self):
        line = ''
        while line != "bye":
            line = input('>>> ')
            self.socket1.send(line.encode("UTF-8"))
            data1 = self.socket1.recv(50000).decode()
            if data1 != 'none':
                [exec("print(ch, end='', flush=True); sleep(0.005)") for ch in data1]
                print('\n')

    def close_connection(self):
        self.socket1.close()
        exit('クライアント側終了です')

if __name__ == "__main__":
    testDrive = SocketClient(input("サーバーのipアドレスを入力してください: "), 50000)
    testDrive.authentification()
    testDrive.interaction()
    testDrive.close_connection()
