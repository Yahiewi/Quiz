# quiz/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Question, SUBJECT_CHOICES
from .serializers import QuestionSerializer
import requests
import json
import os
import random

class QuestionList(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class GenerateQuizView(APIView):
    def post(self, request):
        # Get parameters from request
        subject = request.data.get('subject', random.choice([choice[0] for choice in SUBJECT_CHOICES]))
        num_questions = min(int(request.data.get('num_questions', 5)), 10)  # Limit to 10 questions max
        
        # Using DeepSeek API (free tier)
        try:
            questions = self.generate_questions_with_deepseek(subject, num_questions)
            return Response(questions, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to generate questions: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def generate_questions_with_deepseek(self, subject, num_questions):
        # DeepSeek API key - in production use environment variables
        api_key = os.environ.get("DEEPSEEK_API_KEY", "your_deepseek_api_key")
        
        # API endpoint
        url = "https://api.deepseek.com/v1/chat/completions"
        
        # Prepare the prompt for question generation
        prompt = f"""
        Generate {num_questions} quiz questions about {subject}. 
        
        Each question should:
        1. Be challenging but answerable with typical knowledge of {subject}
        2. Have exactly 4 multiple-choice answers with one correct answer
        3. Include an explanation for why the correct answer is correct
        4. Be formatted as a valid JSON array with objects in this exact structure:
        
        [
        {{
            "question_text": "The question here?",
            "answers": ["Answer A", "Answer B", "Answer C", "Answer D"],
            "correct_answer": 0,  // Index of correct answer (0-3)
            "explanation": "Explanation for why the correct answer is correct.",
            "subject": "{subject}"
        }},
        // More questions...
        ]
        
        The response should be ONLY the JSON array, nothing else.
        """
        
        # Prepare the request payload
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        # Set headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Make the API request
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}: {response.text}")
        
        # Parse the response
        try:
            response_data = response.json()
            content = response_data['choices'][0]['message']['content']
            
            # Direct JSON parsing - the content itself is valid JSON
            questions = json.loads(content)
            
            # Validate the structure
            self.validate_questions(questions)
            
            return questions
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse LLM response as JSON: {str(e)}, Content: {content[:100]}...")

    def validate_questions(self, questions):
        """Validate the structure of generated questions"""
        if not isinstance(questions, list):
            raise Exception("Generated content is not a list")
        
        for q in questions:
            if not isinstance(q, dict):
                raise Exception("Question is not a dictionary")
            if "question_text" not in q or "answers" not in q or "correct_answer" not in q or "explanation" not in q:
                raise Exception("Question is missing required fields")
            if not isinstance(q["answers"], list) or len(q["answers"]) != 4:
                raise Exception("Answers should be a list of exactly 4 items")
            if not isinstance(q["correct_answer"], int) or q["correct_answer"] < 0 or q["correct_answer"] > 3:
                raise Exception("correct_answer should be an integer between 0 and 3")