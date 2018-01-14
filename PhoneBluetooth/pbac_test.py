import lightblue

client = lightblue.obex.OBEXClient( '00:23:D6:32:2F:0E', 4 )
client.connect( {'Target':buffer('\x79\x61\x35\xf0\xf0\xc5\x11\xd8\x09\x66\x08\x00\x20\x0c\x9a\x66') } )
f = file( 'text.txt', 'wb' )
client.get( {'Type':'x-bt/phonebook', 'Name':'telecom/pb.vcf' }, f )
