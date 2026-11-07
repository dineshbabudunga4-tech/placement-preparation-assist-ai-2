import re

class CompanyResumeOptimizer:
    def __init__(self):
        # Define keywords companies look for
        self.company_keywords = {
            'TCS': ['java', 'sql', 'communication', 'aptitude', 'teamwork'],
            'Infosys': ['python', 'java', 'sql', 'agile', 'problem solving'],
            'Google': ['algorithms', 'data structures', 'system design', 'python', 'c++'],
            'Amazon': ['leadership', 'customer obsession', 'data structures', 'java', 'aws'],
            'Microsoft': ['c#', 'azure', 'algorithms', 'problem solving', 'teamwork']
        }
        
        # Common action verbs
        self.action_verbs = ['developed', 'managed', 'led', 'created', 'designed', 'implemented', 'optimized', 'built', 'solved']

    def analyze_resume(self, resume_text, company_name):
        resume_lower = resume_text.lower()
        
        # 1. Action Verbs Score
        found_verbs = [verb for verb in self.action_verbs if verb in resume_lower]
        verb_score = min(100, (len(found_verbs) / 5) * 100) # 5 verbs = 100%

        # 2. Metrics/Numbers Score (Looking for % or numbers like "20%", "50 users")
        metrics_matches = re.findall(r'\b\d+(?:\.\d+)?%?\b', resume_text)
        metrics_score = min(100, (len(metrics_matches) / 4) * 100) # 4 metrics = 100%

        # 3. Technical Keywords Score
        target_keywords = self.company_keywords.get(company_name.title(), ['python', 'java', 'sql', 'communication'])
        found_keywords = [kw for kw in target_keywords if kw in resume_lower]
        keyword_score = min(100, (len(found_keywords) / len(target_keywords)) * 100) if target_keywords else 0

        # 4. Calculate Overall ATS Score
        overall_score = (verb_score * 0.3) + (metrics_score * 0.3) + (keyword_score * 0.4)

        # 5. Generate Suggestions
        suggestions = []
        missing_keywords = [kw for kw in target_keywords if kw not in found_keywords]
        
        if verb_score < 50:
            suggestions.append("Use more action verbs (e.g., Developed, Led, Optimized) to describe your work.")
        if metrics_score < 50:
            suggestions.append("Add quantifiable metrics (e.g., 'Improved efficiency by 20%').")
        if missing_keywords:
            suggestions.append(f"Add missing keywords for {company_name}: {', '.join(missing_keywords)}")

        return {
            'ats_score': round(overall_score, 1),
            'readiness_score': round(overall_score + 10, 1), # Mock readiness score
            'scores': {
                'action_verbs': round(verb_score, 1),
                'metrics': round(metrics_score, 1),
                'keywords': round(keyword_score, 1)
            },
            'missing_keywords': missing_keywords if missing_keywords else ['None detected - Great job!'],
            'suggestions': suggestions if suggestions else ['Your resume looks great for this company!']
        }

    def get_improvement_suggestions(self, analysis_result, company_name):
        return analysis_result.get('suggestions', [])

    def generate_optimized_resume(self, resume_data, company_name, analysis_result):
        # This takes the user's basic resume data and injects the missing keywords
        missing_kws = analysis_result.get('missing_keywords', [])
        
        # Create a new summary emphasizing the missing keywords
        old_summary = resume_data.get('summary', '')
        new_summary = f"{old_summary}\n\nOptimized for {company_name}: Experienced with {', '.join(missing_kws)}."
        
        # Add missing keywords to skills
        current_skills = resume_data.get('skills', [])
        new_skills = list(set(current_skills + missing_kws))

        return {
            'summary': new_summary,
            'skills': new_skills,
            'projects': resume_data.get('projects', [])
        }

    def compare_companies(self, resume_data, companies):
        comparisons = []
        dummy_text = " ".join(str(v) for v in resume_data.values())
        for comp in companies:
            res = self.analyze_resume(dummy_text, comp)
            comparisons.append({
                'company': comp,
                'score': res['ats_score'],
                'missing': res['missing_keywords']
            })
        comparisons.sort(key=lambda x: x['score'], reverse=True)
        return comparisons