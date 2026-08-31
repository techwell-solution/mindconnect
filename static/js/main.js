document.addEventListener("DOMContentLoaded", function () {

console.log("PAYPAL PAGE LOADED");


// ==========================================
// ELEMENTS
// ==========================================

const amountInput =
    document.getElementById("payment-amount");

const paypalContainer =
    document.getElementById("paypal-button-container");

const paypalError =
    document.getElementById("paypal-error");

const paystackForm =
    document.getElementById("paystack-form");

const paystackAmount =
    document.getElementById("paystack_amount");


// ==========================================
// PAYMENT CONFIGURATION
// ==========================================

const paypalCreateUrl =
    paypalContainer.dataset.createUrl;

const paypalCaptureUrl =
    paypalContainer.dataset.captureUrl;

const csrfToken =
    paypalContainer.dataset.csrf;


console.log(
    "PayPal create URL:",
    paypalCreateUrl
);

console.log(
    "PayPal capture URL:",
    paypalCaptureUrl
);


// ==========================================
// CHECK PAYPAL SDK
// ==========================================

console.log(
    "PayPal SDK:",
    typeof paypal
);


if (typeof paypal === "undefined") {

    console.error(
        "PAYPAL SDK NOT LOADED"
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
    // CREATE ORDER
    // ======================================

    createOrder: function () {

        const amount =
            amountInput.value;


        console.log(
            "AMOUNT ENTERED:",
            amount
        );


        if (
            !amount ||
            parseFloat(amount) <= 0
        ) {

            paypalError.textContent =
                "Please enter a valid payment amount.";

            return Promise.reject(
                new Error(
                    "Invalid payment amount."
                )
            );
        }


        const formData =
            new URLSearchParams();

        formData.append(
            "amount",
            amount
        );


        console.log(
            "CREATING PAYPAL ORDER..."
        );


        return fetch(
            paypalCreateUrl,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/x-www-form-urlencoded",

                    "X-CSRFToken":
                        csrfToken
                },

                body: formData
            }
        )

        .then(function (response) {

            console.log(
                "CREATE ORDER STATUS:",
                response.status
            );


            return response.text();

        })

        .then(function (text) {

            console.log(
                "CREATE ORDER RESPONSE:",
                text
            );


            let data;

            try {

                data =
                    JSON.parse(text);

            } catch (error) {

                throw new Error(
                    "Invalid response from server."
                );
            }


            if (!data.id) {

                throw new Error(
                    data.error ||
                    "PayPal order could not be created."
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
            "PAYPAL PAYMENT APPROVED"
        );

        console.log(
            "ORDER ID:",
            data.orderID
        );


        return fetch(
            paypalCaptureUrl,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",

                    "X-CSRFToken":
                        csrfToken
                },

                body: JSON.stringify({
                    orderID:
                        data.orderID
                })
            }
        )

        .then(function (response) {

            console.log(
                "CAPTURE STATUS:",
                response.status
            );


            return response.text();

        })

        .then(function (text) {

            console.log(
                "CAPTURE RESPONSE:",
                text
            );


            let result;

            try {

                result =
                    JSON.parse(text);

            } catch (error) {

                throw new Error(
                    "Invalid capture response from server."
                );
            }


            if (result.success) {

                window.location.href =
                    result.redirect_url;

                return;
            }


            throw new Error(
                result.error ||
                "Payment capture failed."
            );

        })

        .catch(function (error) {

            console.error(
                "CAPTURE ERROR:",
                error
            );


            paypalError.textContent =
                error.message ||
                "Payment capture failed.";

        });

    },


    // ======================================
    // CANCELLED
    // ======================================

    onCancel: function () {

        console.log(
            "PAYPAL PAYMENT CANCELLED"
        );

    },


    // ======================================
    // ERROR
    // ======================================

    onError: function (error) {

        console.error(
            "PAYPAL ERROR:",
            error
        );


        paypalError.textContent =
            "PayPal error: " +
            (
                error.message ||
                "Unknown PayPal error."
            );

    }

}).render(
    "#paypal-button-container"
);

});

document.addEventListener("DOMContentLoaded", function () {

    const cards = document.querySelectorAll(".service-card");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const pageInfo = document.getElementById("pageInfo");

    const cardsPerPage = 3;
    let currentPage = 1;

    const totalPages = Math.ceil(cards.length / cardsPerPage);

    function displayPage(page) {

        const start = (page - 1) * cardsPerPage;
        const end = start + cardsPerPage;

        cards.forEach((card, index) => {

            if (index >= start && index < end) {
                card.style.display = "";
            } else {
                card.style.display = "none";
            }

        });

        pageInfo.textContent = `Page ${page} of ${totalPages}`;

        prevBtn.disabled = page === 1;
        nextBtn.disabled = page === totalPages;
    }

    prevBtn.addEventListener("click", function () {

        if (currentPage > 1) {
            currentPage--;
            displayPage(currentPage);
        }

    });

    nextBtn.addEventListener("click", function () {

        if (currentPage < totalPages) {
            currentPage++;
            displayPage(currentPage);
        }

    });

    if (cards.length > 0) {
        displayPage(currentPage);
    } else {
        prevBtn.style.display = "none";
        nextBtn.style.display = "none";
        pageInfo.style.display = "none";
    }

});