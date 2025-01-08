<template>
    <div class="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <div>
        <Navbar />
      </div>
      
      <main class="container mx-auto px-4 pt-20">
        <div class="flex flex-col items-center text-center">
          
          <h2 class="text-5xl font-bold text-gray-900 mb-6">
            CrunchBot Customer Support, <span class="text-blue-600">Simplified</span>
          </h2>
          
          <p class="text-xl text-gray-600 mb-8 max-w-2xl">
            Empower your support team with AI-driven insights and automated 
            responses while maintaining the human touch your customers love.
          </p>
  
          <NuxtLink 
            to="/login" 
            class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-lg transition-colors"
          >
            Get Started
          </NuxtLink>
        </div>
  
      </main>
    </div>
  </template>
  