# Sign Language Detection

This project implements a real-time sign language detection system using deep learning and computer vision. It can recognize alphabets (A-Z), numbers (0-9), and special characters in sign language through a web interface.

## Features

- Real-time sign language detection through webcam
- Support for:
  - Alphabets (A-Z)
  - Numbers (0-9)
  - Special characters
- Text to sign language conversion
- Web-based user interface
- Built with Python, Flask, and TensorFlow/Keras

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.x
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/Sign-Language-detection.git
cd Sign-Language-detection
```

2. Install the required dependencies:
```bash
pip install flask opencv-python tensorflow numpy pillow
```

## Project Structure

```
Sign-Language-detection/
├── app.py                 # Main Flask application
├── dataCollection.py      # Script for collecting training data
├── data/                 # Training data directory
├── model/               
│   ├── keras_model.h5    # Trained model
│   └── labels.txt        # Label definitions
├── static/               # Static files (JS, CSS)
└── templates/            # HTML templates
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. The application offers two main features:
   - Real-time sign language detection through your webcam
   - Text to sign language conversion

## Data Collection

If you want to collect your own training data:

1. Run the data collection script:
```bash
python dataCollection.py
```

2. Follow the on-screen instructions to capture images for training.

## Model Information

The project uses a pre-trained Keras model (`model/keras_model.h5`) for sign language detection. The model is trained to recognize:
- Letters A through Z
- Numbers 0 through 9
- Special characters

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all contributors who have helped with the development of this project
- Special thanks to the open-source community for providing tools and libraries used in this project