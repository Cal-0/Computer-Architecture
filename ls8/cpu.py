"""CPU functionality."""
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.fl  = [0] * 8 
        self.ram = [0] * 256
        self.reg[7] = 0xF4
        self.sp = self.reg[7]
        self.pc = 0
    
    def ram_read(self):
        ram_index = self.ram[self.pc + 1]
        self.pc += 2
        return self.ram[ram_index]

    def ram_write(self):
        where_save = self.ram[self.pc + 1]
        what_save = self.ram[self.pc + 2]
        self.ram[where_save] = what_save
        self.pc += 3


    def load(self):
        """Load a program into memory."""
        try:
            address = 0

            if len(sys.argv) < 2:
                print('Please pass in a second file name to use')
            file_name = sys.argv[1]


            file_name = 'examples/' + file_name


            with open(file_name) as file:
                for line in file:
                    split_line = line.split('#')
                    command = split_line[0].strip()
                    if command == '':
                        continue 
                    
                    #str to int
                    num = int(command, 2)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[1]} file was not found.')


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # print('op', op)
        # print("ADD")

        if op == "ADD":
            added = self.reg[reg_a] + self.reg[reg_b]
            self.reg[reg_a] = added

        if op == "MUL":
            multiplied = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = multiplied
        else:
            pass

    def trace(self):

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        #table of names for the commands
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        POP = 0b01000110
        RET = 0b00010001
        ADD = 0b10100000
        CMP = 0b10100111
        PUSH = 0b01000101
        CALL = 0b01010000
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        running = True
        while running == True:
    
            command = self.ram[self.pc]
            
            if command == HLT:
                running = False

            if command == LDI:
                reg = self.ram[self.pc + 1]
                integer = self.ram[self.pc + 2]
                self.reg[reg] = integer
                self.pc += 3

            if command == PRN:
                reg = self.ram[self.pc + 1]
                print(self.reg[reg])
                self.pc += 2

            if command == MUL:
                reg_1 = self.ram[self.pc + 1]
                reg_2 = self.ram[self.pc + 2]
                self.alu("MUL", reg_1, reg_2)
                self.pc += 3

            if command == ADD:
                reg_1 = self.ram[self.pc + 1]
                reg_2 = self.ram[self.pc + 2]
                self.alu("ADD", reg_1, reg_2)
                self.pc += 3

            if command == PUSH:
                self.sp -= 1
                value = self.reg[self.ram[self.pc + 1]]
                self.ram[self.sp] = value
                self.pc += 2

            if command == POP:
                reg = self.ram[self.pc + 1]
                value = self.ram[self.sp]
                self.reg[reg] = value
                self.sp += 1
                self.pc += 2

            if command == CALL:
                reg = self.ram[self.pc + 1]
                address = self.reg[reg]
                return_address= self.pc+2
                self.sp -= 1
                self.ram[self.sp] = return_address
                self.pc = address

            if command == RET:
                return_address = self.ram[self.sp]
                self.sp += 1
                self.pc = return_address

            if command == CMP:

                reg_1_address = self.ram[self.pc + 1]
                reg_2_address = self.ram[self.pc + 2]
                reg_1 = self.reg[reg_1_address]
                reg_2 = self.reg[reg_2_address]

                if reg_1 == reg_2:
                    self.fl[-1] = 1
                if reg_1 != reg_2:
                    self.fl[-1] = 0

                if reg_1 > reg_2:
                    self.fl[-2] = 1
                if reg_1 > reg_2 == False:
                    self.fl[-2] = 0
           
                if reg_1 < reg_2:
                    self.fl[-3] = 1
                if reg_1 < reg_2 == False:
                    self.fl[-3] = 0


                self.pc += 3

            if command == JMP:
                
                address = self.ram[self.pc + 1]
                address_value = self.reg[address]
                self.pc = address_value

            if command == JEQ:
                address = self.ram[self.pc + 1]
                
                if self.fl[-1] == 1:
                    address = self.ram[self.pc + 1]
                    address_value = self.reg[address]
                    self.pc = address_value
                else:
                    self.pc += 2

            if command == JNE:
                
                if self.fl[-1] == 0:
                    address = self.ram[self.pc + 1]
                    address_value = self.reg[address]
                    self.pc = address_value
                else:
                    self.pc += 2