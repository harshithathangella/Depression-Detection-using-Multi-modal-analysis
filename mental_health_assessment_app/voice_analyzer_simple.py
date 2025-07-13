import numpy as np
import warnings
import wave
import tempfile
import os
from pydub import AudioSegment
warnings.filterwarnings('ignore')

class VoiceAnalyzer:
    def __init__(self):
        self.sample_rate = 22050
        
    def analyze_voice(self, audio_data=None, audio_file_path=None):
        """
        Analyze voice patterns and return a depression risk score (0-10)
        Lower scores indicate higher risk
        """
        try:
            if audio_data is not None:
                # Convert audio data to temporary file for analysis
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(audio_data)
                    temp_path = tmp_file.name
                
                score = self._analyze_audio_file(temp_path)
                
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
                return score
                
            elif audio_file_path:
                return self._analyze_audio_file(audio_file_path)
            else:
                return 5.0  # Neutral score if no audio provided
                
        except Exception as e:
            print(f"Error analyzing voice: {e}")
            return 5.0  # Return neutral score on error
    
    def _analyze_audio_file(self, file_path):
        """Analyze audio file and return depression risk score"""
        try:
            # Load audio using pydub
            audio = AudioSegment.from_file(file_path)
            
            # Convert to numpy array
            samples = np.array(audio.get_array_of_samples())
            
            # If stereo, convert to mono
            if audio.channels == 2:
                samples = samples.reshape((-1, 2))
                samples = samples.mean(axis=1)
            
            # Normalize
            samples = samples / np.max(np.abs(samples))
            
            # Basic audio analysis
            duration = len(samples) / audio.frame_rate
            
            # Energy analysis
            energy = np.mean(samples ** 2)
            
            # Simple speech rate estimation (zero crossings)
            zero_crossings = np.sum(np.diff(np.signbit(samples)))
            speech_rate = zero_crossings / (duration * 2)  # Approximate speech rate
            
            # Pause detection (silence regions)
            silence_threshold = 0.01
            silent_samples = np.abs(samples) < silence_threshold
            pause_ratio = np.sum(silent_samples) / len(samples)
            
            # Calculate risk score based on audio features
            risk_score = self._calculate_risk_score(energy, speech_rate, pause_ratio, duration)
            
            return max(0, min(10, risk_score))
            
        except Exception as e:
            print(f"Error in audio file analysis: {e}")
            return 5.0
    
    def _calculate_risk_score(self, energy, speech_rate, pause_ratio, duration):
        """Calculate depression risk score from audio features"""
        base_score = 5.0
        
        # Low energy might indicate depression
        if energy < 0.01:
            base_score -= 2.0
        elif energy < 0.05:
            base_score -= 1.0
        elif energy > 0.2:
            base_score += 1.0
        
        # Very slow or very fast speech might indicate issues
        if speech_rate < 50:  # Very slow speech
            base_score -= 1.5
        elif speech_rate < 100:  # Slow speech
            base_score -= 0.5
        elif speech_rate > 300:  # Very fast speech (anxiety)
            base_score -= 1.0
        
        # Too many pauses might indicate hesitation/depression
        if pause_ratio > 0.7:
            base_score -= 1.5
        elif pause_ratio > 0.5:
            base_score -= 0.5
        
        # Very short recordings are less reliable
        if duration < 3:
            base_score += 1.0  # More conservative for short clips
        
        return base_score
    
    def get_detailed_analysis(self, audio_data=None, audio_file_path=None):
        """Get detailed analysis results"""
        try:
            if audio_data is not None:
                # Convert audio data to temporary file for analysis
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(audio_data)
                    temp_path = tmp_file.name
                
                result = self._get_detailed_analysis_from_file(temp_path)
                
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
                return result
                
            elif audio_file_path:
                return self._get_detailed_analysis_from_file(audio_file_path)
            else:
                return self._get_default_analysis()
                
        except Exception as e:
            print(f"Error in detailed analysis: {e}")
            return self._get_default_analysis()
    
    def _get_detailed_analysis_from_file(self, file_path):
        """Get detailed analysis from audio file"""
        try:
            audio = AudioSegment.from_file(file_path)
            samples = np.array(audio.get_array_of_samples())
            
            if audio.channels == 2:
                samples = samples.reshape((-1, 2))
                samples = samples.mean(axis=1)
            
            samples = samples / np.max(np.abs(samples))
            duration = len(samples) / audio.frame_rate
            
            # Calculate features
            energy = np.mean(samples ** 2)
            zero_crossings = np.sum(np.diff(np.signbit(samples)))
            speech_rate = zero_crossings / (duration * 2)
            
            silence_threshold = 0.01
            silent_samples = np.abs(samples) < silence_threshold
            pause_ratio = np.sum(silent_samples) / len(samples)
            
            # Estimate pitch variation (simplified)
            pitch_variation = np.std(samples) / np.mean(np.abs(samples)) if np.mean(np.abs(samples)) > 0 else 0
            
            return {
                'pitch_variation': min(1.0, pitch_variation),
                'energy_level': min(1.0, energy * 10),
                'speech_rate': min(10.0, speech_rate / 50),
                'pause_frequency': min(1.0, pause_ratio),
                'duration': duration,
                'avg_pause_duration': pause_ratio * duration
            }
            
        except Exception as e:
            print(f"Error in detailed file analysis: {e}")
            return self._get_default_analysis()
    
    def _get_default_analysis(self):
        """Return default analysis values"""
        return {
            'pitch_variation': 0.15,
            'energy_level': 0.05,
            'speech_rate': 3.2,
            'pause_frequency': 0.8,
            'duration': 5.0,
            'avg_pause_duration': 0.5
        }