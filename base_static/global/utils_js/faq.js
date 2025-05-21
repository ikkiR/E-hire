document.addEventListener('DOMContentLoaded', function() {
    const questions = document.querySelectorAll('.faq-question');
    
    questions.forEach(question => {
        question.addEventListener('click', function() {
            // Toggle a classe 'active' na pergunta clicada
            this.classList.toggle('active');
            
            // Encontra a resposta correspondente
            const answer = this.nextElementSibling;
            
            // Alterna a classe 'show' na resposta
            answer.classList.toggle('show');
            
            // Fechar outras respostas abertas
            questions.forEach(q => {
                if (q !== question) {
                    q.classList.remove('active');
                    q.nextElementSibling.classList.remove('show');
                }
            });
        });
    });
});