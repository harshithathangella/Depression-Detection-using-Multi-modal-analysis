# Mental Health Assessment Tool

## Overview

This is a Streamlit-based mental health assessment application that analyzes text and voice inputs to provide depression risk assessment. The tool combines natural language processing for text analysis and audio signal processing for voice analysis to generate a composite risk score. The application is designed for educational purposes and includes proper disclaimers about professional medical advice.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application
- **UI Components**: 
  - Multi-page navigation with sidebar
  - Audio recording capabilities via `streamlit_audio_recorder`
  - Interactive data visualizations using Plotly
  - Responsive layout with warning disclaimers
- **State Management**: Streamlit session state for analyzer instances

### Backend Architecture
- **Modular Design**: Separate analyzer classes for different assessment types
- **Core Components**:
  - `TextAnalyzer`: NLP-based text sentiment and keyword analysis
  - `VoiceAnalyzer`: Audio signal processing for voice pattern analysis
  - `DepressionPredictor`: Risk assessment engine combining multiple inputs
  - `utils`: Resource management and helper functions

### Data Processing Pipeline
1. **Text Analysis**: Uses NLTK, spaCy, and TextBlob for sentiment analysis and keyword detection
2. **Voice Analysis**: Employs librosa for audio feature extraction (pitch, energy, speech rate, pauses, spectral features)
3. **Risk Prediction**: Weighted combination of text and voice scores with non-linear adjustments

## Key Components

### TextAnalyzer
- **Purpose**: Analyzes written text for depression-related indicators
- **Technologies**: NLTK, spaCy, TextBlob
- **Features**: 
  - Sentiment analysis
  - Depression keyword detection
  - Automatic model downloading and setup
- **Design Decision**: Uses multiple NLP libraries for comprehensive analysis rather than single-library approach for better accuracy

### VoiceAnalyzer
- **Purpose**: Processes audio recordings for vocal biomarkers of depression
- **Technologies**: librosa, scipy, numpy
- **Features**:
  - Pitch variation analysis
  - Energy level assessment
  - Speech rate calculation
  - Pause pattern detection
  - Spectral feature analysis
- **Design Decision**: Multi-feature approach with weighted scoring to capture various vocal indicators

### DepressionPredictor
- **Purpose**: Combines multiple analysis inputs into final risk assessment
- **Scoring System**: 0-10 scale where lower scores indicate higher risk
- **Risk Categories**: Low Risk (6+), Moderate Risk (4-6), High Risk (2-4), Critical Risk (<2)
- **Design Decision**: Weighted combination (60% text, 40% voice) with non-linear adjustments for extreme scores

## Data Flow

1. **Input Collection**: User provides text input and/or audio recording
2. **Parallel Processing**: Text and voice analyzed simultaneously by respective analyzers
3. **Score Generation**: Each analyzer produces 0-10 risk score
4. **Risk Prediction**: DepressionPredictor combines scores with confidence adjustments
5. **Result Presentation**: Risk level displayed with appropriate resources and recommendations

## External Dependencies

### Python Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation
- **plotly**: Interactive visualizations
- **nltk**: Natural language processing
- **spacy**: Advanced NLP features
- **textblob**: Sentiment analysis
- **librosa**: Audio analysis
- **scipy**: Scientific computing
- **numpy**: Numerical operations
- **streamlit_audio_recorder**: Audio recording widget

### Models and Data
- **spaCy English model**: `en_core_web_sm` for text processing
- **NLTK data**: punkt tokenizer, stopwords, VADER lexicon
- **Audio processing**: 22.05kHz sample rate standard

## Deployment Strategy

### Local Development
- **Requirements**: Python environment with pip package management
- **Setup**: Automatic dependency installation and model downloading
- **Runtime**: Streamlit development server

### Production Considerations
- **Error Handling**: Graceful fallbacks for missing models or processing errors
- **Privacy**: Local processing with no permanent data storage
- **Performance**: Session state management for analyzer initialization
- **Scalability**: Modular architecture supports easy feature additions

## Changelog
- July 03, 2025. Initial setup
- July 03, 2025. Added voice recording and analysis functionality using streamlit-webrtc and pydub
- July 03, 2025. Implemented real-time voice analysis with energy, speech rate, and pause pattern detection
- July 03, 2025. Added audio file upload feature as alternative to live recording

## User Preferences

Preferred communication style: Simple, everyday language.