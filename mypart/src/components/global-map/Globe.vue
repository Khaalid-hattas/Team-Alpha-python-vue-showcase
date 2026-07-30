<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { GlobeScene } from './GlobeScene.js'

const props = defineProps({
  nodes: {
    type: Array,
    default: () => []
  },
  selectedSourceName: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['select'])

const canvasContainer = ref(null)
const globeCanvas = ref(null)
let globeEngineInstance = null

// Native low-level timing sequence tracking arrays
let clickCount = 0
let lastClickTime = 0

function handleResize() {
  if (!canvasContainer.value || !globeEngineInstance) return
  const w = canvasContainer.value.clientWidth
  const h = canvasContainer.value.clientHeight
  globeEngineInstance.resize(w, h)
}

// HIGH INTENSITY RAPID INTERACTION ACTION ROUTER
function handleCinemaInputInteraction(event) {
  event.preventDefault()
  
  const currentTime = Date.now()
  const timeDifference = currentTime - lastClickTime
  
  // If the time between clicks is short, increase count. Otherwise, reset to 1.
  if (timeDifference < 320) {
    clickCount++
  } else {
    clickCount = 1
  }
  
  lastClickTime = currentTime

  // Instantly route triggers based on the current rapid click sequence
  if (clickCount === 2) {
    console.log('Double Click Registered: Launching Particle Explosion Shockwave')
    if (globeEngineInstance) globeEngineInstance.triggerExplosion()
  } else if (clickCount >= 3) {
    console.log('Triple Click Registered: Disassembling Sphere Matrix Assemblies')
    if (globeEngineInstance) globeEngineInstance.triggerFractureCracking()
    clickCount = 0 // Flush click sequence track buffers
  }
}

function handleGlobeClick() {
  if (props.nodes.length > 0) {
    emit('select', props.nodes[0])
  }
}

watch(() => props.loading, (isLoading) => {
  if (globeEngineInstance) {
    globeEngineInstance.triggerExtractionState(isLoading)
  }
})

watch(() => props.nodes, (nodes) => {
  if (!globeEngineInstance) return

  const statuses = {}

  nodes.forEach(node => {
    statuses[node.source_name] = node.status === 'green'
  })

  globeEngineInstance.updateFromData(statuses)

}, { deep: true })

onMounted(() => {
  nextTick(() => {
    if (globeCanvas.value) {
      globeEngineInstance = new GlobeScene(globeCanvas.value)
      window.addEventListener('resize', handleResize)
      
      setTimeout(() => {
        handleResize()
        const statuses = {}

        props.nodes.forEach(node => {
  statuses[node.source_name] = node.status === 'green'
})

globeEngineInstance.updateFromData(statuses)
      }, 100)
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (globeEngineInstance) globeEngineInstance.destroy()
})
</script>

<template>
  <div class="card globe-container-card">
    <div class="card-header-inline">
      <div class="title-indicator-row">
        <span class="status-pulse-dot neon-glow"></span>
        <h3>Target Extraction Origins Map (3D Cyber Sphere)</h3>
      </div>
      <p class="caption-text">Interactive WebGL Matrix. Double-click anywhere on the viewport stage to explode the particles, or triple-click rapidly to shatter the grid assembly!</p>
    </div>

    <!-- Active Mouse Down event listener tracks interactions instantly across the screen -->
    <div 
      ref="canvasContainer" 
      class="canvas-viewport" 
      @mousedown="handleCinemaInputInteraction"
      @click="handleGlobeClick"
    >
      <canvas ref="globeCanvas" class="webgl-render-surface"></canvas>
    </div>
  </div>
</template>

<style scoped>
.globe-container-card {
  width: 100%;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

.card-header-inline {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border);
}

.title-indicator-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-pulse-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #00ffaa;
}

.neon-glow {
  box-shadow: 0 0 10px #00ffaa, 0 0 20px #00ffaa;
  animation: lightPulse 2s infinite ease-in-out;
}

@keyframes lightPulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.card-header-inline h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  margin: 0;
}

.caption-text {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 4px;
  margin-bottom: 0;
}

.canvas-viewport {
  width: 100%;
  height: 100%;
  min-height: 560px;
  position: relative;
  background: radial-gradient(circle at center, #111126 0%, #050512 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
}

.webgl-render-surface {
  width: 100% !important;
  height: 100% !important;
  display: block;
  outline: none;
}
</style>
