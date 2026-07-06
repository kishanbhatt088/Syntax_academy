/**
 * Syntax Academy - Global Validation System
 * Handles client-side validation, password strength, and real-time feedback.
 */

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Password Match Validation
    const password = document.getElementById('id_password1') || document.getElementById('id_new_password1');
    const confirmPassword = document.getElementById('id_password2') || document.getElementById('id_new_password2');

    if (password && confirmPassword) {
        const validatePassword = () => {
            if (password.value !== confirmPassword.value) {
                confirmPassword.setCustomValidity("Passwords don't match");
            } else {
                confirmPassword.setCustomValidity('');
            }
        };

        password.addEventListener('change', validatePassword);
        confirmPassword.addEventListener('keyup', validatePassword);
    }

    // Password Strength Meter
    if (password) {
        const strengthDiv = document.createElement('div');
        strengthDiv.className = 'password-strength mt-1';
        strengthDiv.style.height = '4px';
        strengthDiv.style.borderRadius = '2px';
        strengthDiv.style.transition = 'all 0.3s ease';
        password.parentNode.appendChild(strengthDiv);

        password.addEventListener('input', function() {
            const val = password.value;
            let strength = 0;
            if (val.length >= 8) strength++;
            if (val.match(/[a-z]/) && val.match(/[A-Z]/)) strength++;
            if (val.match(/[0-9]/)) strength++;
            if (val.match(/[^a-zA-Z0-9]/)) strength++;

            const colors = ['#dc3545', '#ffc107', '#0dcaf0', '#198754'];
            const widths = ['25%', '50%', '75%', '100%'];

            if (val.length === 0) {
                strengthDiv.style.width = '0';
            } else {
                strengthDiv.style.width = widths[strength - 1] || '10%';
                strengthDiv.style.backgroundColor = colors[strength - 1] || '#dc3545';
            }
        });
    }

    // Phone Number Formatting (Digits only)
    const phoneInput = document.querySelector('input[name="phone"]');
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9+\-() ]/g, '');
        });
    }

    // Slug Auto-generation (for Admin forms)
    const titleInput = document.querySelector('input[name="title"]') || document.querySelector('input[name="name"]');
    const slugInput = document.querySelector('input[name="slug"]');

    if (titleInput && slugInput && !slugInput.value) {
        titleInput.addEventListener('input', function() {
            slugInput.value = titleInput.value
                .toLowerCase()
                .replace(/[^\w ]+/g, '')
                .replace(/ +/g, '-');
        });
    }
});
