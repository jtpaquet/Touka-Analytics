import os
import json
import codecs


src_filename = os.path.join("touka_18juillet2021", "touka_18juillet2021.json")
dst_filename = os.path.join("touka_18juillet2021", "messages_all.json")

with open(src_filename, 'r') as src_file:
    with open(dst_filename, 'w', encoding='utf-8') as dst_file:
        json_data = json.load(src_file)
        for msg in json_data:
            if 'content' in msg.keys():
                msg['content'] = msg['content'].encode('latin1').decode('utf-8', errors="replace")
            if 'sender_name' in msg.keys():
                msg['author'] = msg['sender_name'].encode('latin1').decode('utf-8', errors="replace")
                del msg['sender_name']
            if 'timestamp_ms' in msg.keys():
                msg['timestamp'] = msg['timestamp_ms']
                del msg['timestamp_ms']
            if 'reactions' in msg.keys():
                for reaction in msg['reactions']:
                    reaction['actor'] = reaction['actor'].encode('latin1').decode('utf-8', errors="replace")
                    reaction['reaction'] = reaction['reaction'].encode('latin1').decode('utf-8', errors="replace")
            if 'users' in msg.keys():
                for user in msg['users']:
                    user['name'] = user['name'].encode('latin1').decode('utf-8', errors="replace")
        json.dump(json_data, dst_file, indent=4, sort_keys=True, ensure_ascii=False)

u1 = "J\u00c3\u00a9r\u00c3\u00a9my Talbot-P\u00c3\u00a2quet"
u2= "J\u00c3\u00a9r\u00c3\u00b4me Sirois Charron"
print(u1.encode('latin1').decode('utf-8'))
print(u2.encode('latin1').decode('utf-8'))
