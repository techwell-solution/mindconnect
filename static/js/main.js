console.log("main.js is loaded");

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded");

    // Mobile Navigation
    const toggle = document.querySelector(".menu-toggle");
    const mobileMenu = document.querySelector(".mobile-menu");

    if (toggle && mobileMenu) {
        toggle.addEventListener("click", () => {
            mobileMenu.classList.toggle("show");
        });
}
    // Sticky Header
    const header = document.querySelector("header");

    if (header) {
        window.addEventListener("scroll", () => {
            header.classList.toggle("sticky", window.scrollY > 50);
        });
    }

    // ...keep the rest of your existing code here...
});
    // ==========================
    // Mobile Navigation
    // ==========================

    // ==========================
    // Sticky Header
    // ==========================
    const header = document.querySelector("header");

    if (header) {
        window.addEventListener("scroll", () => {
            header.classList.toggle("sticky", window.scrollY > 50);
        });
    }

    // ==========================
    // Smooth Scrolling
    // ==========================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {
                e.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth"
                });
            }
        });
    });

    // ==========================
    // Scroll Animation
    // ==========================
    const hiddenElements = document.querySelectorAll(".hidden");

    const observer = new IntersectionObserver(entries => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }

        });

    });

    hiddenElements.forEach(el => observer.observe(el));

    // ==========================
    // Auto-hide Messages
    // ==========================
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {

        setTimeout(() => {

            alert.style.opacity = "0";

            setTimeout(() => {
                alert.remove();
            }, 500);

        }, 4000);

    });

    // ==========================
    // Back to Top Button
    // ==========================
    const backToTop = document.querySelector("#backToTop");

    if (backToTop) {

        window.addEventListener("scroll", () => {

            if (window.scrollY > 300) {
                backToTop.classList.add("show");
            } else {
                backToTop.classList.remove("show");
            }

        });

        backToTop.addEventListener("click", () => {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        });

    }

document.addEventListener("DOMContentLoaded", function () {

    const cards = document.querySelectorAll("#servicesGrid .service-card");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const pageInfo = document.getElementById("pageInfo");

    const cardsPerPage = 3;
    let currentPage = 1;

    const totalPages = Math.ceil(cards.length / cardsPerPage);


    function showPage(page) {

        const start = (page - 1) * cardsPerPage;
        const end = start + cardsPerPage;

        cards.forEach((card, index) => {

            if (index >= start && index < end) {
                card.style.display = "flex";
            } else {
                card.style.display = "none";
            }

        });


        pageInfo.textContent = `Page ${page} of ${totalPages}`;

        prevBtn.disabled = page === 1;
        nextBtn.disabled = page === totalPages;
    }


    nextBtn.addEventListener("click", function () {

        if (currentPage < totalPages) {
            currentPage++;
            showPage(currentPage);
        }

    });


    prevBtn.addEventListener("click", function () {

        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
        }

    });


    showPage(currentPage);

});


      