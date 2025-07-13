# Mental Health Assessment Tool

A comprehensive Streamlit-based application that analyzes text and voice inputs to provide depression risk assessment.

## Features

- **Text Analysis**: Uses Natural Language Processing to analyze written text for depression indicators
- **Voice Analysis**: Processes audio recordings to detect vocal patterns associated with depression
- **Combined Assessment**: Provides comprehensive risk scoring combining both text and voice analysis
- **Mental Health Resources**: Includes crisis helplines and support resources
- **User-Friendly Interface**: Clean, responsive web interface with clear risk visualizations

## Installation

1. Ensure you have Python 3.8+ installed
2. Install required dependencies:
   ```bash
   pip install streamlit pandas plotly nltk spacy textblob pydub numpy scipy streamlit-webrtc
   ```

3. Download required NLP models:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

1. Run the application:
   ```bash
   streamlit run app.py --server.port 5000
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Use the application:
   - Enter text in the text analysis section
   - Upload an audio file (WAV, MP3, OGG, M4A, WebM) for voice analysis
   - View your risk assessment and recommendations

## Risk Levels

- **Low Risk (0-3.0)**: Green indicator - Continue maintaining good mental health habits
- **Moderate Risk (3.1-5.0)**: Orange indicator - Consider speaking with a mental health professional
- **High Risk (5.1-7.0)**: Red indicator - Strongly recommend professional support
- **Very High Risk (7.1-10.0)**: Dark red indicator - Seek immediate professional help

## Important Disclaimer

This tool is for educational and screening purposes only. It is NOT a substitute for professional medical diagnosis or treatment. If you are experiencing mental health concerns, please consult with a qualified mental health professional.

## Files Structure

- `app.py` - Main Streamlit application
- `text_analyzer.py` - Text analysis module using NLP
- `voice_analyzer_simple.py` - Voice analysis module
- `depression_predictor.py` - Risk assessment engine
- `utils.py` - Utility functions and resources
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration

## Technical Details

- **Frontend**: Streamlit web framework
- **Text Analysis**: NLTK, spaCy, TextBlob for sentiment analysis
- **Voice Analysis**: Audio processing using numpy and scipy
- **Risk Assessment**: Weighted combination of text and voice scores

## Support

For crisis support, please contact:
- National Suicide Prevention Lifeline: 988 (US)
- Crisis Text Line: Text HOME to 741741
- International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

## License

This project is for educational purposes. Please use responsibly and always encourage professional help when needed.