import os
import sys


src_filename = os.path.join("utils","touka_10dec2019.json")
dst_filename = os.path.join("messages.json")

with open(src_filename, 'r') as src_file:
    with open(dst_filename, 'w') as dst_file:
        for line in src_file:
            dst_file.write(line.encode('latin_1').decode('utf-8'))

u1 = "J\u00c3\u00a9r\u00c3\u00a9my Talbot-P\u00c3\u00a2quet"
u2= "J\u00c3\u00a9r\u00c3\u00b4me Sirois Charron"
print(u1.encode('latin1').decode('utf-8'))
print(u2.encode('latin1').decode('utf-8'))
