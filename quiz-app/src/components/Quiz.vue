<template>
    <div class="max-w-2xl mx-auto p-6">
      <!-- Loading State -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-400 mb-4"></div>
        <p class="text-xl text-blue-300 font-medium">Loading your quiz...</p>
      </div>
      
      <div v-else>
        <!-- Quiz in Progress -->
        <div v-if="!quizFinished" class="quiz-container">
          <!-- Progress Bar -->
          <div class="mb-6">
            <div class="flex justify-between text-sm mb-1">
              <span class="text-blue-300">Question {{ currentQuestionIndex + 1 }} of {{ questions.length }}</span>
              <span class="text-blue-300">{{ Math.round(((currentQuestionIndex) / questions.length) * 100) }}% Complete</span>
            </div>
            <div class="w-full bg-gray-700 rounded-full h-2.5">
              <div class="bg-blue-500 h-2.5 rounded-full" :style="`width: ${(currentQuestionIndex / questions.length) * 100}%`"></div>
            </div>
          </div>
          
          <!-- Question Card -->
          <div class="bg-gradient-to-br from-gray-800 to-gray-900 border border-blue-500 shadow-xl rounded-lg p-8 transition-all duration-300 hover:shadow-blue-500/20">
            <h2 class="text-2xl font-bold mb-6 text-blue-200 leading-tight">
              {{ currentQuestion.question_text }}
            </h2>
            <ul class="space-y-4">
              <li v-for="(answer, index) in currentQuestion.answers" :key="index" class="transform transition-all duration-200 hover:scale-102">
                <button 
                  @click="selectAnswer(index)" 
                  class="w-full text-left px-6 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 transition-colors rounded-lg shadow-lg text-white font-medium flex items-center"
                >
                  <span class="w-8 h-8 flex items-center justify-center bg-blue-800 rounded-full mr-3 text-sm font-bold">
                    {{ String.fromCharCode(65 + index) }}
                  </span>
                  <span>{{ answer }}</span>
                </button>
              </li>
            </ul>
          </div>
        </div>
        
        <!-- Quiz Results -->
        <div v-else class="mt-8">
          <!-- Score Card -->
          <div class="bg-gradient-to-br from-gray-800 to-gray-900 border-2 border-green-500 rounded-lg p-8 mb-8 shadow-xl text-center">
            <div class="inline-flex items-center justify-center mb-4">
              <div class="relative">
                <svg class="w-24 h-24" viewBox="0 0 36 36">
                  <path 
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
                    fill="none" 
                    stroke="#27ae60" 
                    stroke-width="3"
                    stroke-dasharray="100, 100"
                  />
                  <path 
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
                    fill="none" 
                    stroke="#4ade80" 
                    stroke-width="3"
                    :stroke-dasharray="`${(score / questions.length) * 100}, 100`"
                  />
                </svg>
                <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-white text-xl font-bold">
                  {{ Math.round((score / questions.length) * 100) }}%
                </div>
              </div>
            </div>
            <p class="text-3xl font-bold text-green-400 mb-2">
              Quiz Completed!
            </p>
            <p class="text-xl text-green-300">
              Your score: <span class="font-bold">{{ score }}</span> / {{ questions.length }}
            </p>
            <button @click="restartQuiz" class="mt-6 px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition-colors shadow-lg">
              Try Again
            </button>
          </div>
          
          <!-- Answer Review -->
          <div>
            <h3 class="text-2xl font-semibold mb-6 text-blue-100 border-b border-blue-800 pb-2">Review Your Answers</h3>
            <div v-for="(item, index) in userAnswers" :key="index" 
                 class="mb-6 p-6 border rounded-lg shadow-lg transition-all duration-300"
                 :class="item.correct ? 'border-green-500 bg-green-900/20' : 'border-red-500 bg-red-900/20'"
            >
              <div class="flex items-start">
                <div :class="[
                  'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center mr-3 font-bold',
                  item.correct ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
                ]">
                  {{ index + 1 }}
                </div>
                <div class="flex-grow">
                  <p class="font-bold text-lg mb-3" :class="item.correct ? 'text-green-300' : 'text-red-300'">
                    {{ item.question.question_text }}
                  </p>
                  <div class="pl-4 border-l-2 border-gray-700 mb-3">
                    <p class="mb-1 text-sm text-gray-400">Your answer:</p>
                    <p :class="{'text-green-400 font-medium': item.correct, 'text-red-400 font-medium': !item.correct}">
                      {{ item.question.answers[item.selectedIndex] }}
                    </p>
                  </div>
                  <div v-if="!item.correct" class="pl-4 border-l-2 border-green-700">
                    <p class="mb-1 text-sm text-gray-400">Correct answer:</p>
                    <p class="text-green-400 font-medium">
                      {{ item.question.answers[item.question.correct_answer] }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "Quiz",
    data() {
      return {
        questions: [],
        currentQuestionIndex: 0,
        score: 0,
        quizFinished: false,
        loading: true,
        userAnswers: [] // Store user's answers for review
      };
    },
    computed: {
      currentQuestion() {
        return this.questions[this.currentQuestionIndex];
      }
    },
    methods: {
      selectAnswer(selectedIndex) {
        const current = this.currentQuestion;
        const correct = selectedIndex === current.correct_answer;
        if (correct) {
          this.score++;
        }
        this.userAnswers.push({
          question: current,
          selectedIndex,
          correct
        });
        if (this.currentQuestionIndex < this.questions.length - 1) {
          this.currentQuestionIndex++;
        } else {
          this.quizFinished = true;
        }
      },
      fetchQuestions() {
        fetch('http://localhost:8000/api/questions/')
          .then(response => response.json())
          .then(data => {
            this.questions = data;
            this.loading = false;
          })
          .catch(err => {
            console.error("Error fetching questions:", err);
            this.loading = false;
          });
      },
      restartQuiz() {
        this.currentQuestionIndex = 0;
        this.score = 0;
        this.quizFinished = false;
        this.userAnswers = [];
      }
    },
    mounted() {
      this.fetchQuestions();
    }
  };
  </script>
  
  <style>
  .quiz-container {
    animation: fadeIn 0.5s ease-in-out;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  .hover\:scale-102:hover {
    transform: scale(1.02);
  }
  </style>