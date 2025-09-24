// Namma Traffic AI - Dashboard JavaScript

class TrafficDashboard {
    constructor() {
        this.socket = null;
        this.charts = {};
        this.trafficData = {};
        this.signalStates = {};
        this.systemStats = {};
        this.alerts = [];
        this.isConnected = false;
        
        this.initializeSocket();
        this.setupEventListeners();
        this.startClock();
    }

    initializeSocket() {
        try {
            this.socket = io();
            
            this.socket.on('connect', () => {
                this.isConnected = true;
                this.updateConnectionStatus(true);
                this.addAlert('info', 'Connected to Namma Traffic AI system', 'success');
            });

            this.socket.on('disconnect', () => {
                this.isConnected = false;
                this.updateConnectionStatus(false);
                this.addAlert('error', 'Disconnected from system', 'error');
            });

            this.socket.on('traffic_update', (data) => {
                this.handleTrafficUpdate(data);
            });

            this.socket.on('connected', (data) => {
                console.log('Socket connected:', data);
            });

        } catch (error) {
            console.error('Socket initialization failed:', error);
            this.simulateData(); // Fallback to simulation if socket fails
        }
    }

    simulateData() {
        // Fallback simulation for demo purposes
        setInterval(() => {
            this.generateSimulatedData();
        }, 2000);
    }

    generateSimulatedData() {
        // Generate realistic simulated data
        const points = Object.keys(trafficPoints);
        const simulatedTrafficData = {};
        const simulatedSignalStates = {};

        points.forEach(pointId => {
            const hour = new Date().getHours();
            const isRushHour = (hour >= 8 && hour <= 10) || (hour >= 17 && hour <= 20);
            
            simulatedTrafficData[pointId] = {
                vehicle_count: Math.floor(Math.random() * (isRushHour ? 300 : 150)) + 50,
                congestion_level: Math.floor(Math.random() * (isRushHour ? 80 : 50)) + 20,
                average_speed: Math.floor(Math.random() * 40) + 20,
                queue_length: Math.floor(Math.random() * 20),
                wait_time: Math.floor(Math.random() * 60) + 10
            };

            const currentState = ['red', 'yellow', 'green'][Math.floor(Math.random() * 3)];
            simulatedSignalStates[pointId] = {
                current_state: currentState,
                time_remaining: Math.floor(Math.random() * 60) + 10,
                auto_mode: true,
                vehicles_waiting: Math.floor(Math.random() * 50) + 10
            };
        });

        const simulatedStats = {
            total_vehicles_processed: Math.floor(Math.random() * 10000) + 50000,
            average_wait_time: Math.floor(Math.random() * 30) + 15,
            commute_time_reduction: (Math.random() * 0.12).toFixed(3),
            system_efficiency: Math.floor(Math.random() * 20) + 75
        };

        this.handleTrafficUpdate({
            traffic_data: simulatedTrafficData,
            signal_states: simulatedSignalStates,
            system_stats: simulatedStats
        });
    }

    handleTrafficUpdate(data) {
        this.trafficData = data.traffic_data || {};
        this.signalStates = data.signal_states || {};
        this.systemStats = data.system_stats || {};

        this.updateSystemStats();
        this.updateTrafficPoints();
        this.updateCharts();
    }

    updateSystemStats() {
        const commuteReduction = (this.systemStats.commute_time_reduction * 100).toFixed(1);
        const efficiency = this.systemStats.system_efficiency || 0;
        const avgWaitTime = this.systemStats.average_wait_time || 0;
        const totalVehicles = this.systemStats.total_vehicles_processed || 0;

        // Update DOM elements
        this.updateElement('commute-reduction', `${commuteReduction}%`);
        this.updateElement('system-efficiency', `${efficiency}%`);
        this.updateElement('avg-wait-time', `${avgWaitTime}s`);
        this.updateElement('total-vehicles', totalVehicles.toLocaleString());

        // Update progress indicators
        this.updateCommuteReductionProgress(commuteReduction);
    }

    updateCommuteReductionProgress(percentage) {
        const target = 10; // 10% target
        const progress = Math.min(100, (percentage / target) * 100);
        
        // Color coding based on progress
        const element = document.getElementById('commute-reduction');
        if (element) {
            if (percentage >= target) {
                element.style.color = '#27ae60'; // Green - target achieved
            } else if (percentage >= target * 0.7) {
                element.style.color = '#f39c12'; // Orange - getting close
            } else {
                element.style.color = '#e74c3c'; // Red - needs improvement
            }
        }
    }

    updateTrafficPoints() {
        Object.keys(this.trafficData).forEach(pointId => {
            const trafficInfo = this.trafficData[pointId];
            const signalInfo = this.signalStates[pointId];

            if (!trafficInfo || !signalInfo) return;

            // Update metrics
            this.updateElement(`vehicles-${pointId}`, trafficInfo.vehicle_count);
            this.updateElement(`speed-${pointId}`, `${trafficInfo.average_speed} km/h`);
            this.updateElement(`congestion-${pointId}`, `${trafficInfo.congestion_level}%`);
            
            // Update congestion bar
            this.updateCongestionBar(pointId, trafficInfo.congestion_level);
            
            // Update traffic light
            this.updateTrafficLight(pointId, signalInfo);
            
            // Update timer
            this.updateElement(`timer-${pointId}`, `${signalInfo.time_remaining}s`);
            
            // Update control buttons
            this.updateControlButtons(pointId, signalInfo.auto_mode);
        });
    }

    updateTrafficLight(pointId, signalInfo) {
        const states = ['red', 'yellow', 'green'];
        
        states.forEach(state => {
            const element = document.getElementById(`${state}-${pointId}`);
            if (element) {
                element.classList.toggle('active', state === signalInfo.current_state);
            }
        });
    }

    updateCongestionBar(pointId, congestionLevel) {
        const bar = document.getElementById(`congestion-bar-${pointId}`);
        if (bar) {
            bar.style.width = `${congestionLevel}%`;
            
            // Update color based on congestion level
            if (congestionLevel < 30) {
                bar.style.background = '#27ae60'; // Green
            } else if (congestionLevel < 60) {
                bar.style.background = '#f39c12'; // Orange
            } else {
                bar.style.background = '#e74c3c'; // Red
            }
        }
    }

    updateControlButtons(pointId, isAutoMode) {
        const autoBtn = document.querySelector(`[data-point-id="${pointId}"] .control-btn.auto`);
        const manualBtn = document.querySelector(`[data-point-id="${pointId}"] .control-btn.manual`);
        
        if (autoBtn && manualBtn) {
            autoBtn.classList.toggle('active', isAutoMode);
            manualBtn.classList.toggle('active', !isAutoMode);
        }
    }

    updateCharts() {
        // Update traffic flow chart
        this.updateTrafficFlowChart();
        
        // Update performance chart
        this.updatePerformanceChart();
    }

    updateTrafficFlowChart() {
        const chartDiv = document.getElementById('traffic-flow-chart');
        if (!chartDiv) return;

        const points = Object.keys(this.trafficData);
        const vehicleCounts = points.map(p => this.trafficData[p]?.vehicle_count || 0);
        const pointNames = points.map(p => trafficPoints[p]?.name || p);

        const trace = {
            x: pointNames,
            y: vehicleCounts,
            type: 'bar',
            marker: {
                color: vehicleCounts.map(count => {
                    if (count < 100) return '#27ae60';
                    if (count < 200) return '#f39c12';
                    return '#e74c3c';
                })
            }
        };

        const layout = {
            title: 'Current Vehicle Count by Location',
            xaxis: { title: 'Traffic Points' },
            yaxis: { title: 'Vehicle Count' },
            margin: { t: 50, l: 50, r: 20, b: 100 },
            height: 180
        };

        try {
            Plotly.newPlot(chartDiv, [trace], layout, { responsive: true });
        } catch (error) {
            chartDiv.innerHTML = '<p style="text-align: center; color: #95a5a6;">Chart loading...</p>';
        }
    }

    updatePerformanceChart() {
        const chartDiv = document.getElementById('performance-chart');
        if (!chartDiv) return;

        const efficiency = this.systemStats.system_efficiency || 0;
        const commuteReduction = (this.systemStats.commute_time_reduction * 100) || 0;
        const targetReduction = 10;

        const trace1 = {
            x: ['System Efficiency', 'Commute Reduction', 'Target'],
            y: [efficiency, commuteReduction, targetReduction],
            type: 'bar',
            marker: {
                color: ['#3498db', '#27ae60', '#95a5a6']
            }
        };

        const layout = {
            title: 'Performance Metrics',
            yaxis: { title: 'Percentage (%)' },
            margin: { t: 50, l: 50, r: 20, b: 50 },
            height: 180
        };

        try {
            Plotly.newPlot(chartDiv, [trace1], layout, { responsive: true });
        } catch (error) {
            chartDiv.innerHTML = '<p style="text-align: center; color: #95a5a6;">Chart loading...</p>';
        }
    }

    updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }

    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connection-status');
        if (statusElement) {
            statusElement.classList.toggle('connected', connected);
            statusElement.classList.toggle('disconnected', !connected);
            
            const statusText = statusElement.querySelector('span');
            const statusIcon = statusElement.querySelector('i');
            
            if (statusText) {
                statusText.textContent = connected ? 'Connected' : 'Disconnected';
            }
            
            if (statusIcon) {
                statusIcon.style.color = connected ? '#27ae60' : '#e74c3c';
            }
        }
    }

    addAlert(type, message, alertClass = 'info') {
        const alertsList = document.getElementById('alerts-list');
        if (!alertsList) return;

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert-item ${alertClass}`;
        
        const iconClass = {
            'info': 'fas fa-info-circle',
            'warning': 'fas fa-exclamation-triangle',
            'error': 'fas fa-times-circle',
            'success': 'fas fa-check-circle'
        }[type] || 'fas fa-info-circle';

        alertDiv.innerHTML = `
            <i class="${iconClass}"></i>
            <span>${message}</span>
            <small>${new Date().toLocaleTimeString()}</small>
        `;

        // Insert at the top
        alertsList.insertBefore(alertDiv, alertsList.firstChild);

        // Keep only last 10 alerts
        while (alertsList.children.length > 10) {
            alertsList.removeChild(alertsList.lastChild);
        }

        // Auto-remove after 10 seconds for non-error alerts
        if (alertClass !== 'error') {
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.parentNode.removeChild(alertDiv);
                }
            }, 10000);
        }
    }

    startClock() {
        const updateClock = () => {
            const now = new Date();
            const timeString = now.toLocaleTimeString();
            const dateString = now.toLocaleDateString();
            
            this.updateElement('system-time', `${dateString} ${timeString}`);
            this.updateElement('init-time', timeString);
        };

        updateClock();
        setInterval(updateClock, 1000);
    }

    setupEventListeners() {
        // Emergency mode button
        const emergencyBtn = document.querySelector('.emergency-btn');
        if (emergencyBtn) {
            emergencyBtn.addEventListener('click', () => this.emergencyMode());
        }

        // Reset system button
        const resetBtn = document.querySelector('.reset-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.resetSystem());
        }

        // AI settings
        const aiSettings = document.getElementById('ai-aggressiveness');
        const updateFreq = document.getElementById('update-frequency');
        
        if (aiSettings) {
            aiSettings.addEventListener('change', () => this.updateAISettings());
        }
        
        if (updateFreq) {
            updateFreq.addEventListener('change', () => this.updateAISettings());
        }
    }

    // Control functions
    emergencyMode() {
        this.addAlert('warning', 'Emergency mode activated - All signals set to default timing', 'warning');
        
        // In a real system, this would send emergency signal to backend
        if (this.socket && this.socket.connected) {
            this.socket.emit('emergency_mode', { active: true });
        }
    }

    resetSystem() {
        this.addAlert('info', 'System reset initiated - Returning to default settings', 'info');
        
        if (this.socket && this.socket.connected) {
            this.socket.emit('reset_system', {});
        }
    }

    updateAISettings() {
        const aggressiveness = document.getElementById('ai-aggressiveness')?.value;
        const frequency = document.getElementById('update-frequency')?.value;
        
        if (this.socket && this.socket.connected) {
            this.socket.emit('update_ai_settings', {
                aggressiveness,
                frequency: parseInt(frequency)
            });
        }
        
        this.addAlert('info', `AI settings updated: ${aggressiveness} mode, ${frequency}s updates`, 'info');
    }
}

// Global functions for HTML onclick handlers
function toggleMode(pointId) {
    if (window.dashboard && window.dashboard.socket && window.dashboard.socket.connected) {
        window.dashboard.socket.emit('toggle_signal_mode', { point_id: pointId });
    }
    
    window.dashboard?.addAlert('info', `Signal mode toggled for ${trafficPoints[pointId]?.name}`, 'info');
}

function emergencyMode() {
    window.dashboard?.emergencyMode();
}

function resetSystem() {
    window.dashboard?.resetSystem();
}

function updateAISettings() {
    window.dashboard?.updateAISettings();
}

// Initialize dashboard
function initializeDashboard() {
    window.dashboard = new TrafficDashboard();
    
    // Add welcome message
    setTimeout(() => {
        window.dashboard.addAlert('info', 'Welcome to Namma Traffic AI - Monitoring Bangalore traffic in real-time', 'success');
    }, 1000);
}

// Handle page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize if not already done
    if (!window.dashboard) {
        initializeDashboard();
    }
});

// Export for use in HTML
window.TrafficDashboard = TrafficDashboard;
window.initializeDashboard = initializeDashboard;
window.toggleMode = toggleMode;
window.emergencyMode = emergencyMode;
window.resetSystem = resetSystem;
window.updateAISettings = updateAISettings;