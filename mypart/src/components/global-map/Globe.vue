<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from "vue";
import { GlobeScene } from "./GlobeScene.js";

const props = defineProps({
  nodes: {
    type: Array,
    default: () => [],
  },
  selectedSourceName: {
    type: String,
    default: "",
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["select"]);

const canvasContainer = ref(null);
const globeCanvas = ref(null);
let globeEngineInstance = null;

// Native low-level timing sequence tracking arrays
let clickCount = 0;
let lastClickTime = 0;

function handleResize() {
  if (!canvasContainer.value || !globeEngineInstance) return;
  const w = canvasContainer.value.clientWidth;
  const h = canvasContainer.value.clientHeight;
  globeEngineInstance.resize(w, h);
}

// HIGH INTENSITY RAPID INTERACTION ACTION ROUTER
function handleCinemaInputInteraction(event) {
  event.preventDefault();

  const currentTime = Date.now();
  const timeDifference = currentTime - lastClickTime;

  // If the time between clicks is short, increase count. Otherwise, reset to 1.
  if (timeDifference < 320) {
    clickCount++;
  } else {
    clickCount = 1;
  }

  lastClickTime = currentTime;

  // Instantly route triggers based on the current rapid click sequence
  if (clickCount === 2) {
    console.log(
      "Double Click Registered: Launching Particle Explosion Shockwave"
    );
    if (globeEngineInstance) globeEngineInstance.triggerExplosion();
  } else if (clickCount >= 3) {
    console.log(
      "Triple Click Registered: Disassembling Sphere Matrix Assemblies"
    );
    if (globeEngineInstance) globeEngineInstance.triggerFractureCracking();
    clickCount = 0; // Flush click sequence track buffers
  }
}

function handleGlobeClick(event) {
  if (!globeEngineInstance) return;

  try {
    const pickedNode = globeEngineInstance.pickNode(event.clientX, event.clientY);

    if (!pickedNode) return;

    // Fuzzy match source name to prevent silent failures on backend naming discrepancies
    const selected = props.nodes.find(
      (node) =>
        node.source_name &&
        node.source_name.toLowerCase() === String(pickedNode.id).toLowerCase()
    );

    if (selected) {
      emit("select", selected);
    } else {
      // Fallback emit if nodes prop isn't fully populated yet
      emit("select", { source_name: pickedNode.id, status: pickedNode.success ? "green" : "red" });
    }
  } catch (err) {
    console.error("Error handling globe node pick:", err);
  }
}

// Watch extraction loading state changes
watch(
  () => props.loading,
  (isLoading) => {
    if (globeEngineInstance) {
      globeEngineInstance.triggerExtractionState(isLoading);
    }
  }
);

// Watch incoming node data updates
watch(
  () => props.nodes,
  (nodes) => {
    if (!globeEngineInstance || !Array.isArray(nodes)) return;

    const statuses = {};

    nodes.forEach((node) => {
      if (node && node.source_name) {
        statuses[node.source_name] = node.status === "green";
      }
    });

    globeEngineInstance.updateFromData(statuses);
  },
  { deep: true }
);

onMounted(() => {
  nextTick(() => {
    if (globeCanvas.value) {
      try {
        globeEngineInstance = new GlobeScene(globeCanvas.value);
        window.addEventListener("resize", handleResize);

        setTimeout(() => {
          handleResize();
          const statuses = {};

          if (Array.isArray(props.nodes)) {
            props.nodes.forEach((node) => {
              if (node && node.source_name) {
                statuses[node.source_name] = node.status === "green";
              }
            });
          }

          globeEngineInstance.updateFromData(statuses);
        }, 100);
      } catch (err) {
        console.error("Failed to initialize 3D Globe Scene:", err);
      }
    }
  });
});

onUnmounted(() => {
  window.removeEventListener("resize", handleResize);
  if (globeEngineInstance) {
    globeEngineInstance.destroy();
    globeEngineInstance = null;
  }
});
</script>

<template>
  <div class="card globe-container-card">
    <div class="card-header-inline">
      <div class="title-indicator-row">
        <span class="status-pulse-dot neon-glow"></span>
        <h3>Target Extraction Origins Map (3D Cyber Sphere)</h3>
      </div>
      <p class="caption-text">
        Interactive WebGL Matrix. Double-click anywhere on the viewport stage to
        explode the particles, or triple-click rapidly to shatter the grid
        assembly!
      </p>
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
  border: 1px solid var(--border, #e2e8f0);
  border-radius: 8px;
  overflow: hidden;
}

.card-header-inline {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border, #e2e8f0);
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
  box-shadow:
    0 0 10px #00ffaa,
    0 0 20px #00ffaa;
  animation: lightPulse 2s infinite ease-in-out;
}

@keyframes lightPulse {
  0%,
  100% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
}

.card-header-inline h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text, #0f172a);
  margin: 0;
}

.caption-text {
  font-size: 12px;
  color: var(--text-muted, #64748b);
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
