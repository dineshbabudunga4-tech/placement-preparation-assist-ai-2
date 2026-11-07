from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class GroupDiscussionML:
    def __init__(self):
        pass

    def evaluate_relevance(self, user_answer, target_text):
        if not user_answer or len(user_answer.split()) < 10:
            return 0
        
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform([user_answer, target_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            score = min(100, int(similarity * 150)) 
            return score
        except Exception as e:
            print(f"ML Error: {e}")
            return 0

    def get_structured_feedback(self, user_answer, target_text, score):
        answer_lower = user_answer.lower()
        target_words = set([w.lower() for w in re.findall(r'\b\w+\b', target_text) if len(w) > 4])
        missing_words = [kw for kw in target_words if kw not in answer_lower]
        
        feedback = ""
        if score >= 80:
            feedback = "Excellent! Your answer is highly relevant and well-articulated."
        elif score >= 50:
            feedback = "Good answer. You touched on some key points, but could be more specific."
        else:
            feedback = "Your answer needs improvement. Try to include more relevant keywords."
            
        if missing_words and score < 80:
            feedback += f" Consider mentioning concepts related to: {', '.join(list(missing_words)[:3])}."
            
        return feedback

gd_ml = GroupDiscussionML()