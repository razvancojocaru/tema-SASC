#Collision value: 735174213495964967 locations: 122347852 - 893212236
#Collision value: 1247948159810218381 locations: 122347854 - 893212238
#Collision value: 6810904725035589557 locations: 1064792912 - 3260804768
#Collision value: 7704228482905844942 locations: 122347855 - 893212239
#Collision value: 13709301323247256842 locations: 122347853 - 893212237
collisions = [(122347852, 893212236), (122347854, 893212238), (1064792912, 3260804768), (122347855, 893212239), (122347853, 893212237)]

filepath = 'total.out'
cookie = "ABCDEFGH"

data = "DUMMY IV"
data += "GET / HT"
data += "TP/1.1\r\n"
data += "Host: ww"
data += "w.ab.ro\r"
data += "\nCookie:"
data += " secret="
data += 9 * cookie
data += "\r\nAccept"
data += ": text/p"
data += "lain\r\n\r\n"

MESSAGE_BLOCKS = [data[i*8: (i+1)*8] for i in range(len(data) / 8)]

def get_block_from_file(ix):
	f = open(filepath, 'rb')
	f.seek(ix * 8)

	return f.read(8)

def check_collisions(cols):
	for k, v in cols:
		assert get_block_from_file(k) == get_block_from_file(v), 'this is not a collision'
check_collisions(collisions)

def xor(bt1, bt2):
	r = bytearray([i^j for i, j in zip(bytearray(bt1), bytearray(bt2))])
	return r

def recover_plaintext():
	for k, v in collisions:
		mi_index = k % len(MESSAGE_BLOCKS)
		mj_index = v % len(MESSAGE_BLOCKS)

		success = 0
		if (mi_index >= 7 and mi_index <= 15) and (mj_index <= 6 or mj_index >= 16):
			print "useful collision"
			success = 1
			know_plaintext_index = mj_index

		if (mj_index >= 7 and mj_index <= 15) and (mi_index <= 6 or mi_index >= 16):
			print "useful collision"
			success = 1
			know_plaintext_index = mi_index

		if success == 0:
			continue

		ci_previous = get_block_from_file(k-1)
		cj_previous = get_block_from_file(v-1)

		cipher = xor(ci_previous, cj_previous)

		mi = MESSAGE_BLOCKS[mi_index]
		mj = MESSAGE_BLOCKS[mj_index]

		found_cookie = xor(cipher, MESSAGE_BLOCKS[know_plaintext_index])
		print "found secret cookie: %s" % found_cookie
