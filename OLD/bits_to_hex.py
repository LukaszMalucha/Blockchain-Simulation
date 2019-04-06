dec = 389508950
true_hex = hex(dec)[2:]
hex_string = str(true_hex)
first_two = true_hex[:2]
the_rest = true_hex[2:]
first_two_decimal = int(first_two, 16)
target_length = int(first_two_decimal) * 2
following_zeros_amount = int(target_length) - len(the_rest)
following_zeros = '0' * following_zeros_amount
base_hex = the_rest + following_zeros  
leading_zeros = '0'* (64 - len(base_hex))
final_hex = leading_zeros + base_hex
print (final_hex)