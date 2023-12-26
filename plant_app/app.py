from flask import Flask, render_template, request, jsonify
from torchvision import transforms
from PIL import Image
import torch
import io
import base64

app = Flask(__name__)

# label_mapping = {
#     0: 'Peach_healthy',
#     1: 'Strawberry_leaf_scorch',
#     2: 'Grape_black_measles',
#     3: 'Tomato_septoria_leaf_spot',
#     4: 'Grape_healthy',
#     5: 'Tomato_healthy',
#     6: 'Peach_bacterial_spot',
#     7: 'Corn_gray_leaf_spot',
#     8: 'Soybean_healthy',
#     9: 'Corn_common_rust',
#     10: 'Blueberry_healthy',
#     11: 'Corn_healthy',
#     12: 'Apple_healthy',
#     13: 'Apple_cedar_apple_rust',
#     15: 'Tomato_target_spot',
#     16: 'Pepper_healthy',
#     17: 'Grape_black_rot',
#     18: 'Apple_scab',
#     19: 'Raspberry_healthy',
#     20: 'Tomato_early_blight',
#     21: 'Tomato_yellow_leaf_curl_virus',
#     22: 'Corn_northern_leaf_blight',
#     23: 'Potato_healthy',
#     24: 'Tomato_late_blight',
#     25: 'Cherry_powdery_mildew',
#     26: 'Grape_leaf_blight',
#     27: 'Tomato_leaf_mold',
#     28: 'Pepper_bacterial_spot',
#     29: 'Potato_late_blight',
#     30: 'Tomato_mosaic_virus',
#     31: 'Potato_early_blight',
#     32: 'Tomato_bacterial_spot',
#     33: 'Strawberry_healthy',
#     34: 'Cherry_healthy',
#     35: 'Squash_powdery_mildew',
#     36: 'Tomato_spider_mites_two-spotted_spider_mite',
#     37: 'Orange_haunglongbing',
#     38: 'Apple_black_rot'}

label_mapping = {
    0: "This is the leaf of a peach tree and it appears healthy.",
    1: "This is the leaf of a strawberry plant affected by leaf scorch. Water the plants adequately and ensure proper air circulation.",
    2: "This is the leaf of a grape plant affected by black measles. Prune infected parts and apply suitable fungicides.",
    3: "This is the leaf of a tomato plant with septoria leaf spot. Remove infected leaves, ensure proper air circulation, and avoid overhead watering.",
    4: "This is the leaf of a grape plant and it appears healthy.",
    5: "This is the leaf of a tomato plant and it appears healthy.",
    6: "This is the leaf of a peach tree affected by bacterial spot. Prune infected areas and apply copper-based fungicides.",
    7: "This is the leaf of a corn plant affected by gray leaf spot. Rotate crops and use disease-resistant varieties.",
    8: "This is the leaf of a soybean plant and it appears healthy.",
    9: "This is the leaf of a corn plant affected by common rust. Remove infected plants and use resistant varieties.",
    10: "This is the leaf of a blueberry plant and it appears healthy.",
    11: "This is the leaf of a corn plant and it appears healthy.",
    12: "This is the leaf of an apple tree and it appears healthy.",
    13: "This is the leaf of an apple tree affected by cedar apple rust. Prune affected areas and use fungicides.",
    15: "This is the leaf of a tomato plant affected by target spot. Remove infected leaves and use fungicides.",
    16: "This is the leaf of a pepper plant and it appears healthy.",
    17: "This is the leaf of a grape plant affected by black rot. Prune infected parts and apply suitable fungicides.",
    18: "This is the leaf of an apple tree affected by apple scab. Prune infected areas, apply fungicide in early spring, and maintain good airflow.",
    19: "This is the leaf of a raspberry plant and it appears healthy.",
    20: "This is the leaf of a tomato plant affected by early blight. Remove infected leaves, mulch the soil, and water at the base.",
    21: "This is the leaf of a tomato plant affected by yellow leaf curl virus. Remove infected plants and control whiteflies.",
    22: "This is the leaf of a corn plant affected by northern leaf blight. Rotate crops and use resistant varieties.",
    23: "This is the leaf of a potato plant and it appears healthy.",
    24: "This is the leaf of a tomato plant affected by late blight. Remove infected leaves and use copper-based fungicides.",
    25: "This is the leaf of a cherry tree affected by powdery mildew. Prune infected parts and use fungicides.",
    26: "This is the leaf of a grape plant affected by leaf blight. Prune infected parts and apply suitable fungicides.",
    27: "This is the leaf of a tomato plant affected by leaf mold. Remove infected leaves and ensure good airflow.",
    28: "This is the leaf of a pepper plant affected by bacterial spot. Remove infected leaves and use copper-based fungicides.",
    29: "This is the leaf of a potato plant affected by late blight. Remove infected foliage and use fungicides.",
    30: "This is the leaf of a tomato plant affected by mosaic virus. Remove infected plants and control insect vectors.",
    31: "This is the leaf of a potato plant affected by early blight. Remove infected leaves and use copper-based fungicides.",
    32: "This is the leaf of a tomato plant affected by bacterial spot. Remove infected leaves and use copper-based fungicides.",
    33: "This is the leaf of a strawberry plant and it appears healthy.",
    34: "This is the leaf of a cherry tree and it appears healthy.",
    35: "This is the leaf of a squash plant affected by powdery mildew. Remove infected leaves and improve airflow.",
    36: "This is the leaf of a tomato plant affected by two-spotted spider mite. Use insecticidal soap and remove heavily infested leaves.",
    37: "This is the leaf of an orange tree affected by huanglongbing. Remove infected plants and control psyllid vectors.",
    38: "This is the leaf of an apple tree affected by black rot. Remove infected fruits and branches, apply fungicides, and practice good sanitation."
}

# Load your trained ResNet model
model_path = 'resnet50model.pth'

try:
    print("Model loaded successfully!")

    # Load the model
    resnet_model = torch.load(model_path, map_location=torch.device("cpu"))

    # Ensure the model is in evaluation mode
    resnet_model.eval()

    print("Model loaded successfully!")

except Exception as e:
    print("Error loading the model:", str(e))

@app.route('/')
def index():
    return render_template('plant.html')

@app.route('/resnet_predict', methods=['POST'])
def resnet_predict():
    if request.method == 'POST':
        try:
            # Receive the image from the frontend
            image_data = request.form['image']

            # Replace 'base64_encoded_image' with your actual Base64-encoded image string
            base64_encoded_image =  image_data

            # Extract the base64 content from the string (remove the data URI part if present)
            _, base64_content = base64_encoded_image.split(',')

            # Decode the Base64 content
            image_data = base64.b64decode(base64_content)

            # Create a PIL Image from the decoded binary data
            image = Image.open(io.BytesIO(image_data))

            # Process the image for ResNet prediction
            transform = transforms.Compose([
                transforms.Resize((200, 200)),  # Resize images to 200x200
                transforms.ToTensor(),
            ])

            input_tensor = transform(image)
            input_batch = input_tensor.unsqueeze(0)  # Add batch dimension

            # Perform prediction
            with torch.no_grad():
                output = resnet_model(input_batch)

            _, predicted_class = torch.max(output, 1)
            predicted_class = predicted_class.item()

            # Debugging print statements
            print('Prediction:', label_mapping[predicted_class])

            # Return the prediction as a JSON response
            return jsonify({'prediction': label_mapping[predicted_class]})

        except Exception as e:
            # Print the exception details
            print("Error:", str(e))

            # Return a JSON error response
            return jsonify({'error': 'Internal Server Error'})

if __name__ == '__main__':
    app.run(debug=True)
