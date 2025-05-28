document.addEventListener('DOMContentLoaded', function() {
    const hasError = window.location.search.includes('error')
    if (hasError) {
        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        const loginError = document.getElementById('loginError');
    
        // apply red bord 
        usernameInput.style.borderColor = '#ef4444';
        passwordInput.style.borderColor = '#ef4444';

        // show error message
        loginError.classList.remove('hidden');

        // clear errors on input 
        function clearError() {
            usernameInput.style.borderColor = '';
            passwordInput.style.borderColor = '';
            loginError.classList.add('hidden');
        }
        usernameInput.addEventListener('input', clearError);
        passwordInput.addEventListener('input', clearError);
    }
});