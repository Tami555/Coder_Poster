document.addEventListener('DOMContentLoaded', function() {
    const subscribeBtn = document.querySelector('.subscribe-btn');
    const unsubscribeModal = document.getElementById('unsubscribe-modal');
    const authorNameSpan = document.getElementById('author-name');
    const cancelBtn = document.querySelector('.cancel-btn');
    const confirmBtn = document.querySelector('.confirm-btn');

    if (!subscribeBtn) return;

    let currentAuthorId = subscribeBtn.dataset.authorId;
    let currentAuthorName = subscribeBtn.dataset.authorName;
    let isSubscribed = subscribeBtn.classList.contains('subscribed');

    subscribeBtn.addEventListener('click', function() {
        if (isSubscribed) {
            // Показываем модальное окно для отписки
            showUnsubscribeModal();
        } else {
            // Подписываемся сразу
            subscribeToAuthor();
        }
    });

    function showUnsubscribeModal() {
        authorNameSpan.textContent = currentAuthorName;
        unsubscribeModal.style.display = 'block';
    }

    cancelBtn.addEventListener('click', function() {
        unsubscribeModal.style.display = 'none';
    });

    confirmBtn.addEventListener('click', function() {
        unsubscribeFromAuthor();
        unsubscribeModal.style.display = 'none';
    });

    function subscribeToAuthor() {
        const btnText = subscribeBtn.querySelector('.btn-text');
        const btnLoader = subscribeBtn.querySelector('.btn-loader');

        // Показываем лоадер
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        subscribeBtn.disabled = true;

        fetch('/users/toggle_subscription/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementById('csrf-token').value
            },
            body: JSON.stringify({
                author_id: currentAuthorId,
                action: 'subscribe'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Успешная подписка
                isSubscribed = true;
                subscribeBtn.classList.add('subscribed');
                btnText.textContent = 'Вы подписаны';
                playSubscribeAnimation();
//                showMessage('Вы успешно подписались!', 'success');
            } else {
                showMessage(data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Ошибка соединения. Возможно вы не авторизованы!', 'error');
        })
        .finally(() => {
            // Скрываем лоадер
            btnText.style.display = 'inline-block';
            btnLoader.style.display = 'none';
            subscribeBtn.disabled = false;
        });
    }

    function unsubscribeFromAuthor() {
        const btnText = subscribeBtn.querySelector('.btn-text');
        const btnLoader = subscribeBtn.querySelector('.btn-loader');

        // Показываем лоадер
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        subscribeBtn.disabled = true;

        fetch('/users/toggle_subscription/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementById('csrf-token').value
            },
            body: JSON.stringify({
                author_id: currentAuthorId,
                action: 'unsubscribe'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Успешная отписка
                isSubscribed = false;
                subscribeBtn.classList.remove('subscribed');
                btnText.textContent = 'Подписаться';
//                showMessage('Вы отписались', 'info');
            } else {
                showMessage(data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Ошибка соединения.\nВозможно вы не авторизованы!', 'error');
        })
        .finally(() => {
            // Скрываем лоадер
            btnText.style.display = 'inline-block';
            btnLoader.style.display = 'none';
            subscribeBtn.disabled = false;
        });
    }

    function playSubscribeAnimation() {
        const animationContainer = document.querySelector('.subscribe-animation');
        const particles = animationContainer.querySelectorAll('.animation-particle');

        particles.forEach(particle => {
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * 100 + 50;
            const tx = Math.cos(angle) * distance;
            const ty = Math.sin(angle) * distance;
            const duration = Math.random() * 1000 + 500;

            particle.style.setProperty('--tx', tx + 'px');
            particle.style.setProperty('--ty', ty + 'px');
            particle.style.animation = `particleFly ${duration}ms ease-out forwards`;

            setTimeout(() => {
                particle.style.animation = 'none';
            }, duration);
        });
    }

    function showMessage(text, type) {
        // Используем существующий элемент для сообщений или создаем новый
        const messageElement = document.getElementById('subscribe-message');
        messageElement.textContent = text;
        messageElement.className = `subscribe-message show ${type}`;

        setTimeout(() => {
            messageElement.classList.remove('show');
        }, 3000);
    }

    function createMessageElement() {
        const element = document.createElement('div');
        element.id = 'subscription-message';
        element.className = 'reaction-message';
        document.querySelector('.subscribe-section').appendChild(element);
        return element;
    }
});