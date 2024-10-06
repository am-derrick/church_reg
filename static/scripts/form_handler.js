document.addEventListener('DOMContentLoaded', function() {
    const studentYes = document.getElementById('student_yes');
    const studentNo = document.getElementById('student_no');
    const additionalFields = document.getElementById('additionalFields');
    const occupationField = document.getElementById('occupationField');

    // Add event listeners to the radio buttons
    studentYes.addEventListener('click', function() {
        additionalFields.style.display = 'block'; // Show the additional fields when "Yes" is selected
        occupationField.style.display = 'none'; // Hide occupation when "Yes" is selected
    });

    studentNo.addEventListener('click', function() {
        additionalFields.style.display = 'none'; // Hide the additional fields when "No" is selected
        occupationField.style.display = 'block'; // Show occupation when "No" is selected
    });
});
