import nltk
import spacy
import pandas as pd
import numpy as np
from collections import Counter
import re
from textblob import TextBlob
import streamlit as st

class TextAnalyzer:
    def __init__(self):
        self.setup_nltk()
        self.setup_spacy()
        self.depression_keywords = [
            'sad', 'depressed', 'hopeless', 'worthless', 'empty', 'lonely',
            'tired', 'exhausted', 'unmotivated', 'anxious', 'worried',
            'stressed', 'overwhelmed', 'isolated', 'disconnected', 'numb',
            'pain', 'hurt', 'suffering', 'struggle', 'difficult', 'hard',
            'cannot', 'unable', 'impossible', 'fail', 'failure', 'lost',
            'darkness', 'heavy', 'burden', 'trapped', 'stuck', 'helpless'
        ]
        
        self.positive_keywords = [
            'happy', 'joy', 'excited', 'great', 'amazing', 'wonderful', 'fantastic',
            'good', 'excellent', 'love', 'enjoyable', 'pleasant', 'cheerful',
            'optimistic', 'positive', 'grateful', 'blessed', 'content', 'satisfied'
        ]
        
    def setup_nltk(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
            
        try:
            nltk.data.find('corpora/vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon')
    
    def setup_spacy(self):
        """Setup spaCy model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            st.warning("spaCy English model not found. Installing...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
    
    def analyze_text(self, text):
        """
        Analyze text and return a depression risk score (0-10)
        Lower scores indicate higher risk
        """
        if not text or len(text.strip()) < 10:
            return 5.0  # Neutral score for insufficient text
        
        # Clean and preprocess text
        text = self.preprocess_text(text)
        
        # Multiple analysis approaches
        sentiment_score = self.analyze_sentiment(text)
        keyword_score = self.analyze_keywords(text)
        linguistic_score = self.analyze_linguistic_patterns(text)
        emotional_score = self.analyze_emotional_indicators(text)
        
        # Combine scores with weights
        final_score = (
            sentiment_score * 0.5 +  # Higher weight for sentiment
            keyword_score * 0.3 +    # Keywords are important
            linguistic_score * 0.15 + # Reduced linguistic weight
            emotional_score * 0.05    # Minimal emotional weight
        )
        
        # Apply positive bias - if sentiment is strongly positive, cap the risk
        if sentiment_score < 3.0:  # Very positive sentiment
            final_score = min(final_score, 3.0)  # Cap at moderate-low risk
        
        # Ensure score is within range [0, 10]
        return max(0, min(10, final_score))
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation for sentiment analysis
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        
        return text.strip()
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using TextBlob and VADER"""
        from nltk.sentiment import SentimentIntensityAnalyzer
        
        # TextBlob sentiment
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        
        # VADER sentiment
        sia = SentimentIntensityAnalyzer()
        vader_scores = sia.polarity_scores(text)
        compound_score = vader_scores['compound']  # -1 to 1
        
        # Combine and convert to 0-10 scale
        avg_sentiment = (polarity + compound_score) / 2
        
        # Convert to risk score (positive sentiment = lower risk, negative = higher risk)
        # Scale: +1 sentiment = 0 risk, -1 sentiment = 10 risk, 0 sentiment = 5 risk
        risk_score = 5 - (avg_sentiment * 5)  # 0-10 scale
        
        return risk_score
    
    def analyze_keywords(self, text):
        """Analyze presence of depression-related and positive keywords"""
        words = text.lower().split()
        
        if len(words) == 0:
            return 5.0
        
        # Count depression keywords (exact word matches only)
        depression_count = sum(1 for word in words if word in self.depression_keywords)
        
        # Count positive keywords (exact word matches only)
        positive_count = sum(1 for word in words if word in self.positive_keywords)
        
        # Calculate ratios
        depression_ratio = depression_count / len(words)
        positive_ratio = positive_count / len(words)
        
        # Calculate risk score
        base_score = 5.0
        
        # Positive keywords reduce risk
        if positive_ratio > 0:
            base_score -= positive_ratio * 20  # Strong positive influence
        
        # Depression keywords increase risk
        if depression_ratio > 0:
            base_score += depression_ratio * 30  # Strong negative influence
        
        # Ensure score stays within bounds
        return max(0.0, min(10.0, base_score))
    
    def analyze_linguistic_patterns(self, text):
        """Analyze linguistic patterns that may indicate depression"""
        doc = self.nlp(text)
        
        # First person pronouns (only excessive self-focus is concerning)
        first_person_count = sum(1 for token in doc if token.text.lower() in ['i', 'me', 'my', 'myself'])
        
        # Negative words
        negative_words = ['no', 'not', 'never', 'nothing', 'nobody', 'nowhere', 'neither', 'nor']
        negative_count = sum(1 for token in doc if token.text.lower() in negative_words)
        
        # Absolute words (black and white thinking)
        absolute_words = ['always', 'never', 'all', 'nothing', 'everything', 'everyone', 'nobody']
        absolute_count = sum(1 for token in doc if token.text.lower() in absolute_words)
        
        # Calculate ratios
        total_words = len([token for token in doc if token.is_alpha])
        if total_words == 0:
            return 5.0
        
        first_person_ratio = first_person_count / total_words
        negative_ratio = negative_count / total_words
        absolute_ratio = absolute_count / total_words
        
        # Start with neutral score
        risk_score = 5.0
        
        # Only penalize excessive first-person usage (> 30% of words)
        if first_person_ratio > 0.3:
            risk_score += (first_person_ratio - 0.3) * 10
        
        # Penalize negative language
        risk_score += negative_ratio * 15
        
        # Penalize absolute thinking
        risk_score += absolute_ratio * 20
        
        return min(10, risk_score)
    
    def analyze_emotional_indicators(self, text):
        """Analyze emotional indicators in text"""
        # Emotion words categories
        sadness_words = ['sad', 'depressed', 'down', 'blue', 'melancholy', 'sorrowful']
        anxiety_words = ['anxious', 'worried', 'nervous', 'scared', 'afraid', 'panic']
        hopelessness_words = ['hopeless', 'helpless', 'worthless', 'pointless', 'useless']
        
        words = text.lower().split()
        
        sadness_count = sum(1 for word in words if any(sw in word for sw in sadness_words))
        anxiety_count = sum(1 for word in words if any(aw in word for aw in anxiety_words))
        hopelessness_count = sum(1 for word in words if any(hw in word for hw in hopelessness_words))
        
        if len(words) == 0:
            return 5.0
        
        # Weight hopelessness more heavily
        emotional_score = (sadness_count + anxiety_count + hopelessness_count * 2) / len(words)
        
        # Convert to risk score
        risk_score = min(10, 5 + (emotional_score * 30))
        
        return risk_score
    
    def get_detailed_analysis(self, text):
        """Get detailed analysis results"""
        blob = TextBlob(text)
        doc = self.nlp(text)
        
        # Sentiment breakdown
        sentiment_breakdown = {
            'Positive': max(0, blob.sentiment.polarity),
            'Negative': max(0, -blob.sentiment.polarity),
            'Neutral': 1 - abs(blob.sentiment.polarity)
        }
        
        # Key phrases extraction
        key_phrases = []
        for chunk in doc.noun_chunks:
            if len(chunk.text.strip()) > 2:
                key_phrases.append(chunk.text.strip())
        
        # Depression keywords found
        words = text.lower().split()
        found_keywords = [word for word in words if any(keyword in word for keyword in self.depression_keywords)]
        
        return {
            'sentiment_breakdown': sentiment_breakdown,
            'key_phrases': key_phrases[:10],  # Top 10 phrases
            'found_keywords': list(set(found_keywords)),
            'word_count': len(words),
            'subjectivity': blob.sentiment.subjectivity
        }
