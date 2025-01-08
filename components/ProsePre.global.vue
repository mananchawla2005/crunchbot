<script setup lang="ts">
const props = defineProps({
  code: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: null
  },
  filename: {
    type: String,
    default: null
  },
  highlights: {
    type: Array as () => number[],
    default: () => []
  },
  meta: {
    type: String,
    default: null
  },
  class: {
    type: String,
    default: null
  }
})

const codeCopied = ref<boolean>(false);

const copyCode = (): void => {
  navigator.clipboard.writeText(props.code)
      .then(() => {
        codeCopied.value = true;
        setTimeout(function () {
          codeCopied.value = false;
        }, 5000);
      })
      .catch((e) => {
        console.error('Error: Unable to copy code.');
      });
}
</script>
<template>
    <div class="pre">
      <div class="pre-head">
        <div class="pre-head-left">
          <span v-if="props.language" class="language-label">{{ language }}</span>
          <span v-if="props.filename" class="filename">
            <i>{{ filename }}</i>
          </span>
        </div>
        <div class="pre-head-right">
          <span v-if="codeCopied" class="copy-success"><i>Copied</i></span>
          <button v-if="!codeCopied" class="copy-btn" @click="copyCode">Copy</button>
        </div>
      </div>
      <pre class="pre-body" :class="$props.class"><slot/></pre>
    </div>
  </template>
  
  <style scoped>
.pre {
  border: 1px solid #e2e8f0;
  border-radius: 0 0 0.375rem 0.375rem; 
  overflow: hidden;
}

.pre-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.25rem 0.75rem; 
  background-color: #1e293b;  
  border-bottom: 1px solid #334155;
}

.language-label {
  font-family: ui-monospace, monospace;
  font-size: 0.75rem; 
  color: #94a3b8; 
}

.filename {
  color: #94a3b8;
  font-size: 0.75rem;
}

.copy-btn {
  padding: 0.15rem 0.5rem; 
  font-size: 0.75rem;
  border-radius: 0.25rem;
  background-color: transparent;
  border: 1px solid #475569;
  color: #94a3b8;
  cursor: pointer;
  transition: all 0.2s;
}

.copy-btn:hover {
  background-color: #334155;
}

.copy-success {
  color: #4ade80; 
  font-size: 0.75rem;
}
  
.pre-body {
margin: 0;
border-radius: 0 !important;
padding: 1rem;
}
  </style>