<script setup>
definePageMeta({
    middleware: ["protected"]
});

import { ref, nextTick } from 'vue';

const user = useUser();
const messages = ref([]);
const newMessage = ref('');
const isLoading = ref(false);
const chatContainer = ref(null);
const isSidebarOpen = ref(false);
const messageTextarea = ref(null);

const selectedFile = ref(null);
const fileInputElem = ref(null);

function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file && file.type === 'application/pdf') {
    selectedFile.value = file;
  } else {
    alert('Please select a PDF file');
    event.target.value = '';
  }
}

function clearSelectedFile() {
  selectedFile.value = null;
  if (fileInputElem.value) {
    fileInputElem.value.value = '';
  }
}

function toggleSidebar() {
  isSidebarOpen.value = !isSidebarOpen.value;
}

function createChatMessage(role, content) {
    if (role !== 'user' && role !== 'model') {
        console.warn('Invalid role specified:', role);
        role = 'user'; 
    }
    return {
        role: role,
        content: content,
        timestamp: new Date().toISOString()
    };
}

async function sendMessage() {
    if (!newMessage.value.trim()) return;

    messages.value.push(createChatMessage('user', newMessage.value));
    newMessage.value = '';
    isLoading.value = true;

    const aiResponse = await $fetch("/api/query", {
        method: "POST",
        body: {
            conversation: messages.value
        }
    });

    messages.value.push(createChatMessage('model', aiResponse));
    isLoading.value = false;

    await nextTick();

    if (messageTextarea.value) {
        messageTextarea.value.style.height = '42px';
    }

    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
}

async function logout() {
    await $fetch("/api/logout", { method: "POST" });
    await navigateTo("/login");
}

function formatTime(timestamp) {
    return new Date(timestamp).toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

const inputHeight = ref('auto');

function handleInput(event) {
    const textarea = event.target;
    textarea.style.height = 'auto';
    const newHeight = Math.min(textarea.scrollHeight, 120);
    textarea.style.height = `${newHeight}px`;
}

function handleKeydown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function triggerFileInput() {
    if (fileInputElem.value) {
        fileInputElem.value.click();
    }
}
</script>

<template>
    <div class="flex h-screen bg-gray-50">
      <div :class="{'hidden': !isSidebarOpen, 'md:block': true, 'md:w-80': true, 'lg:w-96': true, 'bg-gradient-to-b': true, 'from-slate-800': true, 'to-slate-900': true, 'text-white': true}">
        <div class="p-6 border-b border-slate-700/50">
          <h2 class="text-xl font-bold tracking-tight truncate">{{ user.name }}</h2>
          <p class="text-sm text-slate-400 mt-1 truncate">ID: {{ user.id }}</p>
        </div>
        <div class="p-6">
          <button @click="logout"
            class="w-full px-4 py-3 text-sm font-medium text-slate-300 border border-slate-700 rounded-xl
                   hover:bg-slate-700/50 transition-colors duration-200
                   focus:outline-none focus:ring-2 focus:ring-slate-400 focus:ring-offset-2 focus:ring-offset-slate-800">
            Sign out
          </button>
        </div>
      </div>

      <div class="flex-1 flex flex-col bg-white">
        <div class="px-4 md:px-6 py-4 border-b border-gray-100 bg-white flex justify-between items-center">
          <button class="md:hidden p-2 hover:bg-gray-100 rounded-lg" @click="toggleSidebar">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <h1 class="text-xl font-bold text-gray-800">Chat Session ( CrunchBot )</h1>
          <div class="md:hidden">
            <button @click="logout" class="p-2 hover:bg-gray-100 rounded-lg text-gray-600">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>

        <div ref="chatContainer"
          class="flex-1 overflow-y-auto p-3 md:p-6 space-y-4 bg-gradient-to-b from-gray-50 to-white">
          <template v-for="message in messages" :key="message.timestamp">
            <div v-if="message.role === 'user'" class="flex flex-col items-end space-y-1 w-full">
              <span class="text-xs font-semibold text-gray-500 mr-2">YOU</span>
              <div class="flex items-end justify-end w-full">
                <div class="bg-gradient-to-r from-blue-600 to-blue-700 text-white 
                  rounded-2xl rounded-tr-none py-2 md:py-3 px-3 md:px-4
                  shadow-sm hover:shadow-md transition-all duration-200
                  border border-blue-500/10
                  max-w-[85%] md:max-w-[70%] min-w-[60px] w-fit">
                  <MDC class="prose prose-white text-sm md:text-base" :value="message.content" />
                </div>
              </div>
              <span class="text-xs text-gray-400 mr-2 font-medium">
                {{ formatTime(message.timestamp) }}
              </span>
            </div>

            <div v-else-if="message.role === 'model'" class="flex flex-col items-start space-y-1 w-full">
              <span class="text-xs font-semibold text-gray-500 ml-2">AI</span>
              <div class="flex items-start w-full">
                <div class="bg-white text-gray-800 rounded-2xl rounded-tl-none 
                  py-2 md:py-3 px-3 md:px-4 shadow-sm hover:shadow-md 
                  transition-all duration-200 border border-gray-100
                  max-w-[85%] md:max-w-[70%] min-w-[60px] w-fit">
                  <MDC class="prose text-sm md:text-base" :value="message.content" />
                </div>
              </div>
              <span class="text-xs text-gray-400 ml-2 font-medium">
                {{ formatTime(message.timestamp) }}
              </span>
            </div>
          </template>

          <div v-if="isLoading" class="flex justify-start">
            <div class="bg-white text-gray-800 rounded-2xl rounded-tl-none 
              py-2 md:py-3 px-3 md:px-4 shadow-sm border border-gray-100">
              <div class="flex space-x-2">
                <div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce delay-150"></div>
                <div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce delay-300"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="p-3 md:p-4 bg-white border-t border-gray-100">
          <div v-if="selectedFile" class="mb-2 p-2 bg-blue-50 rounded-lg flex justify-between items-center">
            <div class="flex items-center">
              <svg class="w-5 h-5 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
              <span class="text-sm text-blue-700 truncate max-w-[200px]">{{ selectedFile.name }}</span>
            </div>
            <button @click="clearSelectedFile" class="text-blue-600 hover:text-blue-800">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

		  <form @submit.prevent="sendMessage"
				class="flex items-center space-x-2 md:space-x-3 bg-gray-50 p-2 rounded-xl border border-gray-100">
				
				<input
					ref="fileInputElem"
					type="file"
					accept=".pdf"
					@change="handleFileSelect"
					class="hidden"
				/>
				<button
					type="button"
					@click="triggerFileInput"
					class="p-2 text-gray-500 hidden hover:text-blue-600 focus:outline-none"
					:disabled="isLoading"
				>
					<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
					</svg>
				</button>

				<textarea 
					ref="messageTextarea"
					v-model="newMessage" 
					@input="handleInput"
					@keydown="handleKeydown"
					placeholder="Type your message..." 
					class="flex-1 px-3 md:px-4 py-2 md:py-2.5 bg-transparent text-gray-800 placeholder-gray-400
					focus:outline-none text-sm md:text-base resize-none overflow-y-auto
					min-h-[42px] max-h-[120px]"
					rows="1"
					:disabled="isLoading"
				></textarea>

				<button type="submit" class="px-4 md:px-5 py-2 md:py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 text-white font-medium
					rounded-lg hover:from-blue-700 hover:to-blue-800 transform hover:scale-[1.02]
					transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 
					focus:ring-offset-2 shadow-sm hover:shadow-md text-sm md:text-base"
					:disabled="isLoading">
					Send
				</button>
			</form>
        </div>
      </div>
    </div>
</template>