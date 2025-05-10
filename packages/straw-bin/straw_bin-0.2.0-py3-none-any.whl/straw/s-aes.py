def int_to_bin(n, bits=8):
    return format(n, f'0{bits}b')

def bin_to_int(binary):
    return int(binary, 2)

def xor(a, b):
    return ''.join('1' if a[i] != b[i] else '0' for i in range(len(a)))

def left_shift(key, n):
    return key[n:] + key[:n]

def s_box(nibble, encrypt=True):
    s_boxes = {
        '0000': '1001', '0001': '0100', '0010': '1010', '0011': '1011',
        '0100': '1101', '0101': '0001', '0110': '1000', '0111': '0101',
        '1000': '0110', '1001': '0010', '1010': '0000', '1011': '0011',
        '1100': '1100', '1101': '1110', '1110': '1111', '1111': '0111'
    }
    inv_s_boxes = {v: k for k, v in s_boxes.items()}
    return s_boxes[nibble] if encrypt else inv_s_boxes[nibble]

def apply_sbox(state, encrypt=True):
    return s_box(state[:4], encrypt) + s_box(state[4:], encrypt)

def key_expansion(key):
    w0 = key[:8]
    w1 = key[8:]
    rcon1 = '10000000'
    rcon2 = '00110000'

    w2 = xor(w0, xor(apply_sbox(left_shift(w1, 4)), rcon1))

    w3 = xor(w1, w2)

    w4 = xor(w2, xor(apply_sbox(left_shift(w3, 4)), rcon2))

    w5 = xor(w3, w4)

    return w0 + w1, w2 + w3, w4 + w5

def mix_columns(state, encrypt=True):
    left = state[:8]
    right = state[8:]
    
    if encrypt:
        new_left = xor(left, right)
        new_right = xor(left, right)
    else:
        new_left = right
        new_right = left
    
    return new_left + new_right

def add_round_key(state, round_key):
    return xor(state, round_key)

def s_aes_encrypt(plaintext, key):
    k0, k1, k2 = key_expansion(key)

    state = add_round_key(plaintext, k0)

    state = apply_sbox(state)
    state = mix_columns(state)
    state = add_round_key(state, k1)

    state = apply_sbox(state)
    state = add_round_key(state, k2)
    
    return state

def s_aes_decrypt(ciphertext, key):
    k0, k1, k2 = key_expansion(key)
    state = add_round_key(ciphertext, k2)

    state = apply_sbox(state, encrypt=False)
    state = add_round_key(state, k1)
    state = mix_columns(state, encrypt=False)

    state = apply_sbox(state, encrypt=False)
    state = add_round_key(state, k0)
    
    return state

def main():
    print("Simplified AES (S-AES) Encryption/Decryption")
    print("===========================================")
    
    while True:
        choice = input("\nChoose mode:\n1. Encrypt\n2. Decrypt\n3. Exit\nChoice: ")
        if choice == '3':
            break
            
        if choice not in ['1', '2']:
            print("Invalid choice. Try again.")
            continue

        key_input = input("Enter 16-bit binary key: ")
        if len(key_input) != 16 or not all(bit in '01' for bit in key_input):
            print("Invalid key. Must be 16 binary bits.")
            continue

        text_input = input("Enter 16-bit binary text: ")
        if len(text_input) != 16 or not all(bit in '01' for bit in text_input):
            print("Invalid text. Must be 16 binary bits.")
            continue
        
        if choice == '1':
            result = s_aes_encrypt(text_input, key_input)
            print(f"Encrypted result: {result}")
        else:
            result = s_aes_decrypt(text_input, key_input)
            print(f"Decrypted result: {result}")

if __name__ == "__main__":
    main()