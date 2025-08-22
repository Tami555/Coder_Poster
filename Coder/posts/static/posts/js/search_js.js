document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('btn_get_search');
    const searchInput = document.getElementById('search_line');
    const searchBlock = document.querySelector('.links_block.search');
    const categoryBlock = document.querySelector('.links_block.block_category');

    if (searchBtn && searchBlock && categoryBlock) {
        searchBtn.addEventListener('click', function() {
            // Получаем ширину блока категорий
            const categoryWidth = categoryBlock.offsetWidth;

            // Устанавливаем такую же ширину для поиска
            searchBlock.style.width = categoryWidth + 'px';

            // Переключаем классы
            searchBlock.classList.toggle('active');
            searchBtn.classList.toggle('active');

            // Фокусируемся на input при открытии
            if (searchBlock.classList.contains('active')) {
                setTimeout(() => {
                    searchInput.focus();
                }, 300);
            }
        });

        // Обработка нажатия Enter в поле поиска
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });

        // Функция выполнения поиска
        function performSearch() {
            const searchTerm = searchInput.value.trim();

            if (searchTerm) {
                // Кодируем поисковый запрос для URL
                const encodedSearchTerm = encodeURIComponent(searchTerm);

                // Формируем URL и перенаправляем
                const searchUrl = `/posts/search/${encodedSearchTerm}/`;
                window.location.href = searchUrl;

                // Очищаем поле и закрываем поиск (опционально)
                searchInput.value = '';
                searchBlock.classList.remove('active');
                searchBtn.classList.remove('active');
            }
        }

        // Закрытие по клику вне области
        document.addEventListener('click', function(e) {
            if (searchBlock.classList.contains('active') &&
                !searchBlock.contains(e.target) &&
                !searchBtn.contains(e.target)) {
                searchBlock.classList.remove('active');
                searchBtn.classList.remove('active');
            }
        });

        // Закрытие по ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && searchBlock.classList.contains('active')) {
                searchBlock.classList.remove('active');
                searchBtn.classList.remove('active');
            }
        });

        // Обновляем ширину при изменении размера окна
        window.addEventListener('resize', function() {
            if (searchBlock.classList.contains('active')) {
                const currentCategoryWidth = categoryBlock.offsetWidth;
                searchBlock.style.width = currentCategoryWidth + 'px';
            }
        });
    }
});