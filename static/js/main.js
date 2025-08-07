// Main JavaScript for MBTI Roster
console.log('JavaScript file loaded!');

// Toast notification system
let toastContainer = null;

function createToastContainer() {
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    return toastContainer;
}

function showToast(message, type = 'info', duration = 5000) {
    const container = createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const title = type.charAt(0).toUpperCase() + type.slice(1);
    
    toast.innerHTML = `
        <div class="toast-header">
            <span class="toast-title">${title}</span>
            <button class="toast-close" onclick="this.parentElement.parentElement.remove()">&times;</button>
        </div>
        <div class="toast-message">${message}</div>
    `;
    
    container.appendChild(toast);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (toast.parentElement) {
            toast.classList.add('hiding');
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.remove();
                }
            }, 300);
        }
    }, duration);
    
    return toast;
}

// Global utility functions
function showMessage(message, type = 'info') {
    console.log(`${type.toUpperCase()}: ${message}`);
    showToast(message, type);
}

// API helper functions
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Search functionality
async function searchCelebrities(query, searchType = 'all') {
    try {
        const response = await apiCall(`/search/?q=${encodeURIComponent(query)}&search_type=${searchType}`);
        return response;
    } catch (error) {
        showMessage('Search failed: ' + error.message, 'error');
        return null;
    }
}

// Authentication helpers
function getToken() {
    return localStorage.getItem('auth_token');
}

function setToken(token) {
    localStorage.setItem('auth_token', token);
}

function removeToken() {
    localStorage.removeItem('auth_token');
}

// Modal management
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
    }
}

function switchModal(fromModalId, toModalId) {
    hideModal(fromModalId);
    showModal(toModalId);
}

// Form validation
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

function showFieldError(fieldId, message) {
    const errorElement = document.getElementById(fieldId + 'Error');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.remove('hidden');
    }
}

function hideFieldError(fieldId) {
    const errorElement = document.getElementById(fieldId + 'Error');
    if (errorElement) {
        errorElement.classList.add('hidden');
    }
}

// Authentication functions
async function loginUser(email, password) {
    try {
        console.log('Attempting to login user:', { email });
        const response = await apiCall('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        console.log('Login response:', response);
        
        if (response.access_token) {
            setToken(response.access_token);
            showMessage('登录成功！欢迎回来！', 'success');
            hideModal('loginModal');
            updateAuthUI(); // This will now show user info
            return true;
        } else {
            showMessage('登录失败：服务器响应格式错误', 'error');
            return false;
        }
    } catch (error) {
        console.error('Login error:', error);
        let errorMessage = '登录失败，请稍后重试';
        
        if (error.message.includes('401')) {
            errorMessage = '邮箱或密码错误，请检查后重试';
        } else if (error.message.includes('422')) {
            errorMessage = '请检查输入信息是否正确';
        } else if (error.message.includes('400')) {
            errorMessage = '请求参数错误，请检查输入';
        }
        
        showMessage(errorMessage, 'error');
        return false;
    }
}

async function signupUser(name, email, password) {
    try {
        console.log('Attempting to signup user:', { name, email });
        const response = await apiCall('/auth/signup', {
            method: 'POST',
            body: JSON.stringify({ name, email, password })
        });
        
        console.log('Signup response:', response);
        
        if (response.access_token) {
            setToken(response.access_token);
            showMessage('注册成功！欢迎加入16型花名册！', 'success');
            hideModal('signupModal');
            updateAuthUI(); // This will now show user info
            return true;
        } else {
            showMessage('注册失败：服务器响应格式错误', 'error');
            return false;
        }
    } catch (error) {
        console.error('Signup error:', error);
        let errorMessage = '注册失败，请稍后重试';
        
        if (error.message.includes('409')) {
            errorMessage = '该邮箱已被注册，请使用其他邮箱或直接登录';
        } else if (error.message.includes('422')) {
            errorMessage = '请检查输入信息是否正确';
        } else if (error.message.includes('400')) {
            errorMessage = '请求参数错误，请检查输入';
        }
        
        showMessage(errorMessage, 'error');
        return false;
    }
}

function logoutUser() {
    removeToken();
    removeUserInfoDisplay(); // Clean up user info display
    updateAuthUI();
    showMessage('已退出登录', 'info');
}

function updateAuthUI() {
    const token = getToken();
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    
    if (token) {
        // User is logged in
        if (loginBtn) {
            loginBtn.textContent = '退出';
            loginBtn.className = 'text-gray-700 hover:text-red-600 px-3 py-2 rounded-md text-sm font-medium transition-colors';
        }
        if (signupBtn) signupBtn.style.display = 'none';
        
        // Get and display user info
        getUserProfile();
    } else {
        // User is not logged in
        if (loginBtn) {
            loginBtn.textContent = '登录';
            loginBtn.className = 'text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors';
        }
        if (signupBtn) signupBtn.style.display = 'inline-block';
        
        // Remove user info display
        removeUserInfoDisplay();
    }
}

async function getUserProfile() {
    try {
        const token = getToken();
        if (!token) return;
        
        const response = await apiCall('/auth/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.name) {
            displayUserInfo(response.name);
        }
    } catch (error) {
        console.error('Failed to get user profile:', error);
        // If token is invalid, remove it
        if (error.message.includes('401')) {
            removeToken();
            updateAuthUI();
        }
    }
}

function displayUserInfo(userName) {
    // Remove existing user info if any
    removeUserInfoDisplay();
    
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        // Create user name display
        const userNameDisplay = document.createElement('span');
        userNameDisplay.className = 'text-sm text-gray-700 font-medium mr-3';
        userNameDisplay.textContent = `欢迎，${userName}`;
        userNameDisplay.id = 'userNameDisplay';
        
        // Insert user name before the login button
        loginBtn.parentNode.insertBefore(userNameDisplay, loginBtn);
    }
}

function removeUserInfoDisplay() {
    const userNameDisplay = document.getElementById('userNameDisplay');
    if (userNameDisplay) {
        userNameDisplay.remove();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('MBTI Roster website loaded successfully!');
    console.log('Setting up authentication buttons...');
    
    // Initialize authentication UI
    updateAuthUI();
    
    // Login button event listener
    const loginBtn = document.getElementById('loginBtn');
    console.log('Login button found:', loginBtn);
    if (loginBtn) {
        loginBtn.addEventListener('click', function(e) {
            console.log('Login button clicked!');
            e.preventDefault();
            const token = getToken();
            if (token) {
                // User is logged in, show logout
                console.log('User is logged in, logging out...');
                logoutUser();
            } else {
                // User is not logged in, show login modal
                console.log('User is not logged in, showing login modal...');
                showModal('loginModal');
            }
        });
        console.log('Login button event listener attached');
    } else {
        console.error('Login button not found!');
    }
    
    // Signup button event listener
    const signupBtn = document.getElementById('signupBtn');
    console.log('Signup button found:', signupBtn);
    if (signupBtn) {
        signupBtn.addEventListener('click', function(e) {
            console.log('Signup button clicked!');
            e.preventDefault();
            showModal('signupModal');
        });
        console.log('Signup button event listener attached');
    } else {
        console.error('Signup button not found!');
    }
    
    // Close modal buttons
    const closeLoginModal = document.getElementById('closeLoginModal');
    console.log('Close login modal button found:', closeLoginModal);
    if (closeLoginModal) {
        closeLoginModal.addEventListener('click', function() {
            console.log('Closing login modal');
            hideModal('loginModal');
        });
    }
    
    const closeSignupModal = document.getElementById('closeSignupModal');
    console.log('Close signup modal button found:', closeSignupModal);
    if (closeSignupModal) {
        closeSignupModal.addEventListener('click', function() {
            console.log('Closing signup modal');
            hideModal('signupModal');
        });
    }
    
    // Switch between modals
    const switchToSignup = document.getElementById('switchToSignup');
    console.log('Switch to signup button found:', switchToSignup);
    if (switchToSignup) {
        switchToSignup.addEventListener('click', function() {
            console.log('Switching to signup modal');
            switchModal('loginModal', 'signupModal');
        });
    }
    
    const switchToLogin = document.getElementById('switchToLogin');
    console.log('Switch to login button found:', switchToLogin);
    if (switchToLogin) {
        switchToLogin.addEventListener('click', function() {
            console.log('Switching to login modal');
            switchModal('signupModal', 'loginModal');
        });
    }
    
    // Login form submission
    const loginForm = document.getElementById('loginForm');
    console.log('Login form found:', loginForm);
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            console.log('Login form submitted');
            e.preventDefault();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            console.log('Login attempt with email:', email);
            
            // Clear previous errors
            hideFieldError('loginEmail');
            hideFieldError('loginPassword');
            
            // Validate inputs
            let hasError = false;
            
            if (!validateEmail(email)) {
                showFieldError('loginEmail', '请输入有效的邮箱地址');
                hasError = true;
            }
            
            if (!validatePassword(password)) {
                showFieldError('loginPassword', '密码至少需要6个字符');
                hasError = true;
            }
            
            if (!hasError) {
                await loginUser(email, password);
            }
        });
    }
    
    // Signup form submission
    const signupForm = document.getElementById('signupForm');
    console.log('Signup form found:', signupForm);
    if (signupForm) {
        signupForm.addEventListener('submit', async function(e) {
            console.log('Signup form submitted');
            e.preventDefault();
            
            const name = document.getElementById('signupName').value;
            const email = document.getElementById('signupEmail').value;
            const password = document.getElementById('signupPassword').value;
            const confirmPassword = document.getElementById('signupConfirmPassword').value;
            
            console.log('Signup attempt with email:', email);
            
            // Clear previous errors
            hideFieldError('signupName');
            hideFieldError('signupEmail');
            hideFieldError('signupPassword');
            hideFieldError('signupConfirmPassword');
            
            // Validate inputs
            let hasError = false;
            
            if (name.trim().length < 2) {
                showFieldError('signupName', '姓名至少需要2个字符');
                hasError = true;
            }
            
            if (!validateEmail(email)) {
                showFieldError('signupEmail', '请输入有效的邮箱地址');
                hasError = true;
            }
            
            if (!validatePassword(password)) {
                showFieldError('signupPassword', '密码至少需要6个字符');
                hasError = true;
            }
            
            if (password !== confirmPassword) {
                showFieldError('signupConfirmPassword', '两次输入的密码不一致');
                hasError = true;
            }
            
            if (!hasError) {
                await signupUser(name, email, password);
            }
        });
    }
    
    // Close modals when clicking outside
    const modals = ['loginModal', 'signupModal'];
    modals.forEach(modalId => {
        const modal = document.getElementById(modalId);
        console.log(`Modal ${modalId} found:`, modal);
        if (modal) {
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    console.log(`Closing modal ${modalId} by clicking outside`);
                    hideModal(modalId);
                }
            });
        }
    });
    
    console.log('All event listeners attached successfully!');
    showMessage('Website ready!', 'success');
    
    // Load celebrities for main page if we're on the homepage
    if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
        console.log('Loading celebrities for main page...');
        loadCelebritiesForMainPage();
    }
});

// Export functions for use in templates
window.MBTIApp = {
    showMessage,
    apiCall,
    searchCelebrities,
    getToken,
    setToken,
    removeToken,
    loginUser,
    signupUser,
    logoutUser
};

// Load celebrities for main page
async function loadCelebritiesForMainPage() {
    try {
        // Get recent celebrities (limit to 6 for display)
        const response = await apiCall('/celebrities/?limit=6');
        
        const container = document.getElementById('celebritiesPreview');
        if (!container) {
            console.log('Celebrities preview container not found');
            return;
        }
        
        if (response && response.length > 0) {
            container.innerHTML = '';
            
            response.forEach(celebrity => {
                const celebrityCard = document.createElement('div');
                celebrityCard.className = 'bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6 text-center';
                
                // Get MBTI type from votes
                let mbtiType = '未知';
                if (celebrity.votes && celebrity.votes.length > 0) {
                    mbtiType = celebrity.votes[0].mbti_type;
                }
                
                celebrityCard.innerHTML = `
                    <div class="w-20 h-20 bg-primary-100 rounded-full mx-auto mb-4 flex items-center justify-center">
                        <span class="text-2xl font-bold text-primary-600">${celebrity.name.charAt(0)}</span>
                    </div>
                    <h3 class="text-lg font-semibold text-gray-900 mb-1">${celebrity.name}</h3>
                    <p class="text-sm text-gray-600 mb-2">${celebrity.name_en || ''}</p>
                    <div class="inline-block bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm font-medium mb-2">
                        ${mbtiType}
                    </div>
                    <p class="text-xs text-gray-500 line-clamp-2">${celebrity.description || ''}</p>
                `;
                
                // Add click event to navigate to celebrity detail
                celebrityCard.style.cursor = 'pointer';
                celebrityCard.addEventListener('click', () => {
                    window.location.href = `/celebrities/${celebrity.id}`;
                });
                
                container.appendChild(celebrityCard);
            });
        } else {
            container.innerHTML = `
                <div class="col-span-full text-center text-gray-500 py-8">
                    <div class="w-16 h-16 bg-gray-200 rounded-full mx-auto mb-4 flex items-center justify-center">
                        <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                        </svg>
                    </div>
                    <p class="text-lg font-medium">暂无名人数据</p>
                    <p class="text-sm">名人数据库正在建设中...</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Failed to load celebrities:', error);
        const container = document.getElementById('celebritiesPreview');
        if (container) {
            container.innerHTML = `
                <div class="col-span-full text-center text-gray-500 py-8">
                    <div class="w-16 h-16 bg-gray-200 rounded-full mx-auto mb-4 flex items-center justify-center">
                        <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                        </svg>
                    </div>
                    <p class="text-lg font-medium">加载失败</p>
                    <p class="text-sm">无法加载名人数据，请稍后重试</p>
                </div>
            `;
        }
    }
} 