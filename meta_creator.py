
#!/usr/bin/python3
import os
from main2025 import *
dbfile = "metavar.db"
conn = tkit.dbConnect(dbfile)
cur = conn.cursor()
inputfile = 'input_meta.csv'
outfile = 'meta_creator_out.csv'
outheader = ['variable_name', 'default_value', 'description', 'device', 'VDOM', 'mapped_value']
count = 0
sqlite_file = "metavar.db"
mysql_config = {
    "host": "xxx.xxx.xxx.xxx",
    "user": "user",
    "password": "pass",
}
mysql_db = "metavar"
try:
    os.remove(outfile)
except OSError as exception:
    print(exception)
#Write Headers to outfile
with open(outfile, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
    writer.writerow(outheader)
# Consume input file and create sqllite3 db and tables
with (open(inputfile, newline='') as f):
    reader = csv.reader(f)
    for row in reader:
         if count == 0:
             columns = tkit.create_table_from_csv(inputfile, 'metavar.db', 'metavar')
             columnsstr = ', '.join(columns)
             outcolumns = tkit.create_table_from_csv(outfile, 'metavar.db', 'outfile')
             outcolumnsstr = ', '.join(outcolumns)
             print(f'Meta-Variable Columns from {inputfile}: {columns}')
             print(f'Meta-Variable Columns from {outfile}: {outcolumns}')
             count += 1
         elif count != 0:
             values = ', '.join(f"'{w}'" for w in row)
             sqli = f'INSERT into metavar({columnsstr}) values ({values})'
             tkit.dbExecute(conn,sqli)
cur.execute('select * from metavar;')
meta = cur.fetchall()
default = ['ul1_port','ul1_gw','ul1_inbw','ul1_outbw','ul2_port','ul2_gw','ul2_inbw','ul2_outbw','branch_id','branch_supernet']
for x in default:
    tkit.dbExecute(conn,f"INSERT into outfile(variable_name, default_value, description, device, VDOM, mapped_value) values ('{x}','','','','','')")
for row in meta:
    z = 1
    for y in columns:
        name = row[1].replace(" ","_").replace('/',"_").lower()
        device = row[0]
        if 'device' not in y:
            if z == 1:
                name = f"'{name}_{y}','','','{device}','','{name.upper()}'"
            #elif 'vrf' in y:
                #add default value 0 to vrf metavar if present.
            #    name = f"'{name}_{y}',{0},'','{device}','','{row[z]}'"
            elif 'dhcp' in y:
                #add default value n to dhcp metavar present.
                name = f"'{name}_{y}','n','','{device}','','{row[z]}'"
            elif 'netid' in y:
                name = f"'{name}_{y}','','VlanID/DHCP Index','{device}','','{row[z]}'"
            else:
                name = f"'{name}_{y}','','','{device}','','{row[z]}'"

            sqli = f'INSERT into outfile({outcolumnsstr}) values ({name})'
            tkit.dbExecute(conn,sqli)
            z += 1
cur.execute('select * from outfile;')
meta = cur.fetchall()
cur.execute('select variable_name from outfile;')
names = cur.fetchall()
keys = columns
del keys[0]
temp = {}
jinja = []
output = set()
a = 0
for x in names:
    for k in keys:
        if 'ul' in x[0]:
            pass
        elif k in x[0]:
            temp.update({k:x[0]})
            a +=1
            if a == len(keys):
                if temp in jinja:
                    pass
                else:
                    jinja.append(dict(temp))
                y = ("{" + ', '.join(str("'" + key + "'") + ':' + str(value) for key, value in temp.items()))
                output.add(y+'},')
                a = 0
jinja_out = sorted(list(output))
csvout = input('Create a Local CSV FIle? (N): ')
#printscripts = input('Print Scripts (N): ')
if 'y' in csvout.lower():
    with open(outfile, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
        for row in meta:
            writer.writerow(row)
    try:
        os.remove(dbfile)
    except OSError as exception:
        print(exception)
else:
    print(f"Writing to {mysql_config['host']} as {mysql_config['user']}")
    tkit.sqlite_to_mysql(dbfile, mysql_config, mysql_db)
    try:
        os.remove(outfile)
        os.remove(dbfile)
    except OSError as exception:
        print(exception)
print('\n{# Script #1: Main jinja.loop Import CLI template For FMG. Create new FMG CLI Jinja Template#}')
jhead = '''{%- set vlans = 
  ['''
print(jhead)
for x in jinja_out:
    print('\t'+ x)
print('''  ]
-%}\n''')
