<script setup lang="ts">
import Quiz from './components/Quiz.vue'
</script>

<template>
  <div class="app-container bg-gradient-to-br from-gray-900 via-blue-900 to-gray-800 min-h-screen flex flex-col items-center justify-center text-white font-sans">
    <!-- Header with animated effect -->
    <div class="mb-8 text-center">
      <div class="relative">
        <h1 class="text-4xl md:text-5xl font-extrabold drop-shadow-glow tracking-tight mb-2">
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
            Interactive Quiz Lab
          </span>
        </h1>
        <div class="absolute -bottom-1 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-blue-500 to-transparent"></div>
      </div>
      <p class="text-blue-300 text-lg mt-2">Test your knowledge with interactive questions</p>
    </div>
    
    <!-- Main quiz component with card effect -->
    <div class="w-full max-w-6xl backdrop-blur-sm bg-gray-900/50 rounded-xl p-1 shadow-glow-blue">
      <Quiz />
    </div>
    
    <!-- Footer -->
    <div class="mt-8 text-center text-blue-300 text-sm opacity-80">
      <p>Made with ❤️ for knowledge seekers</p>
    </div>
  </div>
</template>

<style>
.app-container {
  background-size: 400% 400%;
  animation: gradientAnimation 15s ease infinite;
}

@keyframes gradientAnimation {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.drop-shadow-glow {
  filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.5));
}

.shadow-glow-blue {
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
}

/* Import a modern font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
}
</style>