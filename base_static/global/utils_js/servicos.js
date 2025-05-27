document.addEventListener('DOMContentLoaded', function () {
    // Navegação entre seções
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section');

    // Mostrar a seção inicial (home)
    showSection('home');

    // Adicionar eventos aos links de navegação
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const sectionId = this.getAttribute('data-section');
            showSection(sectionId);

            // Atualizar navegação ativa
            navLinks.forEach(navLink => navLink.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Função para mostrar a seção selecionada
    function showSection(sectionId) {
        sections.forEach(section => {
            section.classList.toggle('section-active', section.id === sectionId);
        });
    }

    // Sistema de busca
    const searchInputs = document.querySelectorAll('.search-box input');
    searchInputs.forEach(input => {
        input.addEventListener('input', debounce(function () {
            const searchTerm = this.value.trim().toLowerCase();
            const cards = this.closest('section').querySelectorAll('.profile-card');

            cards.forEach(card => {
                const name = card.querySelector('.card-name')?.textContent.toLowerCase() || '';
                const bio = card.querySelector('.card-bio')?.textContent.toLowerCase() || '';
                const skills = Array.from(card.querySelectorAll('.skill-tag'))
                    .map(skill => skill.textContent.toLowerCase())
                    .join(' ');

                const isVisible = searchTerm === '' || 
                                 name.includes(searchTerm) || 
                                 bio.includes(searchTerm) || 
                                 skills.includes(searchTerm);
                card.style.display = isVisible ? 'block' : 'none';
            });
        }, 300));
    });

    // Sistema de filtros
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
        select.addEventListener('change', function () {
            const filterType = this.dataset.filterType || 'default';
            const filterValue = this.value;
            const container = this.closest('section').querySelector('.cards-container');

            // Aplica filtros
            const cards = container.querySelectorAll('.profile-card');
            cards.forEach(card => {
                const shouldShow = applyFilter(card, filterType, filterValue);
                card.style.display = shouldShow ? 'block' : 'none';
            });

            // Aplica ordenação se for um filtro de ordenação
            if (filterType === 'sort') {
                sortCards(container, filterValue);
            }
        });
    });

    // Função para aplicar os filtros
    function applyFilter(card, filterType, filterValue) {
        if (!filterValue || filterValue === 'all') return true;

        switch (filterType) {
            case 'category':
                return card.dataset.category === filterValue;

            case 'skill':
                const skills = Array.from(card.querySelectorAll('.skill-tag'))
                    .map(skill => skill.textContent.toLowerCase());
                return skills.includes(filterValue.toLowerCase());

            case 'availability':
                return card.dataset.availability === filterValue;

            case 'rating':
                const rating = parseFloat(card.dataset.rating);
                return rating >= parseFloat(filterValue);

            default:
                return true;
        }
    }

    // Sistema de avaliação por estrelas
    const ratingElements = document.querySelectorAll('.card-rating');
    ratingElements.forEach(element => {
        const ratingText = element.textContent.replace(',', '.').trim();
        const ratingValue = parseFloat(ratingText);
        
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

        for (let i = 0; i < fullStars; i++) {
            starsHTML += '<span class="star full" aria-hidden="true">★</span>';
        }
        
        if (hasHalfStar) {
            starsHTML += '<span class="star half" aria-hidden="true">★</span>';
        }
        
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
        for (let i = 0; i < emptyStars; i++) {
            starsHTML += '<span class="star empty" aria-hidden="true">★</span>';
        }
        
        return starsHTML;
    }

    // Função para ordenar os cards
    function sortCards(container, sortType) {
        const cards = Array.from(container.querySelectorAll('.profile-card:not([style*="display: none"])'));

        cards.sort((a, b) => {
            switch (sortType) {
                case 'rating-desc':
                    return parseFloat(b.dataset.rating) - parseFloat(a.dataset.rating);

                case 'rating-asc':
                    return parseFloat(a.dataset.rating) - parseFloat(b.dataset.rating);

                case 'availability-desc':
                    return a.dataset.availability.localeCompare(b.dataset.availability);

                case 'availability-asc':
                    return b.dataset.availability.localeCompare(a.dataset.availability);

                default:
                    return 0;
            }
        });

        cards.forEach(card => container.appendChild(card));
    }

    // Botões de contato
    const contactButtons = document.querySelectorAll('.card-button');
    contactButtons.forEach(button => {
        button.addEventListener('click', function () {
            const card = this.closest('.profile-card');
            const name = card.querySelector('.card-name')?.textContent || 'este profissional';
            alert(`Você está entrando em contato com ${name}. Em breve eles responderão sua solicitação!`);
        });
    });

    // Animação ao rolar a página
    window.addEventListener('scroll', debounce(() => {
        document.querySelectorAll('.animate-on-scroll').forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            element.classList.toggle('visible', elementPosition < screenPosition);
        });
    }, 100));

    // Inicializar elementos animados
    document.querySelectorAll('.animate-on-scroll').forEach(element => {
        element.classList.add('animate-on-scroll-init');
    });

    // Debounce helper
    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
});