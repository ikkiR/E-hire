document.addEventListener('DOMContentLoaded', () => {
    const abasComPaginacao = ['#companies', '#providers'];
    const abaPadrao = '#home';

    const navLinks = document.querySelectorAll('.nav-link');
    const filterSelects = document.querySelectorAll('.filter-select');
    const ratingElements = document.querySelectorAll('.card-rating');
    const contactButtons = document.querySelectorAll('.card-button');
    const animElements = document.querySelectorAll('.animate-on-scroll');

    function getHash() {
        return window.location.hash || abaPadrao;
    }

    function getPage() {
        return new URLSearchParams(window.location.search).get('page') || '1';
    }

    function mostrarAba(hash) {
    document.querySelectorAll('section').forEach(section => {
        section.style.display = ('#' + section.id === hash) ? 'block' : 'none';
    });

    if (hash === '#home') {
        document.querySelectorAll('#home section').forEach(subsection => {
            subsection.style.display = 'block';
        });
    }

    navLinks.forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === hash);
    });
}

    function ajustarURLParaPagina(hash) {
        const url = new URL(window.location);
        if (abasComPaginacao.includes(hash)) {
            url.hash = hash;
        } else {
            url.hash = hash;
            url.searchParams.delete('page');
        }
        window.history.replaceState(null, null, url.toString());
    }

    function inicializar() {
        let hash = getHash();
        if (!['#home', '#companies', '#providers'].includes(hash)) {
            hash = abaPadrao;
            window.location.hash = hash;
        }
        ajustarURLParaPagina(hash);
        mostrarAba(hash);
    }

    navLinks.forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const hash = link.getAttribute('href');
            window.location.hash = hash;
            ajustarURLParaPagina(hash);
            mostrarAba(hash);
        });
    });

    window.addEventListener('hashchange', () => {
        const hash = getHash();
        ajustarURLParaPagina(hash);
        mostrarAba(hash);
    });

    inicializar();

    // --- Sistema de filtros ---
    filterSelects.forEach(select => {
        select.addEventListener('change', function () {
            const filterType = this.dataset.filterType || 'default';
            const filterValue = this.value;
            const container = this.closest('section')?.querySelector('.cards-container');
            if (!container) return;

            const cards = container.querySelectorAll('.profile-card');
            cards.forEach(card => {
                const shouldShow = applyFilter(card, filterType, filterValue);
                card.style.display = shouldShow ? 'block' : 'none';
            });

            if (filterType === 'sort') {
                sortCards(container, filterValue);
            }
        });
    });

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
                return parseFloat(card.dataset.rating) >= parseFloat(filterValue);
            default:
                return true;
        }
    }

    // --- Avaliação por estrelas ---
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

        starsHTML += '★'.repeat(fullStars).replace(/./g, '<span class="star full" aria-hidden="true">★</span>');
        if (hasHalfStar) starsHTML += '<span class="star half" aria-hidden="true">★</span>';
        starsHTML += '★'.repeat(5 - fullStars - (hasHalfStar ? 1 : 0))
            .replace(/./g, '<span class="star empty" aria-hidden="true">★</span>');
        return starsHTML;
    }

    function sortCards(container, sortType) {
        const cards = Array.from(container.querySelectorAll('.profile-card'))
            .filter(card => card.style.display !== 'none');

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

    // --- Botões de contato ---
    contactButtons.forEach(button => {
        button.addEventListener('click', function () {
            const name = this.closest('.profile-card')?.querySelector('.card-name')?.textContent || 'este profissional';
            alert(`Você está entrando em contato com ${name}. Em breve eles responderão sua solicitação!`);
        });
    });

    // --- Animação ao rolar ---
    window.addEventListener('scroll', debounce(() => {
        animElements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            element.classList.toggle('visible', elementPosition < screenPosition);
        });
    }, 100));

    animElements.forEach(element => {
        element.classList.add('animate-on-scroll-init');
    });

    // --- Função debounce ---
    function debounce(func, wait) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
});
