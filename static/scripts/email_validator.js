// Email validation
document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.querySelector('input[name="email"]');
    if (!emailInput) return;
    
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = 'invalid-feedback';
    feedbackDiv.style.fontWeight = '600';
    feedbackDiv.style.fontSize = '0.81rem';
    emailInput.parentNode.appendChild(feedbackDiv);

    // Style for valid/invalid states
    const setValidationState = (isValid, message) => {
        emailInput.classList.remove('is-valid', 'is-invalid');
        emailInput.classList.add(isValid ? 'is-valid' : 'is-invalid');
        feedbackDiv.textContent = message;
        if (!isValid) {
            feedbackDiv.style.animation = 'shake 0.5s';
            setTimeout(() => feedbackDiv.style.animation = '', 500);
        }
    };

    const validateEmail = (email) => {
        if (email.length === 0) {
            return { isValid: false, message: '⚠️ Email address is required' };
        }

        // Basic email format validation
        const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        
        if (!emailRegex.test(email)) {
            return { isValid: false, message: '⚠️ Please enter a valid email address' };
        }

        // Additional checks
        if (email.length > 255) {
            return { isValid: false, message: '⚠️ Email address is too long' };
        }

        return { isValid: true, message: '✓ Valid email address' };
    };

    // Event listeners
    emailInput.addEventListener('input', function(e) {
        const validation = validateEmail(e.target.value);
        setValidationState(validation.isValid, validation.message);
    });

    // Validate on form submission
    const form = emailInput.closest('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const validation = validateEmail(emailInput.value);
            if (!validation.isValid) {
                e.preventDefault();
                setValidationState(false, validation.message);
                emailInput.focus();
            }
        });
    }
});
