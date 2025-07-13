import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import tempfile
import os
import numpy as np
from text_analyzer import TextAnalyzer
from voice_analyzer_simple import VoiceAnalyzer
from depression_predictor import DepressionPredictor
from utils import get_mental_health_resources, get_risk_level_info

def main():
    st.set_page_config(
        page_title="Depression Detection Assessment Tool",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize analyzers
    if 'text_analyzer' not in st.session_state:
        st.session_state.text_analyzer = TextAnalyzer()
    if 'voice_analyzer' not in st.session_state:
        st.session_state.voice_analyzer = VoiceAnalyzer()
    if 'depression_predictor' not in st.session_state:
        st.session_state.depression_predictor = DepressionPredictor()
    
    # Header
    st.title("🧠 Depression Detection Assessment Tool")
    st.markdown("---")
    
    # Important disclaimer
    st.warning("""
    ⚠️ **Important Disclaimer**: This tool is for educational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. If you're experiencing mental health concerns, please consult with a qualified healthcare professional.
    """)
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        page = st.selectbox(
            "Choose a section:",
            ["Assessment", "Resources", "About"]
        )
        
        st.markdown("---")
        st.markdown("### Privacy Notice")
        st.info("Your data is processed locally and not stored permanently.")
    
    if page == "Assessment":
        show_assessment_page()
    elif page == "Resources":
        show_resources_page()
    else:
        show_about_page()

def show_assessment_page():
    st.header("Mental Health Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Text Analysis")
        st.markdown("Please share your thoughts and feelings:")
        
        text_input = st.text_area(
            "How are you feeling today?",
            height=200,
            placeholder="Share your thoughts, feelings, or experiences here..."
        )
        
        text_score = None
        if text_input:
            with st.spinner("Analyzing text..."):
                text_score = st.session_state.text_analyzer.analyze_text(text_input)
            
            st.success(f"Text analysis completed! Score: {text_score:.2f}")
            
            # Display text analysis details
            with st.expander("View Text Analysis Details"):
                sentiment_data = st.session_state.text_analyzer.get_detailed_analysis(text_input)
                
                # Sentiment breakdown
                fig_sentiment = px.bar(
                    x=list(sentiment_data['sentiment_breakdown'].keys()),
                    y=list(sentiment_data['sentiment_breakdown'].values()),
                    title="Sentiment Breakdown"
                )
                st.plotly_chart(fig_sentiment, use_container_width=True)
                
                # Key phrases
                if sentiment_data['key_phrases']:
                    st.write("**Key Phrases Detected:**")
                    for phrase in sentiment_data['key_phrases']:
                        st.write(f"- {phrase}")
    
    with col2:
        st.subheader("🎤 Voice Analysis")
        st.markdown("Upload an audio file to analyze speech patterns:")
        
        voice_score = None
        
        # Simple instructions for voice recording
        st.info("""
        📱 **How to record your voice:**
        1. Use your phone's voice recorder app
        2. Record yourself speaking for 30-60 seconds
        3. Save the recording as a file
        4. Upload it using the button below
        """)
        
        # Audio file upload
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=['wav', 'mp3', 'ogg', 'm4a', 'webm'],
            help="Upload a voice recording in WAV, MP3, OGG, M4A, or WebM format"
        )
        
        if uploaded_file is not None:
            # Show file details
            st.write(f"**File name:** {uploaded_file.name}")
            st.write(f"**File size:** {uploaded_file.size / 1024:.1f} KB")
            
            # Play audio file
            st.audio(uploaded_file, format='audio/wav')
            
            if st.button("Analyze Voice", type="primary"):
                with st.spinner("Analyzing voice patterns..."):
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        temp_path = tmp_file.name
                    
                    try:
                        voice_score = st.session_state.voice_analyzer.analyze_voice(audio_file_path=temp_path)
                        st.success(f"Voice analysis completed! Score: {voice_score:.2f}")
                        
                        # Display voice analysis details
                        with st.expander("View Voice Analysis Details"):
                            voice_data = st.session_state.voice_analyzer.get_detailed_analysis(audio_file_path=temp_path)
                            
                            # Voice features
                            features_df = pd.DataFrame({
                                'Feature': ['Pitch Variation', 'Energy Level', 'Speech Rate', 'Pause Frequency'],
                                'Value': [
                                    voice_data['pitch_variation'],
                                    voice_data['energy_level'],
                                    voice_data['speech_rate'],
                                    voice_data['pause_frequency']
                                ]
                            })
                            
                            fig_voice = px.bar(
                                features_df,
                                x='Feature',
                                y='Value',
                                title="Voice Pattern Analysis",
                                color='Feature'
                            )
                            st.plotly_chart(fig_voice, use_container_width=True)
                            
                            # Additional details
                            st.write("**Analysis Details:**")
                            st.write(f"- Duration: {voice_data['duration']:.1f} seconds")
                            st.write(f"- Energy Level: {voice_data['energy_level']:.3f}")
                            st.write(f"- Speech Rate: {voice_data['speech_rate']:.2f}")
                            st.write(f"- Pause Frequency: {voice_data['pause_frequency']:.2f}")
                            
                    finally:
                        # Clean up temporary file
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)
        
        # Demo voice analysis option
        st.markdown("---")
        st.markdown("**Don't have an audio file? Try a demo:**")
        if st.button("Demo Voice Analysis", help="This will show sample voice analysis results"):
            voice_score = 6.5  # Sample score
            st.success(f"Demo voice analysis completed! Score: {voice_score:.2f}")
            
            # Display demo voice analysis details
            with st.expander("View Demo Voice Analysis Details"):
                demo_data = {
                    'pitch_variation': 0.25,
                    'energy_level': 0.15,
                    'speech_rate': 4.2,
                    'pause_frequency': 0.6,
                    'duration': 15.0,
                    'avg_pause_duration': 0.8
                }
                
                features_df = pd.DataFrame({
                    'Feature': ['Pitch Variation', 'Energy Level', 'Speech Rate', 'Pause Frequency'],
                    'Value': [
                        demo_data['pitch_variation'],
                        demo_data['energy_level'],
                        demo_data['speech_rate'],
                        demo_data['pause_frequency']
                    ]
                })
                
                fig_voice = px.bar(
                    features_df,
                    x='Feature',
                    y='Value',
                    title="Demo Voice Pattern Analysis",
                    color='Feature'
                )
                st.plotly_chart(fig_voice, use_container_width=True)
                
                st.write("**Demo Analysis Details:**")
                st.write(f"- Duration: {demo_data['duration']:.1f} seconds")
                st.write(f"- Energy Level: {demo_data['energy_level']:.3f}")
                st.write(f"- Speech Rate: {demo_data['speech_rate']:.2f}")
                st.write(f"- Pause Frequency: {demo_data['pause_frequency']:.2f}")
    
    # Combined analysis
    if text_score is not None or voice_score is not None:
        st.markdown("---")
        st.header("🎯 Combined Assessment Results")
        
        # Calculate combined score
        combined_score = st.session_state.depression_predictor.predict_depression_risk(
            text_score, voice_score
        )
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Text Analysis Score",
                f"{text_score:.2f}" if text_score is not None else "N/A",
                help="Lower scores indicate more concerning text patterns"
            )
        
        with col2:
            st.metric(
                "Voice Analysis Score",
                f"{voice_score:.2f}" if voice_score is not None else "N/A",
                help="Lower scores indicate more concerning voice patterns"
            )
        
        with col3:
            st.metric(
                "Combined Risk Assessment",
                f"{combined_score:.2f}",
                help="Overall risk assessment based on available data"
            )
        
        # Risk level indicator
        risk_level, color, message = get_risk_level_info(combined_score)
        
        st.markdown(f"""
        <div style="padding: 20px; border-radius: 10px; background-color: {color}; margin: 20px 0;">
            <h3 style="color: white; margin: 0;">Risk Level: {risk_level}</h3>
            <p style="color: white; margin: 10px 0 0 0;">{message}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Recommendations
        st.subheader("💡 Recommendations")
        recommendations = st.session_state.depression_predictor.get_recommendations(combined_score)
        for rec in recommendations:
            st.write(f"• {rec}")
        
        # Progress visualization
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=combined_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Mental Health Risk Assessment"},
            delta={'reference': 5.0},
            gauge={
                'axis': {'range': [None, 10]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 3], 'color': "lightgreen"},
                    {'range': [3, 6], 'color': "yellow"},
                    {'range': [6, 10], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 7
                }
            }
        ))
        
        st.plotly_chart(fig_gauge, use_container_width=True)

def show_resources_page():
    st.header("🆘 Mental Health Resources")
    
    resources = get_mental_health_resources()
    
    for category, items in resources.items():
        st.subheader(category)
        for item in items:
            st.write(f"• **{item['name']}**: {item['description']}")
            if 'contact' in item:
                st.write(f"  📞 {item['contact']}")
            if 'website' in item:
                st.write(f"  🌐 {item['website']}")
        st.markdown("---")

def show_about_page():
    st.header("ℹ️ About This Tool")
    
    st.markdown("""
    ### Purpose
    This Mental Health Assessment Tool uses natural language processing and basic audio analysis to provide insights into mental health indicators based on text and voice inputs.
    
    ### How It Works
    
    **Text Analysis:**
    - Analyzes sentiment, emotional tone, and linguistic patterns
    - Identifies key phrases and emotional indicators
    - Uses machine learning models trained on mental health datasets
    
    **Voice Analysis:**
    - Examines speech patterns, pitch variation, and energy levels
    - Analyzes pause frequency and speech rate
    - Detects vocal stress indicators
    
    **Combined Assessment:**
    - Weighs both text and voice analysis results
    - Provides a comprehensive risk assessment
    - Offers personalized recommendations
    
    ### Important Notes
    - This tool is for educational and awareness purposes only
    - Results should not be used for medical diagnosis
    - Always consult healthcare professionals for medical concerns
    - Your privacy is protected - no data is stored permanently
    
    ### Technology Stack
    - **Frontend**: Streamlit
    - **Text Analysis**: NLTK, spaCy
    - **Voice Analysis**: librosa, scipy
    - **Visualization**: Plotly
    """)

if __name__ == "__main__":
    main()
