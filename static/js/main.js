// Получение CSRF-токена из cookie
function getCsrfToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return decodeURIComponent(value);
    }
    return '';
}

// Показать кастомный премиальный Toast с сообщением
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const id = 'toast-' + Date.now();
    let accentColor = 'var(--accent)';
    let icon = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'; // info

    if (type === 'success') {
        accentColor = 'var(--success)';
        icon = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>';
    } else if (type === 'error' || type === 'danger' || type === 'warning') {
        accentColor = type === 'warning' ? 'var(--warning)' : 'var(--danger)';
        icon = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>';
    }

    container.insertAdjacentHTML('beforeend', `
        <div id="${id}" class="toast align-items-center border-0" role="alert" aria-live="assertive" style="background: rgba(30, 33, 48, 0.85); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08) !important; border-left: 4px solid ${accentColor} !important; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); color: #fff; margin-bottom: 10px; width: 350px; max-width: 100%;">
            <div class="d-flex align-items-center py-3 px-3">
                <span style="color: ${accentColor}; margin-right: 12px; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0;">${icon}</span>
                <div class="toast-body p-0" style="font-weight: 550; font-size: 13.5px; line-height: 1.4; color: #fff;">${message}</div>
                <button type="button" class="btn-close btn-close-white ms-auto" data-bs-dismiss="toast" aria-label="Close" style="opacity: 0.75; font-size: 11px; flex-shrink: 0;"></button>
            </div>
        </div>
    `);

    const toastEl = document.getElementById(id);
    const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
    toast.show();
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

// Загрузка товаров из API, динамический рендеринг и переключение видимости
function loadProducts(containerId, buttonElOrApiUrl, optionalApiUrl) {
    const container = document.getElementById(containerId);
    const spinner = document.getElementById('loading-spinner');
    
    let buttonEl = null;
    let apiUrl = '/api/products/';

    // Определяем типы аргументов для защиты от кэширования старой сигнатуры
    if (buttonElOrApiUrl instanceof HTMLElement) {
        buttonEl = buttonElOrApiUrl;
        if (typeof optionalApiUrl === 'string') {
            apiUrl = optionalApiUrl;
        }
    } else if (typeof buttonElOrApiUrl === 'string') {
        apiUrl = buttonElOrApiUrl;
    }

    const button = buttonEl || document.querySelector('[onclick^="loadProducts"]');

    if (!container) return;

    // Если контейнер заполнен и сейчас отображается, скрываем его
    if (container.innerHTML !== '' && container.style.display !== 'none') {
        container.style.display = 'none';
        if (button) button.textContent = 'Загрузить товары через API';
        if (spinner) spinner.style.display = 'none';
        return;
    }
    
    // Если контейнер заполнен, но скрыт, снова показываем его
    if (container.innerHTML !== '' && container.style.display === 'none') {
        container.style.display = 'grid';
        if (button) button.textContent = 'Скрыть API товары';
        return;
    }

    // Иначе выполняем запрос к API
    if (spinner) spinner.style.display = 'block';
    if (button) button.textContent = 'Загрузка...';
    container.innerHTML = '';

    fetch(apiUrl)
        .then(response => {
            if (response.status === 403 || response.status === 401) {
                throw new Error('Для загрузки товаров через API необходимо войти в аккаунт.');
            }
            if (!response.ok) throw new Error(`Ошибка сервера: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (spinner) spinner.style.display = 'none';

            const products = Array.isArray(data) ? data : (data.results || []);

            if (products.length === 0) {
                container.innerHTML = '<p class="text-muted">Товары не найдены.</p>';
                if (button) button.textContent = 'Загрузить товары через API';
                return;
            }

            container.innerHTML = '';
            container.style.display = 'grid';
            if (button) button.textContent = 'Скрыть API товары';

            products.forEach(product => {
                container.innerHTML += `
                    <div class="product-card" style="box-shadow: 0 10px 20px rgba(0,0,0,0.1); border-color: rgba(255, 255, 255, 0.04);">
                        <div class="product-card-body">
                            <div class="product-card-category">${product.category_name || ''}</div>
                            <div class="product-card-name">
                                <a href="/catalog/${product.id}/">${product.name}</a>
                            </div>
                            <div class="product-card-mfr">${product.manufacturer_name || ''}</div>
                        </div>
                    </div>`;
            });
        })
        .catch(error => {
            if (spinner) spinner.style.display = 'none';
            if (button) button.textContent = 'Загрузить товары через API';
            console.error('Ошибка загрузки товаров:', error);
            container.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-danger" style="margin: 0;">
                        ${error.message || 'Не удалось загрузить товары. Попробуйте обновить страницу.'}
                    </div>
                </div>`;
        });
}

// Добавление товара в корзину через API
function addToCart(productId, productName = 'Товар', quantity = 1) {
    fetch(`/cart/add/${productId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken(),
        },
        body: `quantity=${quantity}`,
    })
        .then(response => {
            if (response.redirected || response.ok) {
                showToast(`"${productName}" добавлен в корзину`, 'success');
            } else {
                throw new Error('Ошибка при добавлении');
            }
        })
        .catch(error => {
            console.error('Ошибка добавления в корзину:', error);
            showToast('Не удалось добавить товар в корзину', 'danger');
        });
}

// Делегирование кликов для всей карточки товара (за исключением интерактивных элементов)
document.addEventListener('DOMContentLoaded', () => {
    document.body.addEventListener('click', (e) => {
        const card = e.target.closest('.product-card');
        if (!card) return;

        // Если кликнули по кнопке, форме или ссылке внутри карточки — ничего не делаем
        if (e.target.closest('button') || e.target.closest('form') || e.target.closest('a')) {
            return;
        }

        // Ищем ссылку на детальную страницу товара и переходим по ней
        const link = card.querySelector('.product-card-img-link') || card.querySelector('.product-card-name a');
        if (link) {
            window.location.href = link.href;
        }
    });
});

