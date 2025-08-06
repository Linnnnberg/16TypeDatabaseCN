// Main JavaScript for MBTI Roster

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
        const response = await apiCall('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        if (response.access_token) {
            setToken(response.access_token);
            showMessage('登录成功！', 'success');
            hideModal('loginModal');
            updateAuthUI();
            return true;
        }
    } catch (error) {
        showMessage('登录失败: ' + error.message, 'error');
        return false;
    }
}

async function signupUser(name, email, password) {
    try {
        const response = await apiCall('/auth/signup', {
            method: 'POST',
            body: JSON.stringify({ name, email, password })
        });
        
        if (response.access_token) {
            setToken(response.access_token);
            showMessage('注册成功！', 'success');
            hideModal('signupModal');
            updateAuthUI();
            return true;
        }
    } catch (error) {
        showMessage('注册失败: ' + error.message, 'error');
        return false;
    }
}

function logoutUser() {
    removeToken();
    updateAuthUI();
    showMessage('已退出登录', 'info');
}

function updateAuthUI() {
    const token = getToken();
    const loginBtn = document.getElementById('loginBtn');
    const signupBtn = document.getElementById('signupBtn');
    
    if (token) {
        // User is logged in
        if (loginBtn) loginBtn.textContent = '退出';
        if (signupBtn) signupBtn.style.display = 'none';
    } else {
        // User is not logged in
        if (loginBtn) loginBtn.textContent = '登录';
        if (signupBtn) signupBtn.style.display = 'inline-block';
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('MBTI Roster website loaded successfully!');
    
    // Initialize authentication UI
    updateAuthUI();
    
    // Login button event listener
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', function() {
            const token = getToken();
            if (token) {
                // User is logged in, show logout
                logoutUser();
            } else {
                // User is not logged in, show login modal
                showModal('loginModal');
            }
        });
    }
    
    // Signup button event listener
    const signupBtn = document.getElementById('signupBtn');
    if (signupBtn) {
        signupBtn.addEventListener('click', function() {
            showModal('signupModal');
        });
    }
    
    // Close modal buttons
    const closeLoginModal = document.getElementById('closeLoginModal');
    if (closeLoginModal) {
        closeLoginModal.addEventListener('click', function() {
            hideModal('loginModal');
        });
    }
    
    const closeSignupModal = document.getElementById('closeSignupModal');
    if (closeSignupModal) {
        closeSignupModal.addEventListener('click', function() {
            hideModal('signupModal');
        });
    }
    
    // Switch between modals
    const switchToSignup = document.getElementById('switchToSignup');
    if (switchToSignup) {
        switchToSignup.addEventListener('click', function() {
            switchModal('loginModal', 'signupModal');
        });
    }
    
    const switchToLogin = document.getElementById('switchToLogin');
    if (switchToLogin) {
        switchToLogin.addEventListener('click', function() {
            switchModal('signupModal', 'loginModal');
        });
    }
    
    // Login form submission
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
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
    if (signupForm) {
        signupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const name = document.getElementById('signupName').value;
            const email = document.getElementById('signupEmail').value;
            const password = document.getElementById('signupPassword').value;
            const confirmPassword = document.getElementById('signupConfirmPassword').value;
            
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
        if (modal) {
            modal.addEventListener('click', function(e) {
                if (e.target === modal) {
                    hideModal(modalId);
                }
            });
        }
    });
    
    showMessage('Website ready!', 'success');
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