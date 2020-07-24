"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL=  0b10100010 
POP = 0b01000110
PUSH= 0b01000101
MUL = 0b10100010 
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class.All CPUs manage a _stack_ that can be used to store information temporarily."""

    def __init__(self):
        # ""You’ll have to convert the binary strings to integer values to store in RAM. The built-in int() function can do that when you specify a number base as the second argument:x = int("1010101", 2)  # Convert binary string to integer."""
        # """Construct a new CPU."""

        self.ram= [0]*256
        self.register = [0] * 8
        self.pc= 0   #(program count)
        # self.sp=0xF4 #sp:stack pointer
        self.running = True

        self.pc = self.register[0] #A program counter is a register in a computer processor that contains the address (location) of the instruction being executed at the current time. As each instruction gets fetched, the program counter increases its stored value by 1.

        self.ir =0 #Instruction Register

        #stack_ pointer R7
        self.sp=7 
        self.branch ={
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            MUL: self.mul,
            POP: self.pop,
            PUSH: self.push,
            CALL: self.call,
            RET: self.ret,            
            CMP: self.cmp,
            JMP: self.jmp,
            JEQ: self.jeq,
            JNE: self.jne
        }
        self.flag = 0b00000000
    
    #access the RAM inside the CPU object. ram_read() accept the address to read and return the value stored there. 
    def ram_read(self, index):
        return self.ram[index]

    #should accept a value to write, and the address to write it to
    def ram_write(self, index, value):
        self.ram[index] = value

    def load(self, filename):
        """Load a program into memory. open a file, read in its contents   and save appropriate data into RAM.You’ll have to convert the binary strings to integer values to store in RAM."""

        address = 0
   
        # if len(sys.argv) != 2:
        #     print("usage: comp.py filename")
        #     sys.exit(1)
        
        #If runs python3 ls8.py examples/mult.ls8,sys.argv[0] is the name of the running program itself.  sys.argv[0] == "ls8.py"; sys.argv[1] == "examples/mult.ls8": the name of the file to load.read in its contents line by line, and save appropriate data into RAM.
        with open(sys.argv[1], 'r') as f:
            for line in f:                     
                line = line.split("#",1)[0]
                try:                               
                    line = int(line, 2)  # int() is base 10 by default
                except ValueError:
                            continue
                # memory[address] = line
                self.ram_write(address,line)

                address += 1

                 
        # except FileNotFoundError:

        #     print(f"Couldn't find file {sys.argv[1]}")

        # sys.exit(1)

    def alu(self, op, reg_a, reg_b):


        """ALU operations(Arithmetic logic unit). MUL is the responsiblity of the ALU,`MUL registerA registerB` Multiply the values in two registers together and store the result in registerA.."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "CMP":  
            if self.register[reg_a] == self.register[reg_b]:
                self.flag = 0b00000001
            elif self.register[reg_a] < self.register[reg_b]:
                self.flag = 0b00000100
            elif self.register[reg_a] > self.register[reg_b]:
                self.flag = 0b00000010
            else:
                self.flag = 0b00000000
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.Some instructions requires up to the next two bytes of data after the PC in memory to perform operations on. Sometimes the byte value is a register number.  Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
        """
        
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
             
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU. Read the memory address that’s stored in register PC, and store that result in IR, the Instruction Register"""
        # IR=[]
        # PC=[]
        
        # sp=[]
        # running = True

        while self.running:
            #Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b
            operand_a =self.ram_read(self.pc + 1)
            operand_b =self.ram_read(self.pc + 2)# the next two bytes of data after the PC in memory to perform operations on.


            ir = self.ram_read(self.pc)
            if ir in self.branch:
                self.branch[ir](operand_a, operand_b)
            else:
            
                print(f"Unknown instruction {ir}")
                sys.exit(1)  #halt the CPU and exit the emulator


    def hlt(self, operand_a, operand_b):

        self.running =False

    #load "immediate"
    def ldi (self, operand_a, operand_b):#The byte value of some instruction is a constant value for LDI.
        self.register[operand_a]= operand_b
        self.pc+=3


    # PRN register` pseudo-instruction, Print numeric value stored in the given register.print to the console the decimal integer value that is stored in the given register.  

    def prn(self, operand_a, operand_b):
        self.pc+=2
        print(self.register[operand_a])
    
    def mul (self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)
        self.pc += 3

    def push(self,operand_a, operand_b):

        # PUSH a value in a register onto the stack:
        # decrement stack pointer
        # register[SP] -= 1
        # register[SP] &= 0xff  # keep R7 in the range 00-FF​      
        # reg_num = memory[pc + 1 ]  #get register value

        self.sp -= 1
        # reg_num = self.ram_read[self.pc + 1 ]
        value =self. register[operand_a]

        # Store in memory/Store the value in the register into RAM at the address stored in SP. address_to_push_to = register[SP]. memory[address_to_push_to] = value
        self.ram_write(self.sp, value)
        self.pc += 2

    """`POP register`,pop value at the top of the stack into the given register.Copy the value from the address pointed to by `SP` to the given egister. Increment `SP`. `PUSH register`Push the value in the given register on the stack.1. Decrement the `SP`.2. Copy the value in the given register to the address pointed to by`SP`"""
    def pop(self,  operand_a, operand_b): 

        # Get value from RAM
        address_to_pop_from = self. register[self.sp]        
         
        # value = memory[address_to_pop_from] 
        value = self.ram[self.register[self.sp]]
        # Store in the given register       
        # reg_num = memory[pc + 1]
        # reg_num =self.ram_read(self.pc + 1)
        self.register[operand_a] = value
        # Increment SP
        self.sp += 1
        self.pc += 2 
    
    #Return from subroutine.
    # Pop the value from the top of the stack and store it in the `PC`.
    #`CALL register` Calls a subroutine (function) at the address stored in the register. 1. The address of the ***instruction*** _directly after_ `CALL` is  pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing. 2. The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC can move forward or backwards from its current location.```

    def call(self,  operand_a, operand_b):
        
        return_addr = self.pc + 2  # Get address of the next instruction       

        # Push that on the stack
        self.register[self.sp] -= 1

        # address_to_push_to = self.register[self.sp]
        self.ram[register[self.sp]] = return_addr

        # Set the PC to the subroutine address
        # reg_num = memory[pc + 1]
         
        subroutine_addr =self. register[operand_a]
        self.pc = subroutine_addr

    def ret(self,  operand_a, operand_b):
        # Get return address from the top of the stack

        # address_to_pop_from = self.register[self.sp]

        return_addr = self.register[self.register[self.sp]]
        # Set the PC to the return address
        self.pc = self. ram_read(return_addr )       
        self.register[self.sp] += 1
         
        #return_addr = memory[address_to_pop_from]
        # pc = return_addr
       
    def cmp(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)
        self.pc += 3

    def jeq(self, operand_a, operand_b):
        """If `equal` flag is set (true), jump to the address stored in the given register. """
        if self.flag == 0b00000001:
            #self.flag == [1]
            self.pc = self.register[operand_a]
        else:
            self.pc += 2

    def jne(self, operand_a, operand_b):
        """`JNE register` if `E` flag is clear (false, 0), jump to the address stored in the given register."""
        
        if self.flag != 0b00000001:            
            self.pc = self.register[operand_a]
        else:
            self.pc += 2

    def jmp(self, operand_a, operand_b):
        """`JMP register`Jump to the address stored in the given register.Set the `PC` to the address stored in the given register."""

        self.pc = self.register[operand_a]
        print(f'pc instruction stored in {self.pc}')