<script setup>
import { ref, computed } from 'vue'
import { SUPPORTED_SOURCES } from '../constants/sources'

const props = defineProps({
  existingNames: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['site-added'])

const selectedName = ref('')

// Only offer sources that are actually supported AND not already registered,
// so users can't pick from a list of arbitrary/unsupported feeds or add
// duplicates.
const availableSources = computed(() =>
  SUPPORTED_SOURCES.filter(source => !props.existingNames.includes(source.name))
)

function handleAdd() {
  if (!selectedName.value) return

  const source = SUPPORTED_SOURCES.find(s => s.name === selectedName.value)
  if (!source) return

  emit('site-added', {
    name: source.name,
    url: source.url,
    category: source.category
  })

  selectedName.value = ''
}
</script>

<template>
  <div class="card">
    <div class="card-header">
      <h2>Register Pipeline Feed Stream</h2>
      <p class="subtitle">
        Connect automated targets via remote XML/RSS protocols
      </p>
    </div>

    <form v-if="availableSources.length > 0" @submit.prevent="handleAdd" class="form">
      <div class="field">
        <label>Available Source</label>

        <select v-model="selectedName" required>
          <option value="" disabled>Select a source&hellip;</option>
          <option
            v-for="source in availableSources"
            :key="source.name"
            :value="source.name"
          >
            {{ source.name }}
          </option>
        </select>
      </div>

      <div class="field button-field">
        <button type="submit" class="btn-primary" :disabled="!selectedName">
          Add Pipeline Stream
        </button>
      </div>
    </form>

    <p v-else class="all-added">
      All supported sources have already been added.
    </p>
  </div>
</template>

<style scoped>
.card-header {
  padding: 24px;
  padding-bottom: 0;
}

.card-header h2 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}

.subtitle {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 24px;
}

.form {
  padding: 0 24px 24px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 20px;
  align-items: end;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text);
}

.field select {
  width: 100%;
  height: 46px;
  padding: 0 14px;
  border: 1px solid var(--border);
  border-radius: 4px;
  font-size: 15px;
  font-family: 'Inter', sans-serif;
  background: #fff;
  transition: border-color 0.2s ease;
}

.field select:focus {
  outline: none;
  border-color: var(--primary);
}

.button-field {
  justify-content: flex-end;
}

.btn-primary {
  height: 46px;
  padding: 0 24px;
  background: #1b1464;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  white-space: nowrap;
  transition: background 0.2s ease;
}

.btn-primary:hover:not(:disabled) {
  background: #130d43;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.all-added {
  padding: 24px;
  color: var(--text-muted);
  font-size: 14px;
}

@media (max-width: 700px) {
  .form {
    grid-template-columns: 1fr;
  }

  .button-field {
    justify-content: stretch;
  }

  .btn-primary {
    width: 100%;
  }
}
</style>