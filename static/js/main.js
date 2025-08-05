// Main JavaScript for 16型花名册

// Global variables
let currentUser = null;
let authToken = localStorage.getItem('authToken');

// API base URL
const API_BASE_URL = window.location.origin;

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500 text-white' :
        type === 'error' ? 'bg-red-500 text-white' :
        'bg-blue-500 text-white'
    }`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function setLoading(loading = true) {
    const loadingElements = document.querySelectorAll('.loading');
    loadingElements.forEach(el => {
        el.style.display = loading ? 'block' : 'none';
    });
}

// Authentication functions
function showLoginModal() {
    const modal = document.getElementById('loginModal');
    modal.classList.remove('hidden');
    modal.classList.add('modal-enter');
}

function hideLoginModal() {
    const modal = document.getElementById('loginModal');
    modal.classList.add('hidden');
    modal.classList.remove('modal-enter');
}

function showSignupModal() {
    const modal = document.getElementById('signupModal');
    modal.classList.remove('hidden');
    modal.classList.add('modal-enter');
}

function hideSignupModal() {
    const modal = document.getElementById('signupModal');
    modal.classList.add('hidden');
    modal.classList.remove('modal-enter');
}

async function login(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            authToken = data.access_token;
            localStorage.setItem('authToken', authToken);
            currentUser = data.user;
            hideLoginModal();
            showNotification('登录成功！', 'success');
            updateAuthUI();
        } else {
            showNotification(data.detail || '登录失败', 'error');
        }
    } catch (error) {
        showNotification('网络错误，请重试', 'error');
    }
}

async function signup(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            hideSignupModal();
            showNotification('注册成功！请登录', 'success');
            showLoginModal();
        } else {
            showNotification(data.detail || '注册失败', 'error');
        }
    } catch (error) {
        showNotification('网络错误，请重试', 'error');
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    updateAuthUI();
    showNotification('已退出登录', 'info');
}

function updateAuthUI() {
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    
    if (currentUser) {
        loginBtn.textContent = currentUser.email;
        loginBtn.onclick = logout;
        signupBtn.textContent = '退出';
        signupBtn.onclick = logout;
    } else {
        loginBtn.textContent = '登录';
        loginBtn.onclick = showLoginModal;
        signupBtn.textContent = '注册';
        signupBtn.onclick = showSignupModal;
    }
}

// API helper functions
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
        ...options,
    };

    if (authToken) {
        config.headers.Authorization = `Bearer ${authToken}`;
    }

    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || '请求失败');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Test functionality
let currentQuestionIndex = 0;
let answers = {};

function initTest() {
    if (typeof mbtiQuestions === 'undefined') return;
    
    showQuestion(currentQuestionIndex);
    updateProgress();
}

function showQuestion(index) {
    if (index < 0 || index >= mbtiQuestions.length) return;
    
    const question = mbtiQuestions[index];
    const container = document.getElementById('questionContainer');
    
    container.innerHTML = `
        <div class="mb-6">
            <h3 class="text-xl font-semibold text-gray-900 mb-4">问题 ${index + 1} / ${mbtiQuestions.length}</h3>
            <p class="text-lg text-gray-700 mb-6">${question.question}</p>
            
            <div class="space-y-4">
                ${question.options.map((option, optionIndex) => `
                    <label class="question-option block p-4 border-2 border-gray-200 rounded-lg cursor-pointer transition-all ${
                        answers[question.id] === option.value ? 'selected' : ''
                    }">
                        <input type="radio" name="question_${question.id}" value="${option.value}" 
                               class="sr-only" ${answers[question.id] === option.value ? 'checked' : ''}>
                        <div class="flex items-center">
                            <div class="w-4 h-4 border-2 border-gray-300 rounded-full mr-3 flex items-center justify-center">
                                <div class="w-2 h-2 bg-primary-600 rounded-full ${answers[question.id] === option.value ? '' : 'hidden'}"></div>
                            </div>
                            <span class="text-gray-700">${option.text}</span>
                        </div>
                    </label>
                `).join('')}
            </div>
        </div>
    `;
    
    // Add event listeners
    const options = container.querySelectorAll('input[type="radio"]');
    options.forEach(option => {
        option.addEventListener('change', (e) => {
            answers[question.id] = e.target.value;
            updateProgress();
        });
    });
}

function updateProgress() {
    const answeredCount = Object.keys(answers).length;
    const totalQuestions = mbtiQuestions.length;
    const progressPercentage = (answeredCount / totalQuestions) * 100;
    
    document.getElementById('progressText').textContent = `${answeredCount} / ${totalQuestions}`;
    document.getElementById('progressBar').style.width = `${progressPercentage}%`;
    
    // Update navigation buttons
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    prevBtn.disabled = currentQuestionIndex === 0;
    nextBtn.style.display = currentQuestionIndex === totalQuestions - 1 ? 'none' : 'block';
    submitBtn.style.display = currentQuestionIndex === totalQuestions - 1 ? 'block' : 'none';
}

function nextQuestion() {
    if (currentQuestionIndex < mbtiQuestions.length - 1) {
        currentQuestionIndex++;
        showQuestion(currentQuestionIndex);
        updateProgress();
    }
}

function prevQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        showQuestion(currentQuestionIndex);
        updateProgress();
    }
}

function calculateMBTI() {
    const scores = { E: 0, I: 0, S: 0, N: 0, T: 0, F: 0, J: 0, P: 0 };
    
    Object.values(answers).forEach(answer => {
        if (scores.hasOwnProperty(answer)) {
            scores[answer]++;
        }
    });
    
    const mbtiType = [
        scores.E > scores.I ? 'E' : 'I',
        scores.S > scores.N ? 'S' : 'N',
        scores.T > scores.F ? 'T' : 'F',
        scores.J > scores.P ? 'J' : 'P'
    ].join('');
    
    return {
        type: mbtiType,
        scores: scores,
        percentages: {
            E: (scores.E / (scores.E + scores.I)) * 100,
            I: (scores.I / (scores.E + scores.I)) * 100,
            S: (scores.S / (scores.S + scores.N)) * 100,
            N: (scores.N / (scores.S + scores.N)) * 100,
            T: (scores.T / (scores.T + scores.F)) * 100,
            F: (scores.F / (scores.T + scores.F)) * 100,
            J: (scores.J / (scores.J + scores.P)) * 100,
            P: (scores.P / (scores.J + scores.P)) * 100
        }
    };
}

// Celebrities functionality
async function loadCelebrities(page = 1, filters = {}) {
    try {
        const params = new URLSearchParams({
            skip: (page - 1) * 12,
            limit: 12,
            ...filters
        });
        
        const data = await apiCall(`/celebrities?${params}`);
        return data;
    } catch (error) {
        showNotification('加载名人数据失败', 'error');
        return { items: [], total: 0 };
    }
}

function renderCelebrityCard(celebrity) {
    return `
        <div class="celebrity-card bg-white rounded-lg shadow-lg p-6" data-id="${celebrity.id}">
            <div class="text-center mb-4">
                <div class="w-24 h-24 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center mx-auto mb-3">
                    <span class="text-white text-xl font-bold">${celebrity.name.charAt(0)}</span>
                </div>
                <h3 class="text-lg font-semibold text-gray-900">${celebrity.name}</h3>
                <span class="mbti-badge ${celebrity.mbti_type.toLowerCase()}">${celebrity.mbti_type}</span>
            </div>
            
            <p class="text-gray-600 text-sm mb-4 line-clamp-3">${celebrity.description}</p>
            
            <div class="flex flex-wrap gap-2 mb-4">
                ${celebrity.tags.map(tag => `
                    <span class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full">${tag.name}</span>
                `).join('')}
            </div>
            
            <div class="flex justify-between items-center text-sm text-gray-500">
                <span>${celebrity.vote_count || 0} 票</span>
                <span>${celebrity.comment_count || 0} 评论</span>
            </div>
        </div>
    `;
}

// Homepage functionality
async function loadHomepageData() {
    try {
        // Load recent celebrities
        const celebritiesData = await apiCall('/celebrities?limit=6');
        const container = document.getElementById('celebritiesPreview');
        
        if (celebritiesData.items && celebritiesData.items.length > 0) {
            container.innerHTML = celebritiesData.items.map(celebrity => `
                <div class="text-center">
                    <div class="w-32 h-32 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center mx-auto mb-4">
                        <span class="text-white text-2xl font-bold">${celebrity.name.charAt(0)}</span>
                    </div>
                    <h4 class="font-semibold text-gray-900 mb-1">${celebrity.name}</h4>
                    <span class="mbti-badge ${celebrity.mbti_type.toLowerCase()}">${celebrity.mbti_type}</span>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading homepage data:', error);
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize authentication UI
    updateAuthUI();
    
    // Modal event listeners
    document.getElementById('loginBtn')?.addEventListener('click', showLoginModal);
    document.getElementById('signupBtn')?.addEventListener('click', showSignupModal);
    
    // Close modal buttons
    document.getElementById('closeLoginModal')?.addEventListener('click', hideLoginModal);
    document.getElementById('closeSignupModal')?.addEventListener('click', hideSignupModal);
    
    // Switch between modals
    document.getElementById('switchToSignup')?.addEventListener('click', () => {
        hideLoginModal();
        showSignupModal();
    });
    
    document.getElementById('switchToLogin')?.addEventListener('click', () => {
        hideSignupModal();
        showLoginModal();
    });
    
    // Form submissions
    document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        await login(email, password);
    });
    
    document.getElementById('signupForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('signupEmail').value;
        const password = document.getElementById('signupPassword').value;
        const confirmPassword = document.getElementById('signupConfirmPassword').value;
        
        if (password !== confirmPassword) {
            showNotification('密码不匹配', 'error');
            return;
        }
        
        await signup(email, password);
    });
    
    // Test functionality
    if (window.location.pathname === '/test') {
        initTest();
        
        document.getElementById('nextBtn')?.addEventListener('click', nextQuestion);
        document.getElementById('prevBtn')?.addEventListener('click', prevQuestion);
        document.getElementById('mbtiTestForm')?.addEventListener('submit', (e) => {
            e.preventDefault();
            const result = calculateMBTI();
            window.location.href = `/result?type=${result.type}`;
        });
    }
    
    // Celebrities page functionality
    if (window.location.pathname === '/celebrities') {
        loadCelebrities().then(data => {
            const container = document.getElementById('celebritiesGrid');
            const loadingState = document.getElementById('loadingState');
            
            if (data.items && data.items.length > 0) {
                container.innerHTML = data.items.map(renderCelebrityCard).join('');
                loadingState.style.display = 'none';
            } else {
                document.getElementById('noResults').classList.remove('hidden');
                loadingState.style.display = 'none';
            }
        });
    }
    
    // Homepage functionality
    if (window.location.pathname === '/') {
        loadHomepageData();
    }
    
    // Share functionality
    document.getElementById('shareResult')?.addEventListener('click', () => {
        const modal = document.getElementById('shareModal');
        modal.classList.remove('hidden');
        document.getElementById('shareLink').value = window.location.href;
    });
    
    document.getElementById('closeShareModal')?.addEventListener('click', () => {
        document.getElementById('shareModal').classList.add('hidden');
    });
    
    document.getElementById('copyLink')?.addEventListener('click', () => {
        const linkInput = document.getElementById('shareLink');
        linkInput.select();
        document.execCommand('copy');
        showNotification('链接已复制到剪贴板', 'success');
    });
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showNotification('发生错误，请刷新页面重试', 'error');
}); 