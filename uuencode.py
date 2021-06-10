def font2bytes(file):
    with open(file, 'b+r') as file_opened:
        binary = file_opened.read()
        byte_list = [ int(x, 16) for x in binary.hex(' ', 1).split() ]
    return byte_list


# ~4Mb acces+uuencode
# ocaml tail recursive:  0.978s
# ocaml tail recursive3: 0.588s
# python imperative:     1.303s

def uuencode_byte_list(byte_list):
    ebyte_list = []
    n = len(byte_list)
    if n%3 == 1: 
        byte_list += [0x00, 0x00]
        n += 2
    if n%3 == 2:
        byte_list += [0x00]
        n += 1
    for i in range(0, n, 3):
        e = []
        tree_bytes = (byte_list[i] << 16 ) + (byte_list[i+1] << 8) + (byte_list[i+2]) 
        e.append(((tree_bytes >> 18) & 63) + 33)
        e.append(((tree_bytes >> 12) & 63) + 33)
        e.append(((tree_bytes >> 6) & 63) + 33)
        e.append((tree_bytes & 63) +33)

        ebyte_list += e
    return ebyte_list

def ebyte_list2string(ebyte_list):
    s = ''
    c = 1
    for x in ebyte_list:
        s += chr(x)
        if not c % 80: s+= '\n'
        c+=1
    return s

def uuencode(file):
    return ebyte_list2string(uuencode_byte_list(font2bytes(file)))