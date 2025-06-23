// Aguarda o carregamento completo do DOM
document.addEventListener('DOMContentLoaded', () => {
    // Configura o botão de logout
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            if (confirm('Deseja realmente sair do sistema?')) {
                window.location.href = 'login.html';
            }
        });
    }

    // Abrir modal ao clicar em qualquer botão "Selecionar Plano"
    const planButtons = document.querySelectorAll('.plan-button');
    const pixModal = document.getElementById('pixModal');
    const closePixModal = document.getElementById('closePixModal');

    if (planButtons && pixModal) {
        planButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                pixModal.style.display = 'flex';
            });
        });
    }

    // Fechar modal
    if (closePixModal) {
        closePixModal.addEventListener('click', () => {
            pixModal.style.display = 'none';
        });
    }

    // Fechar modal ao clicar fora dele
    window.addEventListener('click', (event) => {
        if (event.target === pixModal) {
            pixModal.style.display = 'none';
        }
    });
});