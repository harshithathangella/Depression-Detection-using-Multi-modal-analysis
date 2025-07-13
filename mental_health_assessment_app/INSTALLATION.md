# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection for downloading models

## Step-by-Step Installation

### 1. Extract the ZIP file
Extract all files to your desired directory.

### 2. Install Python Dependencies
Navigate to the project directory and install required packages:

```bash
pip install -r project_requirements.txt
```

Or install individually:
```bash
pip install streamlit pandas plotly nltk spacy textblob pydub numpy scipy streamlit-webrtc
```

### 3. Download NLP Models
Download the required spaCy English model:

```bash
python -m spacy download en_core_web_sm
```

### 4. Run the Application
Start the Streamlit application:

```bash
streamlit run app.py --server.port 5000
```

### 5. Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## Troubleshooting

### Common Issues:

1. **ModuleNotFoundError**: Ensure all dependencies are installed
2. **spaCy model not found**: Run the model download command again
3. **Port already in use**: Change the port number in the command
4. **Audio upload issues**: Ensure your audio files are in supported formats (WAV, MP3, OGG, M4A, WebM)

### System Requirements:
- RAM: Minimum 2GB, recommended 4GB
- Storage: At least 500MB free space
- OS: Windows 10+, macOS 10.14+, or Linux

## Configuration

The application includes a `.streamlit/config.toml` file with optimized settings. You can modify it if needed:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

## Support

If you encounter issues:
1. Check that all dependencies are installed correctly
2. Verify your Python version is 3.8+
3. Ensure internet connection for initial model downloads
4. Try running with different port numbers if port 5000 is occupied