document.addEventListener("DOMContentLoaded", function () {

    console.log("PAYPAL PAGE LOADED");


    // ==========================================
    // ELEMENTS
    // ==========================================

    const amountInput = document.getElementById(
        "payment-amount"
    );

    const paypalContainer = document.getElementById(
        "paypal-button-container"
    );

    const paypalError = document.getElementById(
        "paypal-error"
    );

    const paystackForm = document.getElementById(
        "paystack-form"
    );

    const paystackAmount = document.getElementById(
        "paystack_amount"
    );


    // ==========================================
    // CHECK PAYPAL SDK
    // ==========================================

    console.log(
        "PayPal SDK:",
        typeof paypal
    );

    console.log(
        "Client ID present:",
        "{{ paypal_client_id|yesno:'YES,NO' }}"
    );


    if (typeof paypal === "undefined") {

        console.error(
            "PayPal SDK NOT LOADED"
        );

        paypalError.textContent =
            "PayPal could not be loaded. Please refresh the page.";

        return;
    }


    // ==========================================
    // PAYSTACK / MPESA
    // ==========================================

    if (paystackForm) {

        paystackForm.addEventListener(
            "submit",
            function (event) {

                const amount =
                    amountInput.value;


                if (
                    !amount ||
                    parseFloat(amount) <= 0
                ) {

                    event.preventDefault();

                    alert(
                        "Please enter a valid payment amount."
                    );

                    return;
                }


                paystackAmount.value =
                    amount;

            }
        );

    }


    // ==========================================
    // PAYPAL BUTTON
    // ==========================================

    paypal.Buttons({

        style: {
            layout: "vertical",
            color: "gold",
            shape: "rect",
            label: "paypal"
        },


        // ======================================
        // CREATE PAYPAL ORDER
        // ======================================

        createOrder: function () {

            const amount =
                amountInput.value;


            console.log(
                "Amount entered:",
                amount
            );


            if (
                !amount ||
                parseFloat(amount) <= 0
            ) {

                paypalError.textContent =
                    "Please enter a valid payment amount.";

                throw new Error(
                    "Invalid payment amount"
                );
            }


            const formData =
                new URLSearchParams();

            formData.append(
                "amount",
                amount
            );


            console.log(
                "Sending amount to Django:",
                amount
            );


            return fetch(
                "{% url 'paypal_create_order' session.id %}",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded",

                        "X-CSRFToken":
                            "{{ csrf_token }}"
                    },

                    body: formData
                }
            )

            .then(function (response) {

                console.log(
                    "Create order HTTP status:",
                    response.status
                );


                if (!response.ok) {

                    throw new Error(
                        "Django returned HTTP " +
                        response.status
                    );
                }


                return response.json();

            })

            .then(function (data) {

                console.log(
                    "CREATE ORDER RESPONSE:",
                    data
                );


                if (data.error) {

                    paypalError.textContent =
                        data.error;

                    throw new Error(
                        data.error
                    );
                }


                if (!data.id) {

                    throw new Error(
                        "PayPal did not return an order ID."
                    );
                }


                console.log(
                    "PAYPAL ORDER ID:",
                    data.id
                );


                return data.id;

            })

            .catch(function (error) {

                console.error(
                    "CREATE ORDER ERROR:",
                    error
                );

                paypalError.textContent =
                    error.message ||
                    "Unable to create PayPal order.";

                throw error;

            });

        },


        // ======================================
        // PAYMENT APPROVED
        // ======================================

        onApprove: function (data) {

            console.log(
                "PAYPAL APPROVED"
            );

            console.log(
                "ORDER ID:",
                data.orderID
            );


            return fetch(
                "{% url 'paypal_capture_order' session.id %}",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json",

                        "X-CSRFToken":
                            "{{ csrf_token }}"
                    },

                    body: JSON.stringify({
                        orderID:
                            data.orderID
                    })
                }
            )

            .then(function (response) {

                console.log(
                    "Capture HTTP status:",
                    response.status
                );


                if (!response.ok) {

                    throw new Error(
                        "Capture request failed: HTTP " +
                        response.status
                    );
                }


                return response.json();

            })

            .then(function (result) {

                console.log(
                    "CAPTURE RESPONSE:",
                    result
                );


                if (result.success) {

                    window.location.href =
                        result.redirect_url;

                    return;
                }


                paypalError.textContent =
                    result.error ||
                    "Payment capture failed.";

            })

            .catch(function (error) {

                console.error(
                    "CAPTURE ERROR:",
                    error
                );

                paypalError.textContent =
                    error.message ||
                    "There was a problem completing your payment.";

            });

        },


        // ======================================
        // PAYMENT CANCELLED
        // ======================================

        onCancel: function () {

            console.log(
                "PAYPAL PAYMENT CANCELLED"
            );

        },


        // ======================================
        // PAYPAL ERROR
        // ======================================

        onError: function (error) {

            console.error(
                "PAYPAL ERROR:",
                error
            );

            paypalError.textContent =
                "PayPal encountered an error. Please try again.";

        }

    }).render(
        "#paypal-button-container"
    );

});