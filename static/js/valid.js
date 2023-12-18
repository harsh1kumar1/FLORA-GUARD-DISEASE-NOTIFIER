document.getElementById('fruitButton').addEventListener('click', function() {
    document.getElementById('modelType').value = 'fruit';
    document.getElementById('pageSelection').style.display = 'none';
    document.getElementById('fileSelection').style.display = 'block';
});

document.getElementById('vegetableButton').addEventListener('click', function() {
    document.getElementById('modelType').value = 'vegetable';
    document.getElementById('pageSelection').style.display = 'none';
    document.getElementById('fileSelection').style.display = 'block';
});

document.getElementById('chooseFileButton').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function() {
    const selectedFileName = document.getElementById('selectedFileName');
    selectedFileName.value = this.files[0].name;
});

document.querySelector('form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        const { prediction, recommendations, image_data } = result;

        document.getElementById('fileSelection').style.display = 'none';
        document.getElementById('result').style.display = 'block';
        document.getElementById('predictedCategory').textContent = `Predicted Category: ${prediction}`;

        const recommendationsList = document.getElementById('recommendations');
        recommendationsList.innerHTML = "";
        recommendations.forEach(recommendation => {
            const listItem = document.createElement('li');
            listItem.textContent = recommendation;
            recommendationsList.appendChild(listItem);
        });

        // Display the predicted image
        document.getElementById('predictedImage').src = `data:image/jpeg;base64,${image_data}`;

    } catch (error) {
        console.error('Error:', error);
    }
});

document.getElementById('goBack').addEventListener('click', function() {
    document.getElementById('result').style.display = 'none';
    document.getElementById('pageSelection').style.display = 'block';
    const predictedImage = document.getElementById('predictedImage');
    predictedImage.src = '/path/to/your/image.jpg?' + new Date().getTime();
    document.getElementById('fileInput').value = ''; // Clear the selected file
});
