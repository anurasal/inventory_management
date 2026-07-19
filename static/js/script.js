// Confirm delete actions
document.addEventListener("DOMContentLoaded", function () {

    const deleteForms = document.querySelectorAll(".delete-form");

    deleteForms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            const confirmed = confirm(
                "Are you sure you want to delete this item?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });



    // Automatically hide flash messages

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.transition = "opacity 0.5s";

            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 500);

        }, 4000);

    });

});
