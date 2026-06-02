def extract_secret_message(counts, receiver_key):

    recovered_bits = []

    print("\nDecoded States:\n")

    sorted_states = sorted(
        counts.keys()
    )

    for index, state in enumerate(sorted_states):

        reversed_state = state[::-1]

        value_bits = reversed_state[0:2]

        final_v0 = int(
            value_bits[1]
        )

        key_bit = int(
            receiver_key[index]
        )

        secret_bit = final_v0 ^ key_bit

        recovered_bits.append(
            str(secret_bit)
        )

        print(

            f"State: {state} | "
            f"Encoded Bit: {final_v0} | "
            f"Key Bit: {key_bit} | "
            f"Recovered Bit: {secret_bit}"
        )

    return ''.join(recovered_bits)