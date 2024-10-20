// Phone number validation for Kenyan numbers
document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.querySelector('input[name="phone_number"]');
    if (!phoneInput) return;
    
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = 'invalid-feedback';
    feedbackDiv.style.fontWeight = '600';
    feedbackDiv.style.fontSize = '0.81rem';
    phoneInput.parentNode.appendChild(feedbackDiv);

    // Style for valid/invalid states
    const setValidationState = (isValid, message) => {
        phoneInput.classList.remove('is-valid', 'is-invalid');
        phoneInput.classList.add(isValid ? 'is-valid' : 'is-invalid');
        feedbackDiv.textContent = message;
        if (!isValid) {
            feedbackDiv.style.animation = 'shake 0.5s';
            setTimeout(() => feedbackDiv.style.animation = '', 500);
        }
    };

    // Add CSS animation for shake effect
    const style = document.createElement('style');
    style.textContent = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-4px); }
            75% { transform: translateX(4px); }
        }
        .invalid-feedback {
            display: block;
            margin-top: 0.25rem;
            color: #dc3545;
        }
    `;
    document.head.appendChild(style);

    // Validate phone number format
    const validatePhoneNumber = (phone) => {
        // First check: Only allow digits
        if (/[^0-9\s]/.test(phone)) {
            return { isValid: false, message: '⚠️ Phone number should only contain digits' };
        }

        // Remove all non-digit characters for processing
        const cleanPhone = phone.replace(/\D/g, '');
        
        // Check length requirements first
        if (cleanPhone.length === 0) {
            return { isValid: false, message: '⚠️ Phone number is required' };
        }

        if (cleanPhone.length < 10) {
            return { isValid: false, message: '⚠️ Phone number must be at least 10 digits' };
        }

        if (cleanPhone.length > 12) {
            return { isValid: false, message: '⚠️ Phone number cannot exceed 12 digits' };
        }

        // Updated patterns for Kenyan numbers
        const patterns = {
            // Safaricom: 0720-0729, 0740-0749, 0790-0799, (+254)7...
            safaricom: /^(?:254|0)(7(?:(?:[01][0-9])|(?:2[0-9])|(?:4[0-9])|(?:5[0-9])|(?:6[0-9])|(?:7[0-9])|(?:9[0-9]))[0-9]{6})$/,
            
            // Airtel: 0730-0739, 0750-0759, 0110-0119, (+254)7... (+254)1...
            airtel: /^(?:254|0)(7(?:3[0-9]|5[0-9]|6[0-2])|1(?:1[0-9]|2[0-9]))[0-9]{6}$/,
        };

        // Test if it matches any valid pattern
        if (patterns.safaricom.test(cleanPhone)) {
            return { isValid: true, message: '✓ Valid number' };
        }
        if (patterns.airtel.test(cleanPhone)) {
            return { isValid: true, message: '✓ Valid number' };
        }

        return { isValid: false, message: '⚠️ Please enter a valid phone number' };
    };

    // Format phone number as user types
    const formatPhoneNumber = (phone) => {
        // Only allow digits
        let cleaned = phone.replace(/[^0-9]/g, '');
        
        // Handle different formats based on input length
        if (cleaned.startsWith('254')) {
            cleaned = cleaned.slice(3);
        }
        if (!cleaned.startsWith('0') && cleaned.length > 0) {
            cleaned = '0' + cleaned;
        }
        
        // Format: 0XXX XXX XXX
        if (cleaned.length > 0) {
            let parts = [];
            parts.push(cleaned.slice(0, 4));
            if (cleaned.length > 4) parts.push(cleaned.slice(4, 7));
            if (cleaned.length > 7) parts.push(cleaned.slice(7, 10));
            return parts.join(' ').trim();
        }
        return cleaned;
    };

    // Prevent non-digit input
    phoneInput.addEventListener('keypress', function(e) {
        if (!/[\d\s]/.test(e.key) && e.key !== 'Backspace' && e.key !== 'Delete' && e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') {
            e.preventDefault();
        }
    });

    // Handle paste events to strip non-digits
    phoneInput.addEventListener('paste', function(e) {
        e.preventDefault();
        const pastedText = (e.clipboardData || window.clipboardData).getData('text');
        const cleanedText = pastedText.replace(/[^0-9]/g, '');
        const formatted = formatPhoneNumber(cleanedText);
        phoneInput.value = formatted;
        const validation = validatePhoneNumber(formatted);
        setValidationState(validation.isValid, validation.message);
    });

    // Event listeners
    phoneInput.addEventListener('input', function(e) {
        // Format the number
        const formatted = formatPhoneNumber(e.target.value);
        e.target.value = formatted;

        // Validate and show feedback
        const validation = validatePhoneNumber(formatted);
        setValidationState(validation.isValid, validation.message);
    });

    // Validate on form submission
    const form = phoneInput.closest('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const validation = validatePhoneNumber(phoneInput.value);
            if (!validation.isValid) {
                e.preventDefault();
                setValidationState(false, validation.message);
                phoneInput.focus();
            }
        });
    }
});
