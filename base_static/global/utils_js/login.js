// Máscara para o CNPJ
document.getElementById('cnpj').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    
    if (value.length > 14) {
        value = value.substring(0, 14);
    }
    
    // Aplica a máscara
    if (value.length > 12) {
        value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2}).*/, '$1.$2.$3/$4-$5');
    } else if (value.length > 8) {
        value = value.replace(/^(\d{2})(\d{3})(\d{3})(\d{4}).*/, '$1.$2.$3/$4');
    } else if (value.length > 5) {
        value = value.replace(/^(\d{2})(\d{3})(\d{3}).*/, '$1.$2.$3');
    } else if (value.length > 2) {
        value = value.replace(/^(\d{2})(\d{3}).*/, '$1.$2');
    }
    
    e.target.value = value;
});

// Validação do formulário
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const cnpj = document.getElementById('cnpj').value;
    const password = document.getElementById('password').value;
    
    // Reset errors
    document.getElementById('cnpjError').style.display = 'none';
    document.getElementById('passwordError').style.display = 'none';
    
    // Validação simples do CNPJ (apenas formato)
    const cnpjRegex = /^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$/;
    if (!cnpjRegex.test(cnpj)) {
        document.getElementById('cnpjError').style.display = 'block';
        return;
    }
    
    // Efeito visual de carregamento
    const button = document.querySelector('.login-button');
    button.textContent = 'Acessando...';
    button.style.backgroundColor = '#2c3e50';
    
    // Simulação de verificação
    setTimeout(() => {
        console.log('CNPJ:', cnpj);
        console.log('Senha:', password);
        
        // Simulação de login bem-sucedido
        button.textContent = 'Acesso confirmado';
        button.style.backgroundColor = '#27ae60';
        
        setTimeout(() => {
            alert('Login realizado com sucesso! Redirecionando...');
            // window.location.href = 'dashboard.html'; // Redirecionamento real
        }, 500);
    }, 1500);
});

