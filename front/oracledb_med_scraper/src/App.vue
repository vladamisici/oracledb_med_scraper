<script setup>
import { ref } from 'vue'
import axios from 'axios'

// State variables
const keywords = ref('')
const rows = ref(10)
const papers = ref([])
const activePage = ref('home')
const showSidebar = ref(false)
const loading = ref(false)

function setActivePage(page) {
  activePage.value = page
}

function toggleSidebar() {
  showSidebar.value = !showSidebar.value
}

async function searchArticles() {
  loading.value = true
  try {
    const resp = await axios.post('http://localhost:5000/api/search', {
      keywords: keywords.value,
      rows: parseInt(rows.value, 10)
    })
    alert(resp.data.message || 'Search completed successfully!')
  } catch (error) {
    console.error(error)
    alert('Error during search!')
  } finally {
    loading.value = false
  }
}

async function getPapers() {
  loading.value = true
  try {
    const resp = await axios.get('http://localhost:5000/api/papers')
    papers.value = resp.data
  } catch (error) {
    console.error(error)
    alert('Error fetching data from DB!')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div id="app">
    <!-- Navigation Bar -->
    <header class="navbar">
      <div class="navbar-left">
        <div class="logo">
          <img src="https://i.postimg.cc/Kz5ZyFSN/medsearchdb.png" alt="Site Logo" />
          <span class="site-title">medsearch.db</span>
        </div>
      </div>
      <nav class="navbar-right">
        <ul class="nav-links">
          <li><a href="#" @click.prevent="setActivePage('home')" :class="{active: activePage==='home'}">Home</a></li>
          <li><a href="#" @click.prevent="setActivePage('search')" :class="{active: activePage==='search'}">Search</a></li>
          <li><a href="#" @click.prevent="setActivePage('database')" :class="{active: activePage==='database'}">Database</a></li>
          <li><a href="#" @click.prevent="setActivePage('about')" :class="{active: activePage==='about'}">About</a></li>
          <li><a href="#" @click.prevent="setActivePage('help')" :class="{active: activePage==='help'}">Help</a></li>
        </ul>
      </nav>
      <div class="mobile-menu" @click="toggleSidebar">
        <ion-icon name="menu-outline"></ion-icon>
      </div>
    </header>

    <!-- Sidebar for mobile -->
    <transition name="slide-fade">
      <aside class="sidebar" v-if="showSidebar">
        <ul class="sidebar-links">
          <li><a href="#" @click.prevent="setActivePage('home'); toggleSidebar()" :class="{active: activePage==='home'}">Home</a></li>
          <li><a href="#" @click.prevent="setActivePage('search'); toggleSidebar()" :class="{active: activePage==='search'}">Search</a></li>
          <li><a href="#" @click.prevent="setActivePage('database'); toggleSidebar()" :class="{active: activePage==='database'}">Database</a></li>
          <li><a href="#" @click.prevent="setActivePage('about'); toggleSidebar()" :class="{active: activePage==='about'}">About</a></li>
          <li><a href="#" @click.prevent="setActivePage('help'); toggleSidebar()" :class="{active: activePage==='help'}">Help</a></li>
        </ul>
      </aside>
    </transition>

    <!-- Main Content Area -->
    <main class="main-content">
      <!-- HOME PAGE -->
      <section v-if="activePage==='home'" class="home-section">
        <div class="hero">
          <h1>Welcome to the Scientific Papers Management System</h1>
          <p>Discover, search, and manage a vast collection of scientific articles. Easily query the database, add new papers from external sources, and explore the world of research.</p>
          <button class="btn-cta" @click="setActivePage('search')">Get Started</button>
        </div>
        <div class="features-grid">
          <div class="feature-item">
            <ion-icon name="search-outline"></ion-icon>
            <h3>Search</h3>
            <p>Find articles by keywords, and retrieve results from external sources to enrich your database.</p>
          </div>
          <div class="feature-item">
            <ion-icon name="server-outline"></ion-icon>
            <h3>Database</h3>
            <p>View and manage articles stored in your local Oracle database. Examine metadata, venues, and DOIs.</p>
          </div>
          <div class="feature-item">
            <ion-icon name="sparkles-outline"></ion-icon>
            <h3>Modern UI</h3>
            <p>Experience a sleek, modern, and highly-detailed interface designed to delight and impress.</p>
          </div>
        </div>
      </section>

      <!-- SEARCH PAGE -->
      <section v-if="activePage==='search'" class="search-section">
        <h2>Search Articles</h2>
        <form @submit.prevent="searchArticles" class="search-form">
          <div class="form-row">
            <label>Keywords</label>
            <input v-model="keywords" type="text" placeholder="e.g. machine learning, quantum computing" />
          </div>
          <div class="form-row">
            <label>Number of Results</label>
            <input v-model="rows" type="number" min="1" value="10" />
          </div>
          <button type="submit" class="btn-search">Search</button>
        </form>
        <transition name="fade">
          <div v-if="loading" class="loading-overlay">
            <div class="spinner"></div>
            <p>Searching articles, please wait...</p>
          </div>
        </transition>
      </section>

      <!-- DATABASE PAGE -->
      <section v-if="activePage==='database'" class="database-section">
        <div class="db-header">
          <h2>Articles in Database</h2>
          <button class="btn-show" @click="getPapers">Show Articles</button>
        </div>
        <transition name="fade">
          <ul v-if="papers.length > 0" class="papers-list">
            <li v-for="paper in papers" :key="paper.Paper_ID" class="paper-card">
              <div class="paper-info">
                <h3 class="paper-title">{{paper.Title}}</h3>
                <div class="paper-meta">
                  <span class="paper-year">Year: {{paper.Year}}</span>
                  <span class="paper-venue">{{paper.Venue_Name}}</span>
                  <span class="paper-doi">DOI: {{paper.DOI}}</span>
                </div>
              </div>
            </li>
          </ul>
          <div v-else class="no-results">
            <p>No articles to display. Try searching or adding new articles.</p>
          </div>
        </transition>
        <transition name="fade">
          <div v-if="loading" class="loading-overlay">
            <div class="spinner"></div>
            <p>Loading articles from DB...</p>
          </div>
        </transition>
      </section>

      <!-- ABOUT PAGE -->
      <section v-if="activePage==='about'" class="about-section">
        <h2>About This Project</h2>
        <p>This platform provides a convenient way to integrate scientific articles from external sources (like CrossRef) into an Oracle database, and to manage and explore these records.</p>
        <p>Features:</p>
        <ul class="about-list">
          <li>Modern UI with responsive design</li>
          <li>Integration with external APIs</li>
          <li>Local Oracle database management</li>
          <li>Scalable architecture</li>
        </ul>
        <p>Team & Credits:</p>
        <ul class="about-list">
          <li>Designers: Inspired by Apple's clean aesthetics</li>
          <li>Developers: Frontend (Vue.js), Backend (Python, Flask), DB (Oracle)</li>
        </ul>
      </section>

      <!-- HELP PAGE -->
      <section v-if="activePage==='help'" class="help-section">
        <h2>Help & Documentation</h2>
        <div class="help-content">
          <h3>How to Search for Articles</h3>
          <p>Navigate to the 'Search' page, enter your desired keywords and the number of results, then click 'Search'. The system will query external APIs and attempt to insert new articles into the database if they do not exist.</p>
          <h3>How to View Articles in the Database</h3>
          <p>Go to the 'Database' page and click 'Show Articles' to retrieve the first 50 entries. If no data appears, try searching for articles first.</p>
          <h3>Troubleshooting</h3>
          <p>If you encounter errors, check the console for messages or contact the support team.</p>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-left">
        <p>&copy; 2024 Scientific Papers Management - Misici Vlada</p>
      </div>
      <div class="footer-right">
        <p> Vue.js, Flask & Oracle DB</p>
      </div>
    </footer>
  </div>
</template>

<style>
/* Reset & Global Styles */
* {
  margin: 0; padding: 0; box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  background: linear-gradient(to bottom right, #f5f5f7, #e9e9ec);
  color: #333;
  overflow-x: hidden;
}

/* Icons (Ionicons) */
@import url("https://unpkg.com/ionicons@5.5.2/dist/css/ionicons.min.css");

/* Layout */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Navbar */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffffcc;
  backdrop-filter: blur(15px);
  padding: 10px 20px;
  box-shadow: 0 2px 15px rgba(0,0,0,0.05);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-left .logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo img {
  border-radius: 50%;
}

.site-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #111;
}

.navbar-right .nav-links {
  list-style: none;
  display: flex;
  gap: 20px;
}

.nav-links li a {
  text-decoration: none;
  font-weight: 500;
  color: #333;
  position: relative;
  padding: 5px;
}

.nav-links li a:hover {
  color: #007aff;
}

.nav-links li a.active::after {
  content: "";
  display: block;
  height: 2px;
  background: #007aff;
  width: 100%;
  position: absolute;
  bottom: -5px;
  left: 0;
}

/* Mobile menu icon */
.mobile-menu {
  display: none;
  font-size: 1.5rem;
  cursor: pointer;
}

/* Sidebar */
.sidebar {
  position: fixed;
  top: 0; left: 0; bottom: 0;
  width: 200px;
  background: #fff;
  box-shadow: 2px 0 15px rgba(0,0,0,0.05);
  z-index: 2000;
  padding: 20px;
}

.sidebar-links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.sidebar-links li a {
  text-decoration: none;
  font-weight: 500;
  color: #333;
  padding: 5px 0;
}

.sidebar-links li a.active {
  color: #007aff;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 40px;
}

/* Home Section */
.home-section .hero {
  text-align: center;
  margin-bottom: 50px;
}

.home-section .hero h1 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #111;
}

.home-section .hero p {
  font-size: 1rem;
  color: #444;
  max-width: 600px;
  margin: 0 auto 30px auto;
}

.btn-cta {
  padding: 12px 20px;
  background: #007aff;
  color: #fff;
  border-radius: 10px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-cta:hover {
  background: #005ecb;
}

.features-grid {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 50px;
}

.feature-item {
  background: #fff;
  border-radius: 15px;
  padding: 30px;
  width: 250px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  transition: box-shadow 0.3s;
}

.feature-item:hover {
  box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}

.feature-item ion-icon {
  font-size: 2rem;
  color: #007aff;
  margin-bottom: 15px;
}

.feature-item h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 10px;
  color: #111;
}

.feature-item p {
  font-size: 0.95rem;
  color: #555;
}

/* Search Section */
.search-section h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #222;
}

.search-form {
  background: #fafafa;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 500px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: flex;
  flex-direction: column;
}

.form-row label {
  font-weight: 500;
  margin-bottom: 8px;
  color: #444;
}

.form-row input {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  font-size: 1rem;
  outline: none;
  background: #fff;
  transition: border-color 0.3s;
}

.form-row input:focus {
  border-color: #007aff;
}

.btn-search {
  padding: 12px 20px;
  background: #007aff;
  color: #fff;
  border-radius: 10px;
  font-weight: 500;
  border: none;
  cursor: pointer;
}

.btn-search:hover {
  background: #005ecb;
}

/* Database Section */
.database-section .db-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.db-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #222;
}

.btn-show {
  padding: 10px 16px;
  background: #007aff;
  color: #fff;
  border-radius: 8px;
  font-weight: 500;
  border: none;
  cursor: pointer;
}

.btn-show:hover {
  background: #005ecb;
}

.papers-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.paper-card {
  background: #fff;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  transition: box-shadow 0.3s;
}

.paper-card:hover {
  box-shadow: 0 8px 25px rgba(0,0,0,0.08);
}

.paper-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.paper-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #111;
}

.paper-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 0.95rem;
  color: #555;
}

.paper-year, .paper-venue, .paper-doi {
  background: #edf0f4;
  border-radius: 8px;
  padding: 5px 10px;
}

.no-results {
  text-align: center;
  font-size: 1rem;
  color: #555;
}

/* About Section */
.about-section {
  max-width: 600px;
  margin: 0 auto;
  text-align: left;
}

.about-section h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #222;
}

.about-section p {
  margin-bottom: 15px;
  color: #444;
}

.about-list {
  list-style: disc;
  margin-left: 20px;
  margin-bottom: 20px;
}

.about-list li {
  margin-bottom: 10px;
  color: #444;
}

/* Help Section */
.help-section {
  max-width: 600px;
  margin: 0 auto;
}

.help-section h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #222;
}

.help-content h3 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-top: 20px;
  margin-bottom: 10px;
  color: #111;
}

.help-content p {
  margin-bottom: 10px;
  color: #444;
}

/* Loading Overlay */
.loading-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(255,255,255,0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 3000;
}

.spinner {
  width: 40px; height: 40px;
  border: 4px solid #ccc;
  border-top: 4px solid #007aff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

/* Footer */
.footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffffcc;
  backdrop-filter: blur(10px);
  padding: 20px;
  box-shadow: 0 -2px 15px rgba(0,0,0,0.05);
  font-size: 0.9rem;
  color: #555;
}

.footer-left, .footer-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
  .nav-links {
    display: none;
  }

  .mobile-menu {
    display: block;
    color: #333;
  }

  .features-grid {
    flex-direction: column;
    align-items: center;
  }

  .search-form, .about-section, .help-section {
    width: 100%;
    max-width: 100%;
  }
}

/* Transitions */
.slide-fade-enter-active, .slide-fade-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.slide-fade-enter-from, .slide-fade-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
