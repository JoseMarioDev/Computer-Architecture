"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    # Step 1: Add the constructor to cpu.py
    # Add list properties to the CPU class to hold 256 bytes of memory and 8 general-purpose registers.
    # Also add properties for any internal registers you need, e.g. PC.
    # Later on, you might do further initialization here, e.g. setting the initial value of the stack pointer.

    HLT = 1
    LDI = 130
    PRN = 71
    MUL = 162

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.ram = [0] * 256
        # 8 general-purpose registers
        self.register = [0] * 8
        # PC
        self.pc = 0

    # accepts the address in RAM and returns the value stored there

    # Step 2: Add RAM functions
    # In CPU, add method ram_read() and ram_write() that access the RAM inside the CPU object.
    # ram_read() should accept the address to read and return the value stored there.
    # raw_write() should accept a value to write, and the address to write it to.

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    # Step 4
    # halt the CPU and exit the emulator
    def hlt(self, operand_a, operand_b):
        return (0, False)
    # load immediate, store a value in a register, or set this register to this value

    # Step 5: Add the LDI instruction

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        return (3, True)

    # Step 6: Add the PRN instruction
    # prints the numeric value stored in a register

    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        return (2, True)

    # def load(self):
    #     """Load a program into memory."""

    #     address = 0

    #     # For now, we've just hardcoded a program:

    #     program = [
    #         # From print8.ls8
    #         0b10000010,  # LDI R0,8
    #         0b00000000,
    #         0b00001000,
    #         0b01000111,  # PRN R0
    #         0b00000000,
    #         0b00000001,  # HLT
    #     ]

    #     for instruction in program:
    #         self.ram[address] = instruction
    #         address += 1

    def load(self, filename):
        print(filename)
        """Load a program into memory."""
        try:
            address = 0
            # Open the file
            with open(filename) as f:
                # Read all the lines
                for line in f:
                    # Parse out comments
                    comment_split = line.strip().split("#")
                    # Cast the numbers from strings to ints
                    value = comment_split[0].strip()
                    # Ignore blank lines
                    if value == "":
                        continue

                    num = int(value, 2)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    if len(sys.argv) != 2:
        print("ERROR: Must have file name")
        sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        # Step 3: Implement the core of CPU's run() method
        """Run the CPU."""
        running = True

        while running:
            ir = self.ram_read(self.pc)

            if ir == self.HLT:
                running = False
            elif ir == self.LDI:
                target_register = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.register[target_register] = value
                self.pc = self.pc + 3
            elif ir == self.PRN:
                print(self.register[self.ram_read(self.pc + 1)])
                self.pc = self.pc + 2
            elif ir == self.MUL:
                print(self.register[self.ram_read(self.pc + 1)]
                      * self.register[self.ram_read(self.pc + 2)])
                self.pc = self.pc + 3
            else:
                print('Bad instruction')
                self.trace()
                running = False
