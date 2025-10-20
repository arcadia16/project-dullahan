<template>
  <div id="app">
    <Toast />
    <nav class="navbar">
      <div class="nav-container">
        <h1>🔒 Project Dullahan - NTLM Security Audit Tool</h1>
        <p>Domain Password Security Assessment</p>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>
    
    <!-- <footer class="footer">
      <p>⚠️ Use only on authorized domains. Handle credentials securely.</p>
    </footer> -->
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f7fa;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background: black;
  color: white;
  padding: 1.5rem 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.navbar h1 {
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.navbar p {
  opacity: 0.9;
}

.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
}

.footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}

/* Custom styles for PrimeVue components */
.p-card {
  margin-bottom: 1.5rem;
}

.p-progress-spinner {
  margin: 1rem auto;
}
</style>