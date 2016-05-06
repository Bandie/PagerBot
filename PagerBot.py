#!/usr/bin/python

# Author: Bandie Yip Kojote for TTYgap
# License: GNU-GPLv3
# Year: 2016
# 
# Software is provided AS IS and so on.


# Host of the IRC server
HOST="irc.example.com"
# TLS port of the IRC server
PORT=6697
# Nick of the bot
NICK="PagerBot"
# Ident of the bot
IDENT="PagerBot"
# Realname of the bot
REALNAME="PagerBot"
# Channel which should be joined
CHAN="#supercoolchan"


# Mail adress you're sending from
FROM="ircbot@example.com"


import sys
import socket
import string
import ssl
import time
import smtplib




def page(receiver, text, user):

    number=""


    # CONFIGURE YOUR USERS HERE

#    if(receiver=="someone"):
#        number="1234567"

    else:
        return "The username you tried to page has no number saved."




    to=number+"@ecityruf.de"
    message=HOST+":"+user+":"+text
    if(len(message)>80):
        return "The message \"%s\" is too big. It has to be less than 80 characters.\r\n" % (message)
    m = smtplib.SMTP('smtpgw3.emessage.de')
    try:
        m.sendmail(FROM, to, "FROM: %s\nTO: %s\nSUBJECT: %s" % (FROM, to, message))
    except:
        e=sys.exc_info()[0]
        return "Error: %s" % e
    m.quit()
    return "Sent."







readbuffer=""

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
ircsock = ssl.wrap_socket(s)
ircsock.send("NICK %s\r\n" % (NICK))
ircsock.send("USER %s %s no :%s\r\n" % (IDENT, HOST, REALNAME))
time.sleep(2)
ircsock.send("MODE %s +B\r\n" %(NICK))
ircsock.send("JOIN %s\r\n" % (CHAN))
print("OK\n")

while 1:
    readbuffer=readbuffer+ircsock.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    pagingtext=""

    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)



        if(line[0]=="PING"):
            ircsock.send("PONG %s\r\n" % line[1])

        if(line[1]=="PRIVMSG"):
            un=string.split(line[0], "!")
            un2=string.split(un[0], ":")
            usernick=un2[1]

            if("#" in line[2]):
                if(line[3] == ":%s:" % (NICK) or line[3] == ":&pager"):
                    ircsock.send("PRIVMSG %s %s: I only do stuff via query.\r\n" % (line[2], usernick))

            if("#" not in line[2]):
                if(line[3] == ":help"): 
                    ircsock.send("PRIVMSG %s This is a bot to use a paging service.\r\n" % (usernick))
                    time.sleep(1)
                    ircsock.send("PRIVMSG %s Use \"/msg %s &pager <Username> <Message>\" to page someone.\r\n" % (usernick, NICK))
                elif(line[3] == ":&pager"):
                    pagingtext=' '.join(line[5:])
                    print("%s tries to send to %s \"%s\"\n" % (usernick, line[4], pagingtext))
                    ircsock.send("PRIVMSG %s %s\r\n" % (usernick, page(line[4], pagingtext, usernick)))


#    print(line)


