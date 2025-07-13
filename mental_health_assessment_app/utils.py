def get_mental_health_resources():
    """Return mental health resources and helplines"""
    return {
        "🆘 Crisis Helplines": [
            {
                "name": "National Suicide Prevention Lifeline",
                "description": "24/7 free and confidential support for people in distress",
                "contact": "988 or 1-800-273-8255",
                "website": "https://suicidepreventionlifeline.org"
            },
            {
                "name": "Crisis Text Line",
                "description": "Free, 24/7 crisis support via text message",
                "contact": "Text HOME to 741741",
                "website": "https://www.crisistextline.org"
            },
            {
                "name": "National Alliance on Mental Illness (NAMI)",
                "description": "Support and education for individuals and families",
                "contact": "1-800-950-NAMI (6264)",
                "website": "https://www.nami.org"
            }
        ],
        "🏥 Professional Help": [
            {
                "name": "Psychology Today",
                "description": "Find mental health professionals in your area",
                "website": "https://www.psychologytoday.com"
            },
            {
                "name": "SAMHSA Treatment Locator",
                "description": "Find treatment facilities and programs",
                "contact": "1-800-662-4357",
                "website": "https://findtreatment.samhsa.gov"
            },
            {
                "name": "Your Primary Care Doctor",
                "description": "Start with your family doctor for referrals and initial assessment"
            }
        ],
        "💪 Self-Help Resources": [
            {
                "name": "Headspace",
                "description": "Meditation and mindfulness app",
                "website": "https://www.headspace.com"
            },
            {
                "name": "Calm",
                "description": "Sleep, meditation, and relaxation app",
                "website": "https://www.calm.com"
            },
            {
                "name": "7 Cups",
                "description": "Free emotional support and online therapy",
                "website": "https://www.7cups.com"
            }
        ],
        "📚 Educational Resources": [
            {
                "name": "National Institute of Mental Health (NIMH)",
                "description": "Comprehensive information about mental health conditions",
                "website": "https://www.nimh.nih.gov"
            },
            {
                "name": "Mental Health America",
                "description": "Mental health screening tools and resources",
                "website": "https://www.mentalhealthamerica.net"
            }
        ]
    }

def get_risk_level_info(score):
    """Get risk level information including color and message"""
    if score <= 3.0:
        return (
            "Low Risk",
            "#4CAF50",  # Green
            "Your responses suggest you're managing well. Continue with healthy habits and don't hesitate to seek support if needed."
        )
    elif score <= 5.0:
        return (
            "Moderate Risk",
            "#FF9800",  # Orange
            "Your responses indicate some areas of concern. Consider speaking with a mental health professional for support and guidance."
        )
    elif score <= 7.0:
        return (
            "High Risk",
            "#F44336",  # Red
            "Your responses suggest significant concerns. We strongly recommend reaching out to a mental health professional or crisis helpline."
        )
    else:
        return (
            "Very High Risk",
            "#D32F2F",  # Dark Red
            "Your responses indicate serious concerns. Please seek immediate professional help or contact a crisis helpline right away."
        )

def format_score_explanation(score_type, score):
    """Format explanation for different score types"""
    explanations = {
        "text": {
            "high": "Your text shows positive language patterns and emotional expression.",
            "moderate": "Your text shows some concerning patterns but also positive elements.",
            "low": "Your text contains language patterns that may indicate distress or difficulty."
        },
        "voice": {
            "high": "Your voice patterns suggest normal energy and expression levels.",
            "moderate": "Your voice patterns show some indicators that may suggest mood changes.",
            "low": "Your voice patterns may indicate low energy or emotional distress."
        }
    }
    
    if score >= 6.0:
        level = "high"
    elif score >= 4.0:
        level = "moderate"
    else:
        level = "low"
    
    return explanations.get(score_type, {}).get(level, "Analysis completed.")
