import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask, request, jsonify

# Initialize NLTK's Vader sentiment analyzer
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

app = Flask(__name__)

@app.route('/predict-emotion', methods=['POST'])
def predict_emotion():
    data = request.get_json()
    text = data['text']
    
    # Analyze sentiment of input text
    sentiment_scores = sid.polarity_scores(text)
    
    # Determine emotional state based on sentiment scores
    if sentiment_scores['compound'] >= 0.05:
        emotion = 'positive'
    elif sentiment_scores['compound'] <= -0.05:
        emotion = 'negative'
    else:
        emotion = 'neutral'
    
    # Generate personalized recommendations based on emotional state
    recommendations = get_recommendations(emotion)
    
    return jsonify({
        'emotion': emotion,
        'recommendations': recommendations
    })

def get_recommendations(emotion):
    if emotion == 'positive':
        return ['Practice gratitude journaling', 'Engage in physical activity', 'Connect with friends or family']
    elif emotion == 'negative':
        return ['Practice deep breathing exercises', 'Take a short break and engage in a calming activity', 'Seek support from a trusted person']
    else:
        return ['Practice mindfulness meditation', 'Engage in a creative hobby', 'Take a moment to focus on the present']

if __name__ == '__main__':
    app.run(debug=True)
