<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

const props = defineProps({
  nodes: {
    type: Array,
    default: () => [],
  },
  selectedSourceName: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['select'])

const rotation = ref(18)
let animationFrameId = 0

const globeSize = 220
const globeRadius = 74
const globeCenter = globeSize / 2
const perspective = 480

function toCartesian(lat, lng, radius) {
  const latitude = (lat * Math.PI) / 180
  const longitude = (lng * Math.PI) / 180

  return {
    x: radius * Math.cos(latitude) * Math.cos(longitude),
    y: radius * Math.sin(latitude),
    z: radius * Math.cos(latitude) * Math.sin(longitude),
  }
}

function rotateY(point, angleDegrees) {
  const angle = (angleDegrees * Math.PI) / 180
  const cos = Math.cos(angle)
  const sin = Math.sin(angle)

  return {
    x: point.x * cos - point.z * sin,
    y: point.y,
    z: point.x * sin + point.z * cos,
  }
}

function rotateX(point, angleDegrees) {
  const angle = (angleDegrees * Math.PI) / 180
  const cos = Math.cos(angle)
  const sin = Math.sin(angle)

  return {
    x: point.x,
    y: point.y * cos - point.z * sin,
    z: point.y * sin + point.z * cos,
  }
}

const projectedNodes = computed(() => {
  return props.nodes.map((node) => {
    const basePoint = toCartesian(node.lat, node.lng, globeRadius)
    const rotated = rotateX(rotateY(basePoint, rotation.value), 18)
    const scale = perspective / (perspective - rotated.z)
    const x = globeCenter + rotated.x * scale
    const y = globeCenter + rotated.y * scale

    return {
      ...node,
      x,
      y,
      scale,
      depth: rotated.z,
      pulseColor: node.status === 'green' ? '#34a853' : '#ea4335',
      selected: node.source_name === props.selectedSourceName,
    }
  })
})

function startSpin() {
  const tick = () => {
    rotation.value = (rotation.value + 0.12) % 360
    animationFrameId = window.requestAnimationFrame(tick)
  }

  animationFrameId = window.requestAnimationFrame(tick)
}

function stopSpin() {
  if (animationFrameId) {
    window.cancelAnimationFrame(animationFrameId)
  }
}

function handleNodeClick(node) {
  emit('select', node)
}

onMounted(startSpin)
onBeforeUnmount(stopSpin)
</script>

<template>
  <section class="card globe-card">
    <header class="card-head">
      <div>
        <h2>Interactive 3D Target Globe</h2>
        <p class="card-subtitle">
          Click a source node to filter the dashboard in real time.
        </p>
      </div>

      <span class="status-pill">3 sources mapped</span>
    </header>

    <div class="globe-stage">
      <div class="globe-shell">
        <div class="globe-shadow" aria-hidden="true"></div>
        <div class="globe-grid" aria-hidden="true"></div>
        <div class="globe-grid globe-grid-vertical" aria-hidden="true"></div>

        <div class="globe-surface" aria-hidden="true"></div>

        <button
          v-for="node in projectedNodes"
          :key="node.source_name"
          class="node"
          :class="{
            active: node.selected,
            green: node.status === 'green',
            red: node.status !== 'green',
          }"
          :style="{
            left: `${node.x}px`,
            top: `${node.y}px`,
            zIndex: Math.round(node.depth + 1000),
            '--pulse-color': node.pulseColor,
            '--scale-factor': node.selected ? 1.35 : 1,
          }"
          type="button"
          @click="handleNodeClick(node)"
        >
          <span class="node-ring" aria-hidden="true"></span>
          <span class="node-dot" aria-hidden="true"></span>
          <span class="node-label">{{ node.source_name }}</span>
        </button>
      </div>

      <div class="globe-caption">
        <strong>Current focus:</strong>
        <span>{{ selectedSourceName || 'All sources' }}</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.globe-card {
  background: white;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

.card-head {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.card-head h2 {
  font-size: 16px;
  font-weight: 600;
}

.card-subtitle {
  color: var(--text-muted);
  font-size: 13px;
  margin-top: 4px;
}

.status-pill {
  font-size: 12px;
  color: var(--primary);
  background: #e8f0fe;
  border: 1px solid #d2e3fc;
  border-radius: 999px;
  padding: 4px 10px;
  font-weight: 600;
  flex-shrink: 0;
}

.globe-stage {
  padding: 12px 12px 10px;
  background: linear-gradient(180deg, #f8fbff 0%, #eef3fb 100%);
}

.globe-shell {
  position: relative;
  width: min(100%, 220px);
  aspect-ratio: 1;
  margin: 0 auto;
  border-radius: 50%;
  overflow: hidden;
  background:
    radial-gradient(circle at 50% 35%, rgba(255, 255, 255, 0.98) 0%, rgba(224, 235, 255, 0.96) 16%, rgba(25, 88, 214, 0.92) 38%, rgba(10, 42, 112, 0.98) 100%);
  box-shadow: 0 24px 60px rgba(13, 36, 92, 0.22);
}

.globe-shadow {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.15), transparent 54%);
  mix-blend-mode: screen;
}

.globe-surface {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background:
    radial-gradient(circle at 50% 50%, transparent 42%, rgba(255, 255, 255, 0.2) 42.5%, transparent 43%);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.15);
}

.globe-grid,
.globe-grid-vertical {
  position: absolute;
  inset: 14% 18%;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-left-color: transparent;
  border-right-color: transparent;
  opacity: 0.8;
}

.globe-grid-vertical {
  inset: 18% 14%;
  border-top-color: transparent;
  border-bottom-color: transparent;
  transform: rotate(24deg);
}

.node {
  position: absolute;
  transform: translate(-50%, -50%) scale(var(--scale-factor));
  border: none;
  background: transparent;
  cursor: pointer;
  color: white;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0;
  transition: transform 0.2s ease, opacity 0.2s ease;
  filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.18));
}

.node:hover {
  transform: translate(-50%, -50%) scale(1.15);
}

.node.active {
  transform: translate(-50%, -50%) scale(1.38);
}

.node-ring {
  position: absolute;
  inset: -11px;
  border-radius: 50%;
  border: 1px solid color-mix(in srgb, var(--pulse-color) 65%, white);
  animation: pulse-ring 1.6s ease-out infinite;
}

.node-dot {
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background: var(--pulse-color);
  box-shadow: 0 0 0 6px color-mix(in srgb, var(--pulse-color) 20%, transparent), 0 0 18px var(--pulse-color);
  animation: pulse-dot 1.6s ease-in-out infinite;
}

.node.green .node-dot {
  box-shadow: 0 0 0 6px rgba(52, 168, 83, 0.2), 0 0 18px rgba(52, 168, 83, 0.95);
}

.node.red .node-dot {
  box-shadow: 0 0 0 6px rgba(234, 67, 53, 0.2), 0 0 18px rgba(234, 67, 53, 0.95);
}

.node-label {
  position: relative;
  left: 4px;
  top: -16px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.2px;
  white-space: nowrap;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.35);
}

.globe-caption {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 18px;
  font-size: 13px;
  color: var(--text-muted);
}

.globe-caption strong {
  color: var(--text);
}

@keyframes pulse-ring {
  0% {
    transform: scale(0.9);
    opacity: 0.5;
  }
  70% {
    transform: scale(1.4);
    opacity: 0;
  }
  100% {
    transform: scale(1.4);
    opacity: 0;
  }
}

@keyframes pulse-dot {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
}

@media (max-width: 768px) {
  .card-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
