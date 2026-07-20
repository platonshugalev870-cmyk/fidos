class SyscallTable:
    def __init__(self):
        self.table = {}
        self.register_syscalls()
    def register_syscalls(self):
        self.table[0x01] = {"name": "pray", "handler": "handle_pray"}
        self.table[0x02] = {"name": "receive_revelation", "handler": "handle_revelation"}
        self.table[0x03] = {"name": "perform_miracle", "handler": "handle_miracle"}
        self.table[0x04] = {"name": "connect_to_god", "handler": "handle_connect"}
        self.table[0x05] = {"name": "disconnect", "handler": "handle_disconnect"}
        self.table[0x06] = {"name": "get_divine_status", "handler": "handle_status"}
        self.table[0xFF] = {"name": "system_halt", "handler": "handle_halt"}
    def get_handler(self, syscall_number):
        if syscall_number in self.table:
            return self.table[syscall_number]["handler"]
        return None
    def get_name(self, syscall_number):
        if syscall_number in self.table:
            return self.table[syscall_number]["name"]
        return "unknown"