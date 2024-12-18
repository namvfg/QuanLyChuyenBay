document.querySelectorAll('.seat-toggle').forEach(button => {
            button.addEventListener('click', () => {
                button.classList.toggle('active');

            });
        });