var image_data; // Declare a global variable to store image data

document.getElementById('uploadArea').addEventListener('dragover', function (e) {
    e.preventDefault();
    e.stopPropagation();
}, false);

document.getElementById('uploadArea').addEventListener('drop', function (e) {
    e.preventDefault();
    e.stopPropagation();
    var files = e.dataTransfer.files;
    handleFiles(files);
}, false);

document.getElementById('browse-files').addEventListener('click', function (e) {
    document.getElementById('fileElem').click();
}, false);

document.getElementById('fileElem').addEventListener('change', function (e) {
    var files = e.target.files;
    handleFiles(files);
}, false);

function handleFiles(files) {
    if (files.length > 0) {
        var reader = new FileReader();

        reader.onload = function (e) {
            const uploadedArea = document.getElementById('uploadArea');
            const browseFilesButton = document.getElementById('browse-files');

            var uploadedImage = document.getElementById('uploadedImage');
            uploadedArea.style.backgroundImage = `url('${e.target.result}')`;
            uploadedArea.style.backgroundSize = 'cover';
            uploadedArea.style.backgroundPosition = 'center';

            var uploadInstruction = document.querySelector('.upload-instruction');
            uploadInstruction.style.display = 'none';

            // Adjusting browseFilesButton to move below the image
            browseFilesButton.style.position = 'relative';
            browseFilesButton.style.top = '82%';
            browseFilesButton.style.left = '-40%';
            browseFilesButton.innerText = 'Re-Upload Image';

            var resnetButton = document.getElementById('resnet');
            resnetButton.style.position = 'relative';
            resnetButton.style.left = '6.5%';

            uploadedArea.innerHTML = uploadedImage.outerHTML + browseFilesButton.outerHTML;

            // Displaying the image and the browseFilesButton inside the uploadArea
            uploadedArea.innerHTML = '';
            uploadedArea.appendChild(uploadedImage);
            uploadedArea.appendChild(browseFilesButton);

            // Update the global image_data variable
            image_data = e.target.result;
        };

        reader.readAsDataURL(files[0]);
    }
}

document.getElementById('resnet').addEventListener('click', function () {

    if (typeof image_data !== 'undefined') {
        console.log(image_data)
        console.log(encodeURIComponent(image_data))

        fetch('/resnet_predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            // body: `image=${image_data}`,
            body: `image=${encodeURIComponent(image_data)}`,

        })
            .then(response => response.json())
            .then(data => {

                console.log('Server Response:', data);

                const uploadedArea = document.getElementById('uploadArea');
                const prediction = data.prediction;
                const browseFilesButton = document.getElementById('browse-files');

                // Style for the uploadedArea to set the image as background and opacity
                uploadedArea.style.backgroundImage = `url('${image_data}')`;
                uploadedArea.style.backgroundSize = '40%';
                uploadedArea.style.backgroundRepeat = 'no-repeat';
                uploadedArea.style.backgroundPosition = 'top';

                // Display prediction text on top of the background image
                const predictionHTML = `
                    <p style="
                        font-size: 18px;
                        color: #ddffdf;
                        position: absolute;
                        top: 50%;
                        bottom: 90%;
                        left: 50%;
                        width: 90%;
                        height: auto;
                        text-align: center;
                        transform: translate(-50%, -50%);
                        z-index: 1;
                    ">
                        ${prediction}
                    </p>`;

                // Clear the uploadedArea content and append the prediction
                uploadedArea.innerHTML = '';
                uploadedArea.innerHTML = predictionHTML;
                uploadedArea.appendChild(browseFilesButton);

                // Update button text and style
                browseFilesButton.innerText = 'Browse Files';
                browseFilesButton.style.marginTop = '7.75%';
                browseFilesButton.style.right = '2.25%';

                // Adjust button position
                var resnetButton = document.getElementById('resnet');
                resnetButton.style.position = 'relative';
                resnetButton.style.left = '5%';
                resnetButton.style.top = '1.125%';
            })

            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        console.error('Image data is not defined.');
    }
});

