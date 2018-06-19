#######################################################
# Project 1: MIPS Disassembler (Teh Zi Cong Nicholas) #
#######################################################

# OPCODE for I-format instruction
opcodes = {4:"beq", 5:"bne", 35:"lw", 43:"sw"}

# FUNC for R-format instruction
funcs = {32:"add", 34:"sub", 36:"and", 37:"or", 42:"slt"}

# Masks to extract a specific part
mask = {"opcode":0b11111100000000000000000000000000,
          "src1":0b00000011111000000000000000000000,
          "src2":0b00000000000111110000000000000000,
          "dest":0b00000000000000001111100000000000,
          "func":0b00000000000000000000000000111111,
          "offset":0b00000000000000001111111111111111}

address = 0x9A040
        
def disassemble(instruction):
    global address
    # Get the OPCODE with the mask and shift right by 26-bits
    print_address = str(hex(address).upper())[2:]
    curr_address = address
    address += 4 # Increment address by 4
    opcode = (instruction & mask["opcode"]) >> 26
    reg_src1 = (instruction & mask["src1"]) >> 21
    reg_src2 = (instruction & mask["src2"]) >> 16

    # OPCODE 0 means is R-format instruction
    if opcode == 0:
        # Get the FUBC with the mask, there is no need to shift
        func = instruction & mask["func"]
        reg_dest = (instruction & mask["dest"]) >> 11
        return print_address + " " + funcs[func] + " " + "$" + str(reg_dest) + ", $" + str(reg_src1) + ", $" + str(reg_src2)

    # OPCODE 4 means is beq, OPCODE 5 means is bne
    elif opcode == 4 or opcode == 5:
        # Additional modification required for branching
        offset = (instruction & mask["offset"]) << 2
        offset += 4
        offset = twos_complement(offset, 18)
        next_address = str(hex(curr_address + offset).upper())[2:]
        return print_address + " " + opcodes[opcode] + " " + "$" + str(reg_src1) + ", $" + str(reg_src2) + ", address " + str(next_address)
            
    # OPCODE 35 means is lw, 43 means is sw
    elif opcode == 35 or opcode == 43: 
        offset = twos_complement(instruction & mask["offset"], 16)
        return print_address + " " + opcodes[opcode] + " " + "$" + str(reg_src2) + ", " + str(offset) + "($" + str(reg_src1) + ")"

    else:
        return "OPCODE not found"
        
# To handle negative offset
def twos_complement(num, bits):
    most_significant_bit = num >> bits - 1
    # If most significant bit is 0, means is positive
    if most_significant_bit == 0:
        return num
    else: # negative, need to +1
        num <<= 1
        num >>= 1
        return num - 2**bits
