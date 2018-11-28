import ftplib
import os
import time
import paramiko
import threading


new_version = "Staj"


hosts = [
    {'address' :"192.168.30.157",'user':'staj','passwd':'00590059' },
    {'address' :"192.168.30.156",'user':'uzemtest','passwd':'00590059' },
]


def main_method(address,user,passwd):

    FTPSession = ftp_connection(address, user, passwd)
    print("\n[***]FTP Uploading Processes Starting... for: "+address+"[***]\n")
    print("\n----------------------ATTENTION: This process can take a long time.Please wait...----------------------\n")
    ftp_uploadfile(FTPSession)

    SSHSession = ssh_connection(address,user,passwd)
    print("[***]SSH Upgrading Processes Starting... for: " + address + "[***]\n")
    ssh_upgrade(SSHSession)


    SSHSession.close()
    FTPSession.close()


def ssh_connection(address,user,passwd):
    print("\n[***]SSH Working for... : "+address+"[***]")
    while True:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(address, username=user, password=passwd, port=22)
            print("[***]SSH Connection OK! on: " + address + "[***]")
            break

        except paramiko.SSHException as e:
            print("SSH error for: "+address+" Please check details: ",e)
            ssh.close()
            print("\n[***]SSH was end... on: "+address+" Type:FAILED[***]\n")
            break

    return ssh


def ssh_upgrade(ssh):

    channel = ssh.invoke_shell()
    out = channel.recv(9999)
    time.sleep(0.9)

    channel.send('ls\n')
    channel.send('cd ftp/' + new_version + "\n")
    channel.send('ls\n')
    print(out.decode("ascii"))
    time.sleep(0.7)

    channel.send('ip addr | grep ens33\n')
    print(out.decode("ascii"))
    time.sleep(0.6)
    channel.send('cat stajdosya.txt\n')
    print(out.decode("ascii"))
    time.sleep(0.8)

    out = channel.recv(9999)
    channel.send('ip addr\n')
    channel.send('\n')
    print(out.decode("ascii"))
    while not channel.recv_ready():
        time.sleep(0.7)

    ssh.close()

    print("\n[***]SSH was end... Type:SUCCESSFUL[***]\n")




def ftp_connection(address,user,passwd):
    print("[***]FTP Working... for: " + address + " [***]")
    while True:

        try:
                ftp = ftplib.FTP(address)
                ftp.login(user=user, passwd=passwd)
                print(ftp.getwelcome())
                print("\n[***]FTP Connection OK! on: " + address + "[***]")
                break

        except ftplib.all_errors as e:
                print("Failed to connect to: "+address+" Check your address and credentials.Details..:", e)
                ftp.close()
                break
    return ftp


def ftp_uploadfile(ftp):

    while True:

        try:

                ftp.mkd("" + new_version)
                ftp.cwd("/" + new_version)
                ftp.dir()
                file = open("stajdosya.txt", "rb")
                ftp.storbinary("STOR stajdosya.txt",file)
                print("END!!!!!!!!!!!!!!!!!!!!!")
                ftp.dir()
                ##file.close()
                print("\n[***]UPLOADING OK!!! [***]")
                print("[***]FTP was end... Type:SUCCESSFUL...[***]\n")
                break

        except ftplib.all_errors as e:
                print("Failed to uploading...Please check details.Details..:", e)
                ftp.close()
                print("\n[***]FTP was end... Type:FAILED[***]")
                break

print("\n")
print("[***]WELCOME TO... NOKIA UPGRADE SCRIPT!!![***]")
print("[***]PROCESS STARTED...[***]\n")



threads = []
for item in hosts:
    t = threading.Thread(name='main_method', target=main_method, args=(item['address'], item['user'], item['passwd'],))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()


print("\n[***]DONE..!Everything OK..!Good bye..![***]")