// Elementos do DOM
    document.addEventListener('DOMContentLoaded', () => {
    const emailInput = document.getElementById('email');
    const sendCodeBtn = document.getElementById('send-code-btn');
    const verificationCodeInput = document.getElementById('verification-code');
    const verifyCodeBtn = document.getElementById('verify-code-btn');
    const newPasswordInput = document.getElementById('new-password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const submitNewPasswordBtn = document.getElementById('submit-new-password');
    const resendCodeLink = document.getElementById('resend-code');
    const emailDisplay = document.getElementById('email-display');
    const messageDiv = document.getElementById('message');
    const passwordStrengthBar = document.getElementById('password-strength-bar');

    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const step3 = document.getElementById('step3');
    const step1Indicator = document.getElementById('step1-indicator');
    const step2Indicator = document.getElementById('step2-indicator');
    const step3Indicator = document.getElementById('step3-indicator');

    let currentStep = 1;
    let userEmail = '';
    let verificationCode = '';

    function showMessage(text, type) {
        messageDiv.textContent = text;
        messageDiv.className = 'message ' + type + '-message';
        messageDiv.style.display = 'block';

        if (type !== 'error') {
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 5000);
        }
    }

    function isValidCorporateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email) && !email.endsWith('@gmail.com') && !email.endsWith('@yahoo.com') && !email.endsWith('@hotmail.com');
    }

    function generateRandomCode() {
        return Math.floor(100000 + Math.random() * 900000).toString();
    }

    function goToStep(step) {
        document.querySelectorAll('.form-step').forEach(el => el.classList.remove('active'));
        document.querySelectorAll('.step').forEach(el => {
            el.classList.remove('active', 'completed');
        });

        if (step > 1) {
            step1Indicator.classList.add('completed');
        }
        if (step > 2) {
            step2Indicator.classList.add('completed');
        }

        if (step === 1) {
            step1.classList.add('active');
            step1Indicator.classList.add('active');
        } else if (step === 2) {
            step2.classList.add('active');
            step2Indicator.classList.add('active');
        } else if (step === 3) {
            step3.classList.add('active');
            step3Indicator.classList.add('active');
        }

        currentStep = step;
    }

    function checkPasswordStrength(password) {
        let strength = 0;

        if (password.length >= 8) strength += 1;
        if (password.match(/[a-z]/)) strength += 1;
        if (password.match(/[A-Z]/)) strength += 1;
        if (password.match(/[0-9]/)) strength += 1;
        if (password.match(/[^a-zA-Z0-9]/)) strength += 1;

        return strength;
    }

    sendCodeBtn.addEventListener('click', function() {
        const email = emailInput.value.trim();

        if (!isValidCorporateEmail(email)) {
            showMessage('Por favor, insira um e-mail corporativo válido.', 'error');
            return;
        }

        userEmail = email;
        verificationCode = generateRandomCode();

        showMessage(`Código de verificação enviado para ${email}. Use: ${verificationCode}`, 'info');

        emailDisplay.textContent = email;

        goToStep(2);
    });

    verifyCodeBtn.addEventListener('click', function() {
        const code = verificationCodeInput.value.trim();

        if (code !== verificationCode) {
            showMessage('Código inválido. Por favor, tente novamente.', 'error');
            return;
        }

        showMessage('Código verificado com sucesso!', 'success');
        goToStep(3);
    });

    resendCodeLink.addEventListener('click', function(e) {
        e.preventDefault();

        verificationCode = generateRandomCode();
        showMessage(`Novo código enviado para ${userEmail}. Use: ${verificationCode}`, 'info');
    });

    newPasswordInput.addEventListener('input', function() {
        const password = newPasswordInput.value;
        const strength = checkPasswordStrength(password);

        let width = 0;
        let color = '#e74c3c';

        if (strength >= 4) {
            width = 100;
            color = '#27ae60';
        } else if (strength >= 2) {
            width = 50;
            color = '#f39c12';
        } else if (password.length > 0) {
            width = 20;
        }

        passwordStrengthBar.style.width = width + '%';
        passwordStrengthBar.style.backgroundColor = color;
    });

    submitNewPasswordBtn.addEventListener('click', function() {
        const newPassword = newPasswordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (newPassword.length < 8) {
            showMessage('A senha deve ter pelo menos 8 caracteres.', 'error');
            return;
        }

        if (newPassword !== confirmPassword) {
            showMessage('As senhas não coincidem.', 'error');
            return;
        }

        showMessage('Senha redefinida com sucesso! Redirecionando...', 'success');

        setTimeout(() => {
            window.location.href = loginUrl;
        }, 2000);
    });
});
