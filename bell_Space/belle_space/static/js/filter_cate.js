
document.getElementById('category-select').addEventListener('change', function () {
    var categoryId = this.value;
    var serviceSelect = document.getElementById('service-select');

    // Clear existing options
    serviceSelect.innerHTML = '';

    if (categoryId) {
        fetch(`/get-services-by-category/${categoryId}/`)
            .then(response => response.json())
            .then(data => {
                data.services.forEach(service => {
                    var option = document.createElement('option');
                    option.value = service.id;
                    option.text = service.name;
                    serviceSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error:', error));
    }
});
