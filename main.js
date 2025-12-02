// HFRL Integration Hub - Main JavaScript
class HFRLApp {
    constructor() {
        this.models = [
            {
                id: 'deepseek-chat',
                name: 'Deepseek Chat',
                provider: 'deepseek',
                status: 'available',
                description: 'Advanced conversational AI',
                maxTokens: 4000,
                temperature: 0.7
            },
            {
                id: 'kimi-k2',
                name: 'Kimi K2',
                provider: 'kimi',
                status: 'available',
                description: 'Creative content generation',
                maxTokens: 8000,
                temperature: 0.8
            },
            {
                id: 'gpt-4',
                name: 'GPT-4',
                provider: 'openai',
                status: 'available',
                description: 'Multi-modal AI assistant',
                maxTokens: 8000,
                temperature: 0.6
            },
            {
                id: 'claude-3',
                name: 'Claude 3',
                provider: 'anthropic',
                status: 'available',
                description: 'Helpful and harmless AI',
                maxTokens: 200000,
                temperature: 0.5
            }
        ];
        
        this.currentModel = null;
        this.isGenerating = false;
        this.feedbackData = [];
        this.performanceHistory = [];
        
        this.init();
    }
    
    init() {
        this.setupParticleBackground();
        this.setupAnimations();
        this.setupEventListeners();
        this.populateModelGrid();
        this.initializeCharts();
        this.setupFileUpload();
        this.loadMockData();
        this.displayAPIKeyStatus();
    }
    
    displayAPIKeyStatus() {
        const statusContainer = document.getElementById('api-keys-status');
        if (!statusContainer) return;
        
        console.log('Checking API key status from localStorage...');
        
        const providers = [
            { id: 'openai', name: 'OpenAI' },
            { id: 'anthropic', name: 'Anthropic' },
            { id: 'deepseek', name: 'Deepseek' },
            { id: 'kimi', name: 'Kimi K2' }
        ];
        
        let html = '';
        providers.forEach(provider => {
            const apiKey = localStorage.getItem(`${provider.id}_api_key`);
            const hasKey = apiKey && apiKey.length > 0;
            
            console.log(`${provider.id}_api_key: ${hasKey ? 'found (' + apiKey.length + ' chars)' : 'not found'}`);
            
            const statusIcon = hasKey ? '✓' : '✗';
            const statusColor = hasKey ? 'text-green-400' : 'text-red-400';
            const statusText = hasKey ? 'Configured' : 'Not configured';
            
            html += `<div class="flex items-center justify-between">
                <span>${provider.name}:</span>
                <span class="${statusColor}">${statusIcon} ${statusText}</span>
            </div>`;
        });
        
        statusContainer.innerHTML = html;
    }
    
    setupParticleBackground() {
        // Create particle system using p5.js
        const sketch = (p) => {
            let particles = [];
            
            p.setup = () => {
                const canvas = p.createCanvas(p.windowWidth, p.windowHeight);
                canvas.parent('particle-bg');
                
                // Create particles
                for (let i = 0; i < 100; i++) {
                    particles.push({
                        x: p.random(p.width),
                        y: p.random(p.height),
                        vx: p.random(-0.5, 0.5),
                        vy: p.random(-0.5, 0.5),
                        size: p.random(1, 3),
                        opacity: p.random(0.3, 0.8)
                    });
                }
            };
            
            p.draw = () => {
                p.clear();
                
                // Update and draw particles
                particles.forEach(particle => {
                    particle.x += particle.vx;
                    particle.y += particle.vy;
                    
                    // Wrap around edges
                    if (particle.x < 0) particle.x = p.width;
                    if (particle.x > p.width) particle.x = 0;
                    if (particle.y < 0) particle.y = p.height;
                    if (particle.y > p.height) particle.y = 0;
                    
                    // Draw particle
                    p.fill(0, 255, 255, particle.opacity * 255);
                    p.noStroke();
                    p.circle(particle.x, particle.y, particle.size);
                    
                    // Draw connections to nearby particles
                    particles.forEach(other => {
                        const distance = p.dist(particle.x, particle.y, other.x, other.y);
                        if (distance < 100) {
                            p.stroke(255, 0, 255, (1 - distance / 100) * 50);
                            p.strokeWeight(0.5);
                            p.line(particle.x, particle.y, other.x, other.y);
                        }
                    });
                });
            };
            
            p.windowResized = () => {
                p.resizeCanvas(p.windowWidth, p.windowHeight);
            };
        };
        
        new p5(sketch);
    }
    
    setupAnimations() {
        // Initialize Splitting.js for text animations
        Splitting();
        
        // Animate hero text
        anime({
            targets: '[data-splitting] .char',
            translateY: [100, 0],
            opacity: [0, 1],
            easing: 'easeOutExpo',
            duration: 1400,
            delay: anime.stagger(30)
        });
        
        // Setup typed.js for description
        new Typed('#typed-description', {
            strings: [
                'Train AI models through human feedback integration.',
                'Improve response quality with reinforcement learning.',
                'Build better AI systems with collaborative training.',
                'Transform AI development with human-in-the-loop learning.'
            ],
            typeSpeed: 50,
            backSpeed: 30,
            backDelay: 2000,
            loop: true,
            showCursor: true,
            cursorChar: '|'
        });
        
        // Animate elements on scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    anime({
                        targets: entry.target,
                        translateY: [50, 0],
                        opacity: [0, 1],
                        easing: 'easeOutQuad',
                        duration: 800,
                        delay: 200
                    });
                }
            });
        }, observerOptions);
        
        // Observe all sections
        document.querySelectorAll('section').forEach(section => {
            observer.observe(section);
        });
    }
    
    setupEventListeners() {
        // Temperature slider
        const tempSlider = document.getElementById('temperature');
        const tempValue = document.getElementById('temp-value');
        tempSlider.addEventListener('input', (e) => {
            tempValue.textContent = e.target.value;
        });
        
        // Max tokens slider
        const tokensSlider = document.getElementById('max-tokens');
        const tokensValue = document.getElementById('tokens-value');
        tokensSlider.addEventListener('input', (e) => {
            tokensValue.textContent = e.target.value;
        });
        
        // Quality rating stars
        const qualityStars = document.querySelectorAll('.quality-star');
        qualityStars.forEach(star => {
            star.addEventListener('click', (e) => {
                const rating = parseInt(e.target.dataset.rating);
                this.setQualityRating(rating);
            });
            
            star.addEventListener('mouseenter', (e) => {
                const rating = parseInt(e.target.dataset.rating);
                this.highlightStars(rating);
            });
        });
        
        document.getElementById('quality-rating').addEventListener('mouseleave', () => {
            this.resetStarHighlight();
        });
        
        // Model provider change
        document.getElementById('model-provider').addEventListener('change', (e) => {
            this.updateModelOptions(e.target.value);
        });
    }
    
    populateModelGrid() {
        const modelGrid = document.getElementById('model-grid');
        modelGrid.innerHTML = '';
        
        this.models.forEach(model => {
            const modelCard = document.createElement('div');
            modelCard.className = 'model-card p-4 cursor-pointer';
            modelCard.onclick = () => this.selectModel(model);
            
            modelCard.innerHTML = `
                <div class="flex items-center justify-between mb-3">
                    <h4 class="font-semibold text-white">${model.name}</h4>
                    <span class="status-indicator status-${model.status}"></span>
                </div>
                <p class="text-sm text-gray-400 mb-3">${model.description}</p>
                <div class="flex justify-between text-xs text-gray-500">
                    <span>Max: ${model.maxTokens}</span>
                    <span>Temp: ${model.temperature}</span>
                </div>
            `;
            
            modelGrid.appendChild(modelCard);
        });
    }
    
    selectModel(model) {
        this.currentModel = model;
        
        // Update UI to show selected model
        document.querySelectorAll('.model-card').forEach(card => {
            card.classList.remove('glow-cyan');
        });
        
        event.currentTarget.classList.add('glow-cyan');
        
        // Update configuration panel
        document.getElementById('model-provider').value = model.provider;
        
        // Show success message
        this.showNotification(`Selected ${model.name}`, 'success');
    }
    
    updateModelOptions(provider) {
        const availableModels = this.models.filter(model => model.provider === provider);
        this.populateModelGrid();
    }
    
    async testConnection() {
        const provider = document.getElementById('model-provider').value;
        const apiKey = localStorage.getItem(`${provider}_api_key`);
        
        if (!apiKey) {
            this.showNotification(`Please configure ${provider} API key in Settings first`, 'error');
            return;
        }
        
        const statusElement = document.getElementById('connection-status');
        statusElement.innerHTML = `
            <div class="flex items-center justify-center">
                <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-cyan-400 mr-2"></div>
                <span class="text-gray-400">Testing...</span>
            </div>
        `;
        
        try {
            // Call backend API to test connection
            const response = await fetch('http://localhost:8000/api/models/test-connection', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    provider: provider,
                    api_key: apiKey
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                statusElement.innerHTML = `
                    <span class="status-indicator status-connected"></span>
                    <span class="text-green-400">Connected</span>
                `;
                this.showNotification('Connection successful!', 'success');
            } else {
                statusElement.innerHTML = `
                    <span class="status-indicator status-disconnected"></span>
                    <span class="text-red-400">Failed</span>
                `;
                this.showNotification(`Connection failed: ${data.message}`, 'error');
            }
        } catch (error) {
            statusElement.innerHTML = `
                <span class="status-indicator status-disconnected"></span>
                <span class="text-red-400">Error</span>
            `;
            this.showNotification('Connection test failed. Check backend server.', 'error');
            console.error('Connection test error:', error);
        }
    }
    
    setupFileUpload() {
        const uploadZone = document.getElementById('upload-zone');
        const fileInput = document.getElementById('file-input');
        const uploadedFiles = document.getElementById('uploaded-files');
        
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('border-cyan-400');
        });
        
        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('border-cyan-400');
        });
        
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('border-cyan-400');
            this.handleFiles(e.dataTransfer.files);
        });
        
        fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });
    }
    
    handleFiles(files) {
        const uploadedFiles = document.getElementById('uploaded-files');
        
        Array.from(files).forEach(file => {
            const fileElement = document.createElement('div');
            fileElement.className = 'flex items-center justify-between p-3 bg-gray-800 rounded-lg';
            fileElement.innerHTML = `
                <div class="flex items-center space-x-3">
                    <span class="text-cyan-400">📄</span>
                    <span class="text-white">${file.name}</span>
                    <span class="text-gray-400 text-sm">(${(file.size / 1024).toFixed(1)} KB)</span>
                </div>
                <button onclick="this.parentElement.remove()" class="text-red-400 hover:text-red-300">✕</button>
            `;
            uploadedFiles.appendChild(fileElement);
        });
    }
    
    async generateContent() {
        if (this.isGenerating) return;
        
        const prompt = document.getElementById('prompt-input').value;
        if (!prompt.trim()) {
            this.showNotification('Please enter a prompt', 'error');
            return;
        }
        
        if (!this.currentModel) {
            this.showNotification('Please select a model first', 'error');
            return;
        }
        
        // Get API key from localStorage
        const apiKey = localStorage.getItem(`${this.currentModel.provider}_api_key`);
        if (!apiKey) {
            this.showNotification(`Please configure ${this.currentModel.provider} API key in Settings`, 'error');
            return;
        }
        
        this.isGenerating = true;
        this.showGenerationProgress();
        
        try {
            const temperature = parseFloat(document.getElementById('temperature').value);
            const maxTokens = parseInt(document.getElementById('max-tokens').value);
            
            // Call backend API
            const response = await fetch('http://localhost:8000/api/models/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': apiKey
                },
                body: JSON.stringify({
                    prompt: prompt,
                    provider: this.currentModel.provider,
                    model: this.currentModel.id,
                    temperature: temperature,
                    max_tokens: maxTokens
                })
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Generation failed');
            }
            
            const data = await response.json();
            this.updateProgress(100);
            this.displayResponse(data.content);
            this.isGenerating = false;
            
        } catch (error) {
            this.isGenerating = false;
            this.showNotification(`Generation failed: ${error.message}`, 'error');
            console.error('Generation error:', error);
            document.getElementById('generation-progress').classList.add('hidden');
            
            // Fallback to mock data if backend is not available
            this.generateMockContent();
        }
    }
    
    generateMockContent() {
        this.isGenerating = true;
        this.showGenerationProgress();
        
        // Simulate AI generation with mock data
        const responses = [
            `Based on your request, here's a comprehensive analysis of the character dialogue patterns:\n\nThe protagonist exhibits a complex emotional arc through their speech patterns. In the opening scenes, their dialogue is characterized by short, fragmented sentences that reflect their internal turmoil. As the narrative progresses, we observe a shift toward more complex syntactic structures, indicating character growth and emotional stability.\n\nKey dialogue features:\n• Initial hesitation patterns ("I... I don't know if...")
• Gradual confidence building ("I believe we should consider...")
• Final assertiveness ("We will implement this strategy.")\n\nThis progression creates a satisfying character arc that readers can follow through linguistic cues alone.`,
            
            `Here's the generated code based on your specifications:\n\n\`\`\`javascript
async function processUserFeedback(feedbackData) {
    try {
        const feedbackScores = feedbackData.map(item => ({
            quality: item.rating,
            relevance: item.relevanceScore,
            timestamp: new Date(item.timestamp)
        }));
        
        const averageScore = feedbackScores.reduce((sum, item) => 
            sum + (item.quality + item.relevance) / 2, 0
        ) / feedbackScores.length;
        
        return {
            success: true,
            averageScore: Math.round(averageScore * 100) / 100,
            totalFeedback: feedbackScores.length,
            recommendations: generateRecommendations(averageScore)
        };
    } catch (error) {
        console.error('Feedback processing error:', error);
        return { success: false, error: error.message };
    }
}\n\`\`\`\n\nThis function efficiently processes user feedback data and provides actionable insights for model improvement.`,
            
            `The data analysis reveals significant patterns in user behavior:\n\n**Key Findings:**\n• 73% improvement in response quality over training sessions\n• User engagement increased by 45% with personalized feedback\n• Model accuracy improved from 68% to 89% over 50 iterations\n\n**Recommendations:** \n1. Continue iterative training approach\n2. Implement real-time feedback integration\n3. Expand training dataset for broader coverage\n4. Monitor for potential overfitting scenarios`,
            
            `Character dialogue sample:\n\n**Scene: Coffee shop confrontation**\n\nSARAH: (nervously stirring coffee) "I know what you did, Marcus. The files... they're all gone."\n\nMARCUS: (leaning back, feigning calm) "I have no idea what you're talking about. Maybe you misplaced them?"\n\nSARAH: (voice rising) "Don't insult my intelligence. I saw you access the server at 2 AM. The security logs don't lie."\n\nMARCUS: (sighs, defeated) "Sarah, you don't understand the pressure I'm under. They have my sister."\n\nSARAH: (pauses, conflicted) "Then we help her together. But don't ever lie to me again."
        `];
        
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];
        
        // Simulate progressive generation
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                this.displayResponse(randomResponse);
                this.isGenerating = false;
            }
            this.updateProgress(progress);
        }, 200);
    }
    
    showGenerationProgress() {
        const progressContainer = document.getElementById('generation-progress');
        progressContainer.classList.remove('hidden');
        this.updateProgress(0);
    }
    
    updateProgress(percent) {
        const progressBar = document.getElementById('progress-bar');
        const progressPercent = document.getElementById('progress-percent');
        
        progressBar.style.width = `${percent}%`;
        progressPercent.textContent = `${Math.round(percent)}%`;
        
        if (percent >= 100) {
            setTimeout(() => {
                document.getElementById('generation-progress').classList.add('hidden');
            }, 500);
        }
    }
    
    displayResponse(responseText) {
        const container = document.getElementById('response-container');
        container.innerHTML = '';
        
        const responseElement = document.createElement('div');
        responseElement.className = 'fira-code text-sm leading-relaxed text-gray-300';
        
        // Add feedback functionality to response text
        const processText = (text) => {
            return text.replace(/\b(\w+)\b/g, (match) => {
                if (Math.random() > 0.8) { // 20% of words are clickable
                    return `<span class="feedback-highlight" onclick="app.addFeedback('${match}', event)">${match}</span>`;
                }
                return match;
            });
        };
        
        responseElement.innerHTML = processText(responseText);
        container.appendChild(responseElement);
        
        // Animate response appearance
        anime({
            targets: responseElement,
            opacity: [0, 1],
            translateY: [20, 0],
            duration: 800,
            easing: 'easeOutQuad'
        });
    }
    
    addFeedback(word, event) {
        const feedback = prompt(`Provide feedback for "${word}":`);
        if (feedback) {
            this.feedbackData.push({
                word,
                feedback,
                timestamp: new Date(),
                type: 'inline'
            });
            
            this.showNotification('Feedback added!', 'success');
            
            // Visual feedback
            event.target.style.background = 'linear-gradient(90deg, rgba(255, 215, 0, 0.5), rgba(255, 165, 0, 0.5))';
        }
    }
    
    setQualityRating(rating) {
        const stars = document.querySelectorAll('.quality-star');
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.remove('text-gray-600');
                star.classList.add('text-yellow-400');
            } else {
                star.classList.remove('text-yellow-400');
                star.classList.add('text-gray-600');
            }
        });
        
        this.currentRating = rating;
    }
    
    highlightStars(rating) {
        const stars = document.querySelectorAll('.quality-star');
        stars.forEach((star, index) => {
            if (index < rating) {
                star.style.color = '#FBBF24';
            } else {
                star.style.color = '#6B7280';
            }
        });
    }
    
    resetStarHighlight() {
        const stars = document.querySelectorAll('.quality-star');
        stars.forEach((star, index) => {
            if (this.currentRating && index < this.currentRating) {
                star.style.color = '#FBBF24';
            } else {
                star.style.color = '#6B7280';
            }
        });
    }
    
    async submitFeedback() {
        const comments = document.getElementById('feedback-comments').value;
        const learningRate = document.getElementById('learning-rate').value;
        
        if (!this.currentRating && !comments.trim()) {
            this.showNotification('Please provide rating or comments', 'error');
            return;
        }
        
        const feedbackData = {
            rating: this.currentRating || 3,
            comments: comments,
            learning_rate: learningRate === 'low' ? 0.0001 : learningRate === 'high' ? 0.01 : 0.001,
            session_id: this.currentSessionId || `session_${Date.now()}`
        };
        
        try {
            // Send feedback to backend
            const response = await fetch('http://localhost:8000/api/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(feedbackData)
            });
            
            if (!response.ok) {
                throw new Error('Failed to submit feedback');
            }
            
            const data = await response.json();
            this.feedbackData.push(data);
            
            this.showNotification('Feedback submitted successfully!', 'success');
            this.updatePerformanceMetrics();
            this.clearFeedbackForm();
            
        } catch (error) {
            this.showNotification('Failed to submit feedback. Saving locally...', 'warning');
            this.feedbackData.push(feedbackData);
            this.clearFeedbackForm();
            console.error('Feedback submission error:', error);
        }
    }
    
    clearFeedbackForm() {
        document.getElementById('feedback-comments').value = '';
        this.setQualityRating(0);
        this.currentRating = null;
    }
    
    updatePerformanceMetrics() {
        // Update mock performance data
        const sessions = parseInt(document.getElementById('total-sessions').textContent) + 1;
        const currentAvg = parseFloat(document.getElementById('avg-quality').textContent);
        const newAvg = ((currentAvg * (sessions - 1)) + (this.currentRating || 4)) / sessions;
        
        document.getElementById('total-sessions').textContent = sessions;
        document.getElementById('avg-quality').textContent = newAvg.toFixed(1) + '/5';
        
        // Update charts
        this.updateCharts();
    }
    
    initializeCharts() {
        // Performance Chart
        const performanceChart = echarts.init(document.getElementById('performance-chart'));
        const performanceOption = {
            backgroundColor: 'transparent',
            textStyle: { color: '#ffffff' },
            tooltip: {
                trigger: 'axis',
                backgroundColor: 'rgba(0,0,0,0.8)',
                borderColor: '#00FFFF',
                textStyle: { color: '#ffffff' }
            },
            xAxis: {
                type: 'category',
                data: ['Session 1', 'Session 2', 'Session 3', 'Session 4', 'Session 5'],
                axisLine: { lineStyle: { color: '#6A0DAD' } },
                axisLabel: { color: '#ffffff' }
            },
            yAxis: {
                type: 'value',
                min: 0,
                max: 5,
                axisLine: { lineStyle: { color: '#6A0DAD' } },
                axisLabel: { color: '#ffffff' },
                splitLine: { lineStyle: { color: '#333' } }
            },
            series: [{
                data: [3.2, 3.8, 4.1, 4.3, 4.5],
                type: 'line',
                smooth: true,
                lineStyle: { color: '#00FFFF', width: 3 },
                itemStyle: { color: '#FF00FF' },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: 'rgba(0,255,255,0.3)' },
                        { offset: 1, color: 'rgba(255,0,255,0.1)' }
                    ])
                }
            }]
        };
        performanceChart.setOption(performanceOption);
        
        // Feedback Chart
        const feedbackChart = echarts.init(document.getElementById('feedback-chart'));
        const feedbackOption = {
            backgroundColor: 'transparent',
            textStyle: { color: '#ffffff' },
            tooltip: {
                trigger: 'item',
                backgroundColor: 'rgba(0,0,0,0.8)',
                borderColor: '#00FFFF',
                textStyle: { color: '#ffffff' }
            },
            series: [{
                type: 'pie',
                radius: ['40%', '70%'],
                data: [
                    { value: 35, name: 'Excellent', itemStyle: { color: '#4CAF50' } },
                    { value: 40, name: 'Good', itemStyle: { color: '#2196F3' } },
                    { value: 20, name: 'Average', itemStyle: { color: '#FF9800' } },
                    { value: 5, name: 'Poor', itemStyle: { color: '#f44336' } }
                ],
                label: { color: '#ffffff' },
                labelLine: { lineStyle: { color: '#ffffff' } }
            }]
        };
        feedbackChart.setOption(feedbackOption);
        
        // Store chart instances for updates
        this.charts = {
            performance: performanceChart,
            feedback: feedbackChart
        };
    }
    
    updateCharts() {
        // Update performance chart with new data
        const newDataPoint = Math.random() * 2 + 3; // Random value between 3-5
        const performanceOption = this.charts.performance.getOption();
        performanceOption.series[0].data.push(newDataPoint);
        
        if (performanceOption.series[0].data.length > 10) {
            performanceOption.series[0].data.shift();
        }
        
        this.charts.performance.setOption(performanceOption);
    }
    
    loadMockData() {
        // Load some initial mock data for demonstration
        this.performanceHistory = [
            { session: 1, quality: 3.2, timestamp: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000) },
            { session: 2, quality: 3.8, timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000) },
            { session: 3, quality: 4.1, timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000) },
            { session: 4, quality: 4.3, timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000) },
            { session: 5, quality: 4.5, timestamp: new Date() }
        ];
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-20 right-6 z-50 p-4 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full`;
        
        // Set colors based on type
        switch (type) {
            case 'success':
                notification.classList.add('bg-green-600', 'text-white');
                break;
            case 'error':
                notification.classList.add('bg-red-600', 'text-white');
                break;
            case 'warning':
                notification.classList.add('bg-yellow-600', 'text-white');
                break;
            default:
                notification.classList.add('bg-cyan-600', 'text-white');
        }
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Animate out and remove
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Utility functions
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

function openDemoModal() {
    document.getElementById('demo-modal').classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeDemoModal() {
    document.getElementById('demo-modal').classList.add('hidden');
    document.body.style.overflow = 'auto';
}

function copyResponse() {
    const container = document.getElementById('response-container');
    const text = container.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        app.showNotification('Response copied to clipboard!', 'success');
    });
}

function exportResponse() {
    const container = document.getElementById('response-container');
    const text = container.textContent;
    
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ai-response.txt';
    a.click();
    URL.revokeObjectURL(url);
    
    app.showNotification('Response exported successfully!', 'success');
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new HFRLApp();
});

// Handle window resize for charts
window.addEventListener('resize', () => {
    if (window.app && window.app.charts) {
        Object.values(window.app.charts).forEach(chart => {
            chart.resize();
        });
    }
});