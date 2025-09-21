document.addEventListener('DOMContentLoaded', function() {
    const reactionItems = document.querySelectorAll('.reaction-item');
    const csrfToken = document.getElementById('csrf-token').value;
    const postId = document.getElementById('post-id').value;
    const messageElement = document.getElementById('reaction-message');

    reactionItems.forEach(item => {
        item.addEventListener('click', function() {
            const reactionType = this.dataset.reaction;
            sendReaction(reactionType, this);
        });
    });

    function sendReaction(reactionType, element) {
        fetch('/posts/set_reaction/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                post_id: postId,
                reaction_type: reactionType
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateUI(data, element);
                playAnimation(element, reactionType);
                showMessage(data.message, 'success');
            } else {
                showMessage(data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Ошибка соединения', 'error');
        });
    }

    function updateUI(data, element) {
        // Обновляем счетчики
        document.getElementById('likes-count').textContent = data.likes_count;
        document.getElementById('dislikes-count').textContent = data.dislikes_count;

        // Убираем активный класс со всех элементов
        reactionItems.forEach(item => {
            item.classList.remove('active');
        });

        // Добавляем активный класс к выбранному элементу
        element.classList.add('active');
    }

    function playAnimation(element, reactionType) {
        if (reactionType === 'like') {
            playConfettiAnimation(element);
        } else {
            playExplosionAnimation(element);
        }
    }

    function playConfettiAnimation(element) {
        const confettiParticles = element.querySelectorAll('.confetti');

        confettiParticles.forEach(particle => {
            // Случайные начальные позиции и анимации
            const startX = Math.random() * 100;
            const startY = Math.random() * 100;
            const duration = Math.random() * 1000 + 500;
            const delay = Math.random() * 300;

            particle.style.left = startX + '%';
            particle.style.top = startY + '%';
            particle.style.animation = `confettiFall ${duration}ms ease-out ${delay}ms forwards`;

            // Сбрасываем анимацию после завершения
            setTimeout(() => {
                particle.style.animation = 'none';
            }, duration + delay);
        });
    }

    function playExplosionAnimation(element) {
        const explosionParticles = element.querySelectorAll('.explosion-particle');

        explosionParticles.forEach(particle => {
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.random() * 50 + 30;
            const tx = Math.cos(angle) * distance;
            const ty = Math.sin(angle) * distance;
            const duration = Math.random() * 500 + 300;

            particle.style.setProperty('--tx', tx + 'px');
            particle.style.setProperty('--ty', ty + 'px');
            particle.style.animation = `explosion ${duration}ms ease-out forwards`;

            setTimeout(() => {
                particle.style.animation = 'none';
            }, duration);
        });
    }

    function showMessage(text, type) {
        messageElement.textContent = text;
        messageElement.className = `reaction-message show ${type}`;

        setTimeout(() => {
            messageElement.classList.remove('show');
        }, 3000);
    }
});