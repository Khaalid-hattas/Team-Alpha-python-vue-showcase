import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

export class GlobeScene {
  constructor(canvas) {
    this.canvas = canvas
    this.width = canvas.clientWidth
    this.height = canvas.clientHeight
    this.nodeMeshes = []
    this.animationFrameId = null
    this.clock = new THREE.Clock()
    
    // Physics interaction configurations
    this.globeState = 'NORMAL' // NORMAL, EXPLODED, CRACKED
    this.stateTimer = 0

    this.targetNodesData = [
      { id: 'EWN', name: 'Johannesburg (EWN)', lat: -26.2041, lon: 28.0473, success: true },
      { id: 'News24', name: 'Cape Town (News24)', lat: -33.9249, lon: 18.4241, success: true },
      { id: 'BBC', name: 'London (BBC News)', lat: 51.5074, lon: -0.1278, success: true }
    ]

    this.init()
  }

  init() {
    this.scene = new THREE.Scene()
    this.scene.background = null

    this.camera = new THREE.PerspectiveCamera(42, this.width / this.height, 0.1, 1000)
    this.camera.position.set(0, 3, 6.8) 

    this.renderer = new THREE.WebGLRenderer({ canvas: this.canvas, antialias: true, alpha: true })
    this.renderer.setSize(this.width, this.height)
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

    this.controls = new OrbitControls(this.camera, this.renderer.domElement)
    this.controls.enableDamping = true
    this.controls.dampingFactor = 0.05
    this.controls.autoRotate = true
    this.controls.autoRotateSpeed = 1.2 

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4)
    this.scene.add(ambientLight)

    const cyanLight = new THREE.DirectionalLight(0x00f0ff, 2.0)
    cyanLight.position.set(5, 4, 5)
    this.scene.add(cyanLight)

    this.globeRadius = 2.4
    this.mainGlobeGroup = new THREE.Group()
    this.scene.add(this.mainGlobeGroup)

    this.buildGlobeGeometry()

    // Scraped Radar Shockwave Burst
    const burstGeo = new THREE.SphereGeometry(this.globeRadius + 0.05, 32, 32)
    this.burstMat = new THREE.MeshBasicMaterial({
      color: 0x00f0ff,
      wireframe: true,
      transparent: true,
      opacity: 0.0
    })
    this.burstMesh = new THREE.Mesh(burstGeo, this.burstMat)
    this.scene.add(this.burstMesh)
    this.burstScale = 1.0
    this.isBurstActive = false

    this.nodeGroup = new THREE.Group()
    this.mainGlobeGroup.add(this.nodeGroup)
    this.buildTargetNodes()

    this.animate()
  }
  buildGlobeGeometry() {
    const particleCount = 2500
    this.particleGeometry = new THREE.BufferGeometry()
    
    this.positions = new Float32Array(particleCount * 3)
    this.originalPositions = new Float32Array(particleCount * 3)
    this.randomDirections = new Float32Array(particleCount * 3)
    this.particleSpeeds = new Float32Array(particleCount)

    for (let i = 0; i < particleCount; i++) {
      const u = Math.random()
      const v = Math.random()
      const theta = u * 2.0 * Math.PI
      const phi = Math.acos(2.0 * v - 1.0)

      const x = this.globeRadius * Math.sin(phi) * Math.cos(theta)
      const y = this.globeRadius * Math.sin(phi) * Math.sin(theta)
      const z = this.globeRadius * Math.cos(phi)

      const i3 = i * 3
      this.positions[i3] = x
      this.positions[i3 + 1] = y
      this.positions[i3 + 2] = z

      this.originalPositions[i3] = x
      this.originalPositions[i3 + 1] = y
      this.originalPositions[i3 + 2] = z

      // FIXED MATH HERE: Explicitly using index strings to avoid canvas compilation drops
      const driftVec = new THREE.Vector3(x, y, z).normalize()
      this.randomDirections[i3] = driftVec.x + (Math.random() - 0.5) * 0.5
      this.randomDirections[i3 + 1] = driftVec.y + (Math.random() - 0.5) * 0.5
      this.randomDirections[i3 + 2] = driftVec.z + (Math.random() - 0.5) * 0.5

      this.particleSpeeds[i] = 1.0 + Math.random() * 2.5
    }

    this.particleGeometry.setAttribute('position', new THREE.BufferAttribute(this.positions, 3))

    const particleMat = new THREE.PointsMaterial({
      color: 0x00f0ff,
      size: 0.04,
      transparent: true,
      opacity: 0.65,
      blending: THREE.AdditiveBlending
    })

    this.particleSystem = new THREE.Points(this.particleGeometry, particleMat)
    this.mainGlobeGroup.add(this.particleSystem)
  }

  calcPosFromLatLon(lat, lon) {
    const phi = (90 - lat) * (Math.PI / 180)
    const theta = (lon + 180) * (Math.PI / 180)
    return new THREE.Vector3(
      -(this.globeRadius * Math.sin(phi) * Math.sin(theta)),
      this.globeRadius * Math.cos(phi),
      this.globeRadius * Math.sin(phi) * Math.cos(theta)
    )
  }

  buildTargetNodes() {
    this.nodeMeshes.forEach(n => this.nodeGroup.remove(n.group))
    this.nodeMeshes = []

    this.targetNodesData.forEach((node) => {
      const coords = this.calcPosFromLatLon(node.lat, node.lon)
      const targetGroup = new THREE.Group()
      targetGroup.position.copy(coords)
      targetGroup.lookAt(new THREE.Vector3(0, 0, 0))
      targetGroup.rotateX(Math.PI / 2)

      const accentColor = node.success ? 0x00ffaa : 0xff2a6d

      const pinGeo = new THREE.CylinderGeometry(0.05, 0.01, 0.25, 12)
      pinGeo.translate(0, 0.125, 0)
      const pinMat = new THREE.MeshBasicMaterial({ color: accentColor })
      const pinMesh = new THREE.Mesh(pinGeo, pinMat)
      targetGroup.add(pinMesh)

      const ringGeo = new THREE.RingGeometry(0.06, 0.18, 24)
      const ringMat = new THREE.MeshBasicMaterial({
        color: accentColor,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.8
      })
      const ringMesh = new THREE.Mesh(ringGeo, ringMat)
      targetGroup.add(ringMesh)

      this.nodeGroup.add(targetGroup)

      this.nodeMeshes.push({
        id: node.id,
        group: targetGroup,
        ringMesh,
        pinMesh,
        pulseSpeed: node.success ? 4.0 : 8.5,
        baseScale: node.success ? 1.0 : 1.4
      })
    })
  }
  triggerExplosion() {
    if (this.globeState !== 'NORMAL') return
    this.globeState = 'EXPLODED'
    this.stateTimer = 0
    this.controls.autoRotateSpeed = 22.0
  }

  triggerFractureCracking() {
    if (this.globeState !== 'NORMAL') return
    this.globeState = 'CRACKED'
    this.stateTimer = 0
    this.controls.autoRotateSpeed = -15.0
  }

  triggerExtractionState(isLoading) {
    if (this.globeState !== 'NORMAL') return
    if (isLoading) {
      this.controls.autoRotateSpeed = 8.0 
      this.isBurstActive = true
      this.burstScale = 1.0
      if (this.burstMat) this.burstMat.opacity = 0.5
    } else {
      this.controls.autoRotateSpeed = 1.2 
    }
  }

  updateFromData(sourceStatuses) {
    this.targetNodesData.forEach(node => {
      if (sourceStatuses[node.id] !== undefined) {
        node.success = sourceStatuses[node.id]
      }
    })
    this.buildTargetNodes()
  }

  resize(width, height) {
    this.camera.aspect = width / height
    this.camera.updateProjectionMatrix()
    this.renderer.setSize(width, height)
  }

  animate() {
    this.animationFrameId = requestAnimationFrame(() => this.animate())
    const elapsedTime = this.clock.getElapsedTime()
    this.stateTimer += 0.016

    const posAttr = this.particleGeometry.attributes.position

    if (this.globeState === 'EXPLODED') {
      for (let i = 0; i < posAttr.count; i++) {
        const i3 = i * 3
        const speed = this.particleSpeeds[i]
        
        if (this.stateTimer < 0.8) {
          const shift = this.stateTimer * speed * 3.0
          posAttr.array[i3] = this.originalPositions[i3] + this.randomDirections[i3] * shift
          posAttr.array[i3 + 1] = this.originalPositions[i3 + 1] + this.randomDirections[i3 + 1] * shift
          posAttr.array[i3 + 2] = this.originalPositions[i3 + 2] + this.randomDirections[i3 + 2] * shift
        } else {
          const t = (this.stateTimer - 0.8) * 1.2
          posAttr.array[i3] = THREE.MathUtils.lerp(posAttr.array[i3], this.originalPositions[i3], t)
          posAttr.array[i3 + 1] = THREE.MathUtils.lerp(posAttr.array[i3 + 1], this.originalPositions[i3 + 1], t)
          posAttr.array[i3 + 2] = THREE.MathUtils.lerp(posAttr.array[i3 + 2], this.originalPositions[i3 + 2], t)
        }
      }
      posAttr.needsUpdate = true
      this.nodeGroup.scale.setScalar(Math.max(0.001, 1 - this.stateTimer * 1.2))

      if (this.stateTimer >= 2.0) {
        this.globeState = 'NORMAL'
        this.controls.autoRotateSpeed = 1.2
        this.nodeGroup.scale.setScalar(1)
      }

    } else if (this.globeState === 'CRACKED') {
      for (let i = 0; i < posAttr.count; i++) {
        const i3 = i * 3
        const speed = this.particleSpeeds[i]
        
        if (this.stateTimer < 1.4) {
          posAttr.array[i3] += this.randomDirections[i3] * 0.04 * speed
          posAttr.array[i3 + 1] += this.randomDirections[i3 + 1] * 0.04 * speed
          posAttr.array[i3 + 2] += this.randomDirections[i3 + 2] * 0.04 * speed
        } else {
          const t = (this.stateTimer - 1.4) * 1.1
          posAttr.array[i3] = THREE.MathUtils.lerp(posAttr.array[i3], this.originalPositions[i3], t)
          posAttr.array[i3 + 1] = THREE.MathUtils.lerp(posAttr.array[i3 + 1], this.originalPositions[i3 + 1], t)
          posAttr.array[i3 + 2] = THREE.MathUtils.lerp(posAttr.array[i3 + 2], this.originalPositions[i3 + 2], t)
        }
      }
      posAttr.needsUpdate = true

      if (this.stateTimer >= 2.6) {
        this.globeState = 'NORMAL'
        this.controls.autoRotateSpeed = 1.2
      }
    } else {
      this.mainGlobeGroup.rotation.y = elapsedTime * 0.04
      
      for (let i = 0; i < posAttr.count; i++) {
        const i3 = i * 3
        posAttr.array[i3] = this.originalPositions[i3]
        posAttr.array[i3 + 1] = this.originalPositions[i3 + 1]
        posAttr.array[i3 + 2] = this.originalPositions[i3 + 2]
      }
      posAttr.needsUpdate = true
    }

    if (this.isBurstActive && this.burstMesh) {
      this.burstScale += 0.04
      this.burstMesh.scale.set(this.burstScale, this.burstScale, this.burstScale)
      this.burstMat.opacity -= 0.012
      
      if (this.burstMat.opacity <= 0) {
        this.isBurstActive = false
        this.burstScale = 1.0
      }
    }

    this.nodeMeshes.forEach((node) => {
      const scaleValue = node.baseScale * (1 + Math.sin(elapsedTime * node.pulseSpeed) * 0.35)
      node.ringMesh.scale.set(scaleValue, scaleValue, 1)
      node.ringMesh.material.opacity = Math.max(0, 0.8 - (scaleValue - 1) * 0.9)
    })

    this.controls.update()
    this.renderer.render(this.scene, this.camera)
  }

  destroy() {
    cancelAnimationFrame(this.animationFrameId)
    this.controls.dispose()
    this.renderer.dispose()
    this.scene.traverse((obj) => {
      if (!obj.isMesh && !obj.isPoints) return
      obj.geometry.dispose()
      if (Array.isArray(obj.material)) obj.material.forEach(m => m.dispose())
      else obj.material.dispose()
    })
  }
}
