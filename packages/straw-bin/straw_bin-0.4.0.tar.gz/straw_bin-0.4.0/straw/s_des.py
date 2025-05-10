def permute(key, perm_table):
    return ''.join(key[i-1] for i in perm_table)

def left_shift(key, n):
    return key[n:] + key[:n]

def xor(a, b):
    return ''.join('1' if a[i] != b[i] else '0' for i in range(len(a)))

def apply_sbox(s, input_bits):
    row = int(input_bits[0] + input_bits[3], 2)
    col = int(input_bits[1] + input_bits[2], 2)
    return format(s[row][col], '02b')

def key_generation(key):
    p10_table = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    key = permute(key, p10_table)

    left = key[:5]
    right = key[5:]
    left = left_shift(left, 1)
    right = left_shift(right, 1)

    p8_table = [6, 3, 7, 4, 8, 5, 10, 9]
    k1 = permute(left + right, p8_table)

    left = left_shift(left, 2)
    right = left_shift(right, 2)

    k2 = permute(left + right, p8_table)
    
    return k1, k2

def f_function(right_half, subkey):
    ep_table = [4, 1, 2, 3, 2, 3, 4, 1]
    expanded = permute(right_half, ep_table)

    xored = xor(expanded, subkey)

    s0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
    s1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
    
    s0_output = apply_sbox(s0, xored[:4])
    s1_output = apply_sbox(s1, xored[4:])

    p4_table = [2, 4, 3, 1]
    return permute(s0_output + s1_output, p4_table)

def s_des_encrypt(plaintext, key):
    k1, k2 = key_generation(key)

    ip_table = [2, 6, 3, 1, 4, 8, 5, 7]
    plaintext = permute(plaintext, ip_table)

    left = plaintext[:4]
    right = plaintext[4:]

    new_right = xor(left, f_function(right, k1))
    new_left = right

    left = new_left
    right = new_right

    new_right = xor(left, f_function(right, k2))
    new_left = right
    
    fp_table = [4, 1, 3, 5, 7, 2, 8, 6]
    return permute(new_left + new_right, fp_table)

def s_des_decrypt(ciphertext, key):
    k1, k2 = key_generation(key)

    ip_table = [2, 6, 3, 1, 4, 8, 5, 7]
    ciphertext = permute(ciphertext, ip_table)

    left = ciphertext[:4]
    right = ciphertext[4:]
    
    new_right = xor(left, f_function(right, k2))
    new_left = right

    left = new_left
    right = new_right

    new_right = xor(left, f_function(right, k1))
    new_left = right

    fp_table = [4, 1, 3, 5, 7, 2, 8, 6]
    return permute(new_left + new_right, fp_table)

def main():
    print("Simplified DES (S-DES) Encryption/Decryption")
    print("===========================================")
    
    while True:
        choice = input("\nChoose mode:\n1. Encrypt\n2. Decrypt\n3. Exit\nChoice: ")
        if choice == '3':
            break
            
        if choice not in ['1', '2']:
            print("Invalid choice. Try again.")
            continue

        key_input = input("Enter 10-bit binary key: ")
        if len(key_input) != 10 or not all(bit in '01' for bit in key_input):
            print("Invalid key. Must be 10 binary bits.")
            continue

        text_input = input("Enter 8-bit binary text: ")
        if len(text_input) != 8 or not all(bit in '01' for bit in text_input):
            print("Invalid text. Must be 8 binary bits.")
            continue
        
        if choice == '1':
            result = s_des_encrypt(text_input, key_input)
            print(f"Encrypted result: {result}")
        else:
            result = s_des_decrypt(text_input, key_input)
            print(f"Decrypted result: {result}")

if __name__ == "__main__":
    main()