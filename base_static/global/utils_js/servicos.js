document.addEventListener('DOMContentLoaded', () => {
    // Controle das avaliações
    const ratingElements = document.querySelectorAll('.card-rating');

    ratingElements.forEach(element => {
        const ratingValue = parseFloat(element.textContent.replace(',', '.').trim());

        if (!isNaN(ratingValue) && ratingValue >= 0 && ratingValue <= 5) {
            const starsContainer = document.createElement('div');
            starsContainer.className = 'rating-stars';
            starsContainer.innerHTML = createStars(ratingValue);
            element.innerHTML = '';
            element.appendChild(starsContainer);
            element.setAttribute('data-rating', ratingValue);
            element.setAttribute('aria-label', `Avaliação: ${ratingValue} de 5`);
        } else {
            console.warn('Valor de avaliação inválido:', element.textContent);
            element.classList.add('rating-error');
        }
    });

    function createStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        let starsHTML = '';

        starsHTML += '<span class="star full" aria-hidden="true">★</span>'.repeat(fullStars);
        if (hasHalfStar) {
            starsHTML += '<span class="star half" aria-hidden="true">★</span>';
        }
        starsHTML += '<span class="star empty" aria-hidden="true">★</span>'
            .repeat(5 - fullStars - (hasHalfStar ? 1 : 0));

        return starsHTML;
    }

    // Controle dos popups
    const hireButtons = document.querySelectorAll('.card-button');
    const popups = document.querySelectorAll('.popup-container');

    hireButtons.forEach((button, index) => {
        const popup = popups[index];
        const closeBtn = popup.querySelector('.close-btn');

        button.addEventListener('click', () => {
            popup.style.display = 'flex';
        });

        closeBtn.addEventListener('click', () => {
            popup.style.display = 'none';
        });

        popup.addEventListener('click', (e) => {
            if (e.target === popup) {
                popup.style.display = 'none';
            }
        });
    });
});
