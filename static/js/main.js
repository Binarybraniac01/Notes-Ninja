document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('examForm');
    const submitBtn = document.getElementById('submitBtn');
    const spinner = submitBtn.querySelector('.spinner-border');
    const toastError = document.getElementById('toastError');
    const toast = new bootstrap.Toast(toastError);
    const imagePreview = document.getElementById('imagePreview');
    const MAX_FILE_SIZE = 16; // MB

    form.addEventListener('submit', function(e) {
        // Show loading state
        submitBtn.disabled = true;
        spinner.classList.remove('d-none');

        // Form submission is handled normally since we want to download the file
        // But we'll add a timeout to reset the button state
        setTimeout(() => {
            submitBtn.disabled = false;
            spinner.classList.add('d-none');
        }, 5000);
    });

    // File input validation and preview
    document.getElementById('files').addEventListener('change', function(e) {
        imagePreview.innerHTML = ''; // Clear existing previews
        let hasError = false;

        Array.from(e.target.files).forEach(file => {
            const fileSize = file.size / 1024 / 1024; // in MB
            if (fileSize > MAX_FILE_SIZE) {
                hasError = true;
                return;
            }

            // Create preview
            const col = document.createElement('div');
            col.className = 'col-md-4 col-sm-6';

            const card = document.createElement('div');
            card.className = 'card h-100';

            const img = document.createElement('img');
            img.className = 'card-img-top';
            img.style.objectFit = 'cover';
            img.style.height = '200px';

            // Read and display image
            const reader = new FileReader();
            reader.onload = function(e) {
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);

            const cardBody = document.createElement('div');
            cardBody.className = 'card-body';
            cardBody.innerHTML = `<p class="card-text small">${file.name}</p>`;

            card.appendChild(img);
            card.appendChild(cardBody);
            col.appendChild(card);
            imagePreview.appendChild(col);
        });

        if (hasError) {
            toast.show();
            e.target.value = '';
            imagePreview.innerHTML = '';
        }
    });
});


var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})