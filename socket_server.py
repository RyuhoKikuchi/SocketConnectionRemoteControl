import socket
from os import chdir, system
from subprocess import PIPE, run
from sys import exit
from time import sleep
from traceback import format_exc


class SocketServer:
    def __init__(self, host1, port1):
        self.host1 = host1
        self.port1 = port1
        print(f'サーバ情報: {self.host1, self.port1}')


    def authentification(self):
        print('クライエントからのパスワード認証待機')
        with open('pass.txt') as psf:
            self.recvline = self.connection.recv(50).decode()
            self.password = psf.readline()
            if self.password == str(self.recvline):
                self.connection.send('True'.encode('utf-8'))
                print('パスワード認証に成功しました')
            else:
                self.connection.send('False'.encode('utf-8'))
                [closing.close() for closing in [self.connection, self.socket1]]
                exit('不正なパスワードです')


    def close_connection(self):
        [closing.close() for closing in [self.connection, self.socket1]]
        exit('サーバー側終了です')


    def establish_connection(self):
        while True:
            try:
                self.socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket1.bind((self.host1, self.port1))
                self.socket1.listen(1)
                print('クライアントからの入力待ち状態')
                self.connection, self.address = self.socket1.accept()
                print(f'接続したクライアント情報: {self.address}')
                break
            except OSError:
                sleep(1)


    def interaction(self):
        recvline = ''
        sendline = ''
        while True:
            proc_opt = True
            recvline = self.connection.recv(50000).decode('utf-8')
            print('\n')
            print('>>> ', end='')
            [exec("print(ch, end='', flush=True); sleep(0.02)") for ch in recvline]
            print('\n')
            try:
                if recvline == '':
                    pass
                elif recvline == "bye":
                    break
                elif "cd" in recvline:
                    if recvline == 'cd':
                        chdir("/Users/kikuchiryuuho")
                    else:
                        try:
                            chdir(recvline.strip("cd "))
                        except:
                            system(recvline)
                else:
                    proc_opt = run(str(recvline), shell=True, text=True, stdout=PIPE).stdout
            except:
                proc_opt = "実行できないコマンド"
                print(format_exc())
            finally:
                if proc_opt == True:
                    self.connection.send('none'.encode('utf-8'))
                else:
                    [exec("print(ch, end='', flush=True); sleep(0.004)") for ch in proc_opt]
                    self.connection.send(proc_opt.encode('utf-8'))


if __name__ == "__main__":
    testDrive = SocketServer(socket.gethostbyname(socket.gethostname()), 50000)
    testDrive.establish_connection()
    testDrive.authentification()
    testDrive.interaction()
    testDrive.close_connection()
