// =========================================
// MOBILE MENU
// =========================================

document.addEventListener("DOMContentLoaded", function () {

    const menuToggle = document.getElementById("menu-toggle");
    const mobileMenu = document.querySelector(".mobile-menu");

    if (menuToggle && mobileMenu) {

        menuToggle.addEventListener("click", function (event) {
            event.stopPropagation();

            mobileMenu.classList.toggle("show");
        });

    }


    // =========================================
    // PROFILE DROPDOWN
    // =========================================

    window.toggleDropdown = function (event) {

        event.stopPropagation();

        const profileMenu = document.getElementById("profileMenu");

        if (profileMenu) {
            profileMenu.classList.toggle("show");
        }

    };


    // =========================================
    // CLOSE MENUS
    // =========================================

    document.addEventListener("click", function () {

        const profileMenu = document.getElementById("profileMenu");

        if (profileMenu) {
            profileMenu.classList.remove("show");
        }

        if (mobileMenu) {
            mobileMenu.classList.remove("show");
        }

    });

});