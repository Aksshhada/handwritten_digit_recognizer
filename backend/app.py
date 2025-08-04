# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from PIL import Image
# import io
# import re
# import base64
# import numpy as np
# import tensorflow as tf

# app = Flask(__name__)
# CORS(app)

# # Load the trained model
# model = tf.keras.models.load_model('digit_model.h5')


# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json()
#     if 'image' not in data:
#         return jsonify({'error': 'No image provided'}), 400

#     # Get base64 string from data URL
#     image_data = data['image']
#     image_data = re.sub('^data:image/.+;base64,', '', image_data)
#     image_bytes = base64.b64decode(image_data)
#     image = Image.open(io.BytesIO(image_bytes)).convert('L')
#     image = image.resize((28, 28))
#     image_array = np.array(image)
#     image_array = 255 - image_array  # invert colors: white background → black digit
#     image_array = image_array / 255.0
#     image_array = image_array.reshape(1, 28, 28, 1)

#     prediction = model.predict(image_array)
#     predicted_class = int(np.argmax(prediction))

#     return jsonify({'prediction': predicted_class})

# if __name__ == "__main__":
#     app.run(debug=True)





from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import re
import base64
import numpy as np
import tensorflow as tf

app = Flask(__name__)
CORS(app)

# Load the trained model
model = tf.keras.models.load_model('digit_model.h5')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    # Get base64 string from data URL
    image_data = data['image']
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image_bytes = base64.b64decode(image_data)

    # Convert and preprocess image
    image = Image.open(io.BytesIO(image_bytes)).convert('L')  # Grayscale
    image = image.resize((28, 28))  # Resize to model input
    image_array = np.array(image)

    image_array = 255 - image_array  # Invert colors (black digit on white)
    image_array = image_array / 255.0  # Normalize pixel values

    # Binarize image: anything above 0.1 becomes 1.0 (digit), rest 0.0 (background)
    image_array = (image_array > 0.1).astype(np.float32)

    image_array = image_array.reshape(1, 28, 28, 1)  # Add batch and channel dimensions

    prediction = model.predict(image_array)
    print("Prediction probabilities:", prediction)  # Debugging: show full prediction probs

    predicted_class = int(np.argmax(prediction))

    return jsonify({'prediction': predicted_class})


if __name__ == "__main__":
    app.run(debug=True)
