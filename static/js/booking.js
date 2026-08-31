document.addEventListener("DOMContentLoaded", function () {

    /* =====================================================
       FORM FIELDS
    ===================================================== */

    const counselor = document.getElementById("id_counselor");
    const sessionType = document.getElementById("id_session_type");
    const sessionMode = document.getElementById("id_session_mode");
    const preferredDate = document.getElementById("id_preferred_date");
    const preferredTime = document.getElementById("id_preferred_time");
    const duration = document.getElementById("id_duration_minutes");

    /* =====================================================
       SUMMARY ELEMENTS
    ===================================================== */

    const summaryCounselor =
        document.getElementById("summaryCounselor");

    const summarySessionType =
        document.getElementById("summarySessionType");

    const summaryMode =
        document.getElementById("summaryMode");

    const summaryDate =
        document.getElementById("summaryDate");

    const summaryTime =
        document.getElementById("summaryTime");

    const summaryDuration =
        document.getElementById("summaryDuration");


    /* =====================================================
       HELPER
       Get selected text from SELECT
    ===================================================== */

    function getSelectedText(selectElement) {

        if (!selectElement || selectElement.selectedIndex < 0) {
            return "Not selected";
        }

        const option =
            selectElement.options[selectElement.selectedIndex];

        if (!option || !option.value) {
            return "Not selected";
        }

        return option.text.trim();
    }


    /* =====================================================
       COUNSELLOR
    ===================================================== */

    function updateCounselor() {

        if (!summaryCounselor) {
            return;
        }

        summaryCounselor.textContent =
            getSelectedText(counselor);
    }


    /* =====================================================
       SESSION TYPE
    ===================================================== */

    function updateSessionType() {

        if (!summarySessionType) {
            return;
        }

        summarySessionType.textContent =
            getSelectedText(sessionType);
    }


    /* =====================================================
       SESSION MODE
    ===================================================== */

    function updateSessionMode() {

        if (!summaryMode) {
            return;
        }

        summaryMode.textContent =
            getSelectedText(sessionMode);
    }


    /* =====================================================
       DATE
    ===================================================== */

    function updateDate() {

        if (!summaryDate) {
            return;
        }

        if (!preferredDate || !preferredDate.value) {

            summaryDate.textContent =
                "Not selected";

            return;
        }

        const dateValue =
            preferredDate.value;

        const date =
            new Date(`${dateValue}T00:00:00`);

        if (isNaN(date.getTime())) {

            summaryDate.textContent =
                "Not selected";

            return;
        }

        summaryDate.textContent =
            date.toLocaleDateString(
                "en-US",
                {
                    weekday: "short",
                    month: "short",
                    day: "numeric",
                    year: "numeric"
                }
            );
    }


    /* =====================================================
       TIME
    ===================================================== */

    function updateTime() {

        if (!summaryTime) {
            return;
        }

        if (!preferredTime || !preferredTime.value) {

            summaryTime.textContent =
                "Not selected";

            return;
        }

        const timeValue =
            preferredTime.value;

        const [hours, minutes] =
            timeValue.split(":");

        const date =
            new Date();

        date.setHours(
            parseInt(hours),
            parseInt(minutes),
            0,
            0
        );

        summaryTime.textContent =
            date.toLocaleTimeString(
                "en-US",
                {
                    hour: "numeric",
                    minute: "2-digit"
                }
            );
    }


    /* =====================================================
       DURATION
    ===================================================== */

    function updateDuration() {

        if (!summaryDuration) {
            return;
        }

        if (!duration || !duration.value) {

            summaryDuration.textContent =
                "Not selected";

            return;
        }

        const minutes =
            parseInt(duration.value);

        if (isNaN(minutes)) {

            summaryDuration.textContent =
                "Not selected";

            return;
        }


        if (minutes < 60) {

            summaryDuration.textContent =
                `${minutes} minutes`;

            return;
        }


        if (minutes === 60) {

            summaryDuration.textContent =
                "1 hour";

            return;
        }


        const hours =
            Math.floor(minutes / 60);

        const remainingMinutes =
            minutes % 60;


        if (remainingMinutes === 0) {

            summaryDuration.textContent =
                `${hours} hours`;

        } else {

            summaryDuration.textContent =
                `${hours} hr ${remainingMinutes} min`;
        }
    }


    /* =====================================================
       PREVENT PAST DATES
    ===================================================== */

    function setMinimumDate() {

        if (!preferredDate) {
            return;
        }

        const today =
            new Date();

        const year =
            today.getFullYear();

        const month =
            String(today.getMonth() + 1)
                .padStart(2, "0");

        const day =
            String(today.getDate())
                .padStart(2, "0");

        const todayString =
            `${year}-${month}-${day}`;

        preferredDate.min =
            todayString;
    }


    /* =====================================================
       DATE VALIDATION
    ===================================================== */

    function validateDate() {

        if (!preferredDate ||
            !preferredDate.value) {

            return true;
        }

        const selectedDate =
            new Date(
                `${preferredDate.value}T00:00:00`
            );

        const today =
            new Date();

        today.setHours(0, 0, 0, 0);


        if (selectedDate < today) {

            preferredDate.setCustomValidity(
                "Please select a future date."
            );

            return false;
        }


        preferredDate.setCustomValidity("");

        return true;
    }


    /* =====================================================
       EVENT LISTENERS
    ===================================================== */

    if (counselor) {

        counselor.addEventListener(
            "change",
            updateCounselor
        );
    }


    if (sessionType) {

        sessionType.addEventListener(
            "change",
            updateSessionType
        );
    }


    if (sessionMode) {

        sessionMode.addEventListener(
            "change",
            updateSessionMode
        );
    }


    if (preferredDate) {

        preferredDate.addEventListener(
            "change",
            function () {

                validateDate();
                updateDate();

            }
        );
    }


    if (preferredTime) {

        preferredTime.addEventListener(
            "change",
            updateTime
        );
    }


    if (duration) {

        duration.addEventListener(
            "change",
            updateDuration
        );
    }


    /* =====================================================
       FORM SUBMISSION VALIDATION
    ===================================================== */

    const bookingForm =
        document.getElementById("bookingForm");

    if (bookingForm) {

        bookingForm.addEventListener(
            "submit",
            function (event) {

                if (!validateDate()) {

                    event.preventDefault();

                    preferredDate.reportValidity();

                    return;
                }

            }
        );
    }


    /* =====================================================
       INITIALIZE
    ===================================================== */

    setMinimumDate();

    updateCounselor();
    updateSessionType();
    updateSessionMode();
    updateDate();
    updateTime();
    updateDuration();

});