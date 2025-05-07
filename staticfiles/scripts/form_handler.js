document.addEventListener('DOMContentLoaded', function() {
    const isStudentField = document.querySelector('input[name="is_student"][value="Yes"]');
    const studentFields = document.getElementById('studentFields');
    const occupationField = document.getElementById('occupationField');

    function toggleFields() {
        if (isStudentField.checked) {
            studentFields.style.display = 'block';
            occupationField.style.display = 'none';
        } else {
            studentFields.style.display = 'none';
            occupationField.style.display = 'block';
        }
    } 

    document.querySelectorAll('input[name="is_student"]').forEach(radio => {
        radio.addEventListener('change', toggleFields);
    });
    toggleFields();
});
