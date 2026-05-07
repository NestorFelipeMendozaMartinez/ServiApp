<template>
  <div id="app">
    <NavBar />
    <main class="pt-navbar">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
</script>

<style>
:root {
  --primary: #FF6B35;
  --primary-dark: #e55a24;
  --secondary: #004E89;
  --accent: #1A936F;
  --bg: #F8F9FA;
  --text: #2D3436;
  --muted: #636e72;
  --card-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

* { box-sizing: border-box; }

body {
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  margin: 0;
}

.pt-navbar { padding-top: 70px; }

.btn-primary {
  background-color: var(--primary) !important;
  border-color: var(--primary) !important;
}
.btn-primary:hover, .btn-primary:focus {
  background-color: var(--primary-dark) !important;
  border-color: var(--primary-dark) !important;
}
.btn-outline-primary {
  color: var(--primary) !important;
  border-color: var(--primary) !important;
}
.btn-outline-primary:hover {
  background-color: var(--primary) !important;
  color: #fff !important;
}
.text-primary { color: var(--primary) !important; }
.bg-primary { background-color: var(--primary) !important; }
.border-primary { border-color: var(--primary) !important; }
.badge-primary { background-color: var(--primary) !important; }

.card {
  border: none;
  box-shadow: var(--card-shadow);
  border-radius: 12px;
}
.badge-cat {
  background-color: rgba(255,107,53,0.12);
  color: var(--primary);
  font-size: 0.75rem;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 600;
  display: inline-block;
}
.stars { color: #ffc107; font-size: 0.9rem; }

.page-header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: #fff;
  padding: 2.5rem 0 2rem;
  margin-bottom: 2rem;
}
.page-header h1 { font-weight: 700; margin: 0; }
.page-header p { opacity: 0.9; margin: 0.4rem 0 0; }

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--muted);
}
.empty-state .icon { font-size: 4rem; margin-bottom: 1rem; }

.status-badge {
  font-size: 0.78rem;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
  display: inline-block;
}
.status-open { background: #d4edda; color: #155724; }
.status-in_progress { background: #fff3cd; color: #856404; }
.status-completed { background: #cce5ff; color: #004085; }
.status-cancelled { background: #f8d7da; color: #721c24; }
</style>
