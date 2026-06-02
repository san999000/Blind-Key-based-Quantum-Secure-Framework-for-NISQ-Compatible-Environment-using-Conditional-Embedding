from flask import Flask, render_template, request

from image_data import image
import secret_data

from circuit.neqr_circuit import create_circuit
from extract_message import extract_secret_message

from qiskit_aer import AerSimulator
from qiskit import transpile

import matplotlib.pyplot as plt
import ast


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():

    measurement_text = ""

    recovered_message = None

    circuit_generated = False

    error_message = None

    if request.method == 'POST':

        action = request.form['action']

        # =================================================
        # SENDER MODULE
        # =================================================

        if action == 'embed':

            # image input
            p00 = int(request.form['p00'])
            p01 = int(request.form['p01'])

            p10 = int(request.form['p10'])
            p11 = int(request.form['p11'])

            # normalize 0-255 -> 0-3
            image.clear()

            image.extend([

                [
                    p00 // 64,
                    p01 // 64
                ],

                [
                    p10 // 64,
                    p11 // 64
                ]
            ])

            # secret message
            secret = request.form['secret']

            secret_key = request.form['secret_key']

            # =====================================
            # VALIDATION
            # =====================================

            if (

                len(secret) != 4 or
                len(secret_key) != 4 or

                not all(bit in '01' for bit in secret) or
                not all(bit in '01' for bit in secret_key)

            ):

                error_message = (
                    "Secret and key must be 4-bit binary values."
                )

                return render_template(

                    'index.html',

                    error_message=error_message
                )

            secret_data.secret_message = secret

            secret_data.secret_key = secret_key

            # create circuit
            qc = create_circuit()

            qc.measure(range(4), range(4))

            # simulator
            simulator = AerSimulator()

            compiled_circuit = transpile(
                qc,
                simulator
            )

            job = simulator.run(
                compiled_circuit,
                shots=1024
            )

            result = job.result()

            counts = result.get_counts()

            print("\nMEASUREMENT RESULTS:\n")

            print(counts)

            # convert counts to text
            measurement_text = str(counts)

            # save circuit image
            figure = qc.draw(output='mpl')

            figure.savefig(
                'static/output/quantum_circuit.png'
            )

            plt.close('all')

            circuit_generated = True

        # =================================================
        # RECEIVER MODULE
        # =================================================

        elif action == 'extract':

            measurement_text = request.form['measurement_text']

            receiver_key = request.form['receiver_key']

            # =====================================
            # RECEIVER KEY VALIDATION
            # =====================================

            if (

                len(receiver_key) != 4 or

                not all(
                    bit in '01'
                    for bit in receiver_key
                )

            ):

                recovered_message = (
                    "Receiver key must be 4-bit binary."
                )

            else:

                try:

                    counts = ast.literal_eval(
                        measurement_text
                    )

                    recovered_message = extract_secret_message(
                        counts,
                        receiver_key
                    )

                except:

                    recovered_message = (
                        "Invalid encoded states"
                    )

    return render_template(

        'index.html',

        measurement_text=measurement_text,

        recovered_message=recovered_message,

        circuit_generated=circuit_generated,

        error_message=error_message
    )


if __name__ == '__main__':

    app.run(debug=True)