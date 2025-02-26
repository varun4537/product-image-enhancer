document.getElementById('enhance-button').addEventListener('click', function () {
    const fileInput = document.getElementById('image-upload');
    const originalImage = document.getElementById('original-image');
    const enhancedImage = document.getElementById('enhanced-image');

    const attribute1 = document.getElementById('attribute1').value;
    const attribute2 = document.getElementById('attribute2').value;
    const attribute3 = document.getElementById('attribute3').value;

    if (fileInput.files && fileInput.files[0]) {
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('image', file);
        formData.append('attribute1', attribute1);
        formData.append('attribute2', attribute2);
        formData.append('attribute3', attribute3);

        // Display the original image
        const reader = new FileReader();
        reader.onload = function (e) {
            originalImage.src = e.target.result;
            originalImage.style.display = 'block';
        };
        reader.readAsDataURL(file);

        // Send the image and attributes to the backend for processing
        fetch('/enhance', {
            method: 'POST',
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                // Update the enhanced image source
                enhancedImage.src = data.enhanced_image_url;
                enhancedImage.style.display = 'block';
            })
            .catch((error) => console.error('Error:', error));
    }
});