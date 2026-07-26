<script setup>
// No local activeNav needed anymore — router-link-active handles it automatically
</script>

<template>
  <header class="top-nav">
    <div class="brand-group">
      <h1>SCRAPING ANALYTICS<br />PLATFORM</h1>
    </div>

    <nav class="nav-links">
      <router-link to="/" exact-active-class="nav-active">Dashboard</router-link>
      <router-link to="/websites" exact-active-class="nav-active">Websites</router-link>
    </nav>
  </header>
</template>

<style scoped>
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 20px 0 16px 0;
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 24px;
}

.brand-group h1 {
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 0.3px;
  color: #1a1a1a;
  line-height: 1.3;
  margin: 0;
  text-transform: uppercase;
}

.nav-links {
  display: flex;
  gap: 28px;
  align-items: center;
  padding-top: 6px;
}

.nav-links a {
  position: relative;
  font-size: 16px;
  font-weight: 500;
  color: #9aa0a6;
  text-decoration: none;
  cursor: pointer;
  padding-bottom: 6px;
  transition: color 0.2s ease;
}

.nav-links a::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 100%;
  height: 2px;
  background-color: #362f78;
  border-radius: 2px;
  transform: translateX(-50%) scaleX(0);
  transform-origin: center;
  transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-links a:hover,
.top-nav .nav-links a:hover {
  color: #362f78 !important;
}

.nav-links a:hover::after {
  transform: translateX(-50%) scaleX(1);
}

.nav-links a.nav-active {
  color: #362f78;
  font-weight: 700;
}

.nav-links a.nav-active::after {
  transform: translateX(-50%) scaleX(1);
  height: 2.5px;
}
</style>