cookie = "ABCDEFGH"


'''
data = """GET / HTTP/1.1\r
Host: www.ab.ro\r
Cookie: secret={0}\r
Accept: text/plain\r
\r
""".format(cookie*9)
'''

data  = "GET / HT"
data += "TP/1.1\r\n"
data += "Host: ww"
data += "w.ab.ro\r"
data += "\nCookie:"
data += " secret="
data += 9 * cookie
data += "\r\nAccept"
data += ": text/p"
data += "lain\r\n\r\n"

print len(data)
print data