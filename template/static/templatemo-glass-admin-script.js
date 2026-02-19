/* ============================================
   TemplateMo 3D Glassmorphism Dashboard
   https://templatemo.com
   JavaScript
============================================ */

(function () {
    'use strict';

    // ============================================
    // Theme Toggle
    // ============================================
    function initThemeToggle() {
        const themeToggle = document.getElementById('theme-toggle');
        if (!themeToggle) return;

        const iconSun = themeToggle.querySelector('.icon-sun');
        const iconMoon = themeToggle.querySelector('.icon-moon');

        function setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);

            if (iconSun && iconMoon) {
                if (theme === 'light') {
                    iconSun.style.display = 'none';
                    iconMoon.style.display = 'block';
                } else {
                    iconSun.style.display = 'block';
                    iconMoon.style.display = 'none';
                }
            }
        }

        // Check for saved theme preference or default to dark
        const savedTheme = localStorage.getItem('theme') || 'dark';
        setTheme(savedTheme);

        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            setTheme(currentTheme === 'dark' ? 'light' : 'dark');
        });
    }

    // ============================================
    // 3D Tilt Effect
    // ============================================
    function initTiltEffect() {
        document.querySelectorAll('.glass-card-3d').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const rotateX = (y - centerY) / 20;
                const rotateY = (centerX - x) / 20;

                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
            });
        });
    }

    // ============================================
    // Animated Counters
    // ============================================
    function animateCounter(element, target, duration = 2000) {
        const start = 0;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing function
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(start + (target - start) * easeOut);

            if (element.dataset.prefix) {
                element.textContent = element.dataset.prefix + current.toLocaleString() + (element.dataset.suffix || '');
            } else {
                element.textContent = current.toLocaleString() + (element.dataset.suffix || '');
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    function initCounters() {
        const counters = document.querySelectorAll('.stat-value');
        counters.forEach(counter => {
            const text = counter.textContent;
            const value = parseInt(text.replace(/[^0-9]/g, ''));

            if (text.includes('$')) {
                counter.dataset.prefix = '$';
            }
            if (text.includes('%')) {
                counter.dataset.suffix = '%';
            }

            animateCounter(counter, value);
        });
    }

    // ============================================
    // Mobile Menu Toggle
    // ============================================
    function initMobileMenu() {
        const menuToggle = document.querySelector('.mobile-menu-toggle');
        const sidebar = document.getElementById('sidebar');

        if (menuToggle && sidebar) {
            menuToggle.addEventListener('click', () => {
                sidebar.classList.toggle('open');
            });

            // Close sidebar when clicking outside
            document.addEventListener('click', (e) => {
                if (sidebar.classList.contains('open') &&
                    !sidebar.contains(e.target) &&
                    !menuToggle.contains(e.target)) {
                    sidebar.classList.remove('open');
                }
            });
        }
    }

    // ============================================
    // Form Validation (for login/register)
    // ============================================
    function initFormValidation() {
        const forms = document.querySelectorAll('form[data-validate]');

        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();

                let isValid = true;
                const inputs = form.querySelectorAll('.form-input[required]');

                inputs.forEach(input => {
                    if (!input.value.trim()) {
                        isValid = false;
                        input.style.borderColor = '#ff6b6b';
                    } else {
                        input.style.borderColor = '';
                    }
                });

                // Email validation
                const emailInput = form.querySelector('input[type="email"]');
                if (emailInput && emailInput.value) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(emailInput.value)) {
                        isValid = false;
                        emailInput.style.borderColor = '#ff6b6b';
                    }
                }

                if (isValid) {
                    // Form is valid - you can add your submission logic here
                    console.log('Form is valid');
                    // For demo purposes, redirect to dashboard
                    if (form.dataset.redirect) {
                        window.location.href = form.dataset.redirect;
                    }
                }
            });
        });
    }

    // ============================================
    // Password Visibility Toggle
    // ============================================
    function initPasswordToggle() {
        const toggleButtons = document.querySelectorAll('.password-toggle');

        toggleButtons.forEach(button => {
            button.addEventListener('click', () => {
                const input = button.parentElement.querySelector('input');
                const icon = button.querySelector('svg');

                if (input.type === 'password') {
                    input.type = 'text';
                    icon.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';
                } else {
                    input.type = 'password';
                    icon.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
                }
            });
        });
    }

    // ============================================
    // Smooth Page Transitions
    // ============================================
    function initPageTransitions() {
        const links = document.querySelectorAll('a[href]');

        links.forEach(link => {
            // Skip if external
            if (link.hostname !== window.location.hostname) return;

            // Skip anchors and javascript links
            if (link.getAttribute('href').startsWith('#')) return;

            link.addEventListener('click', (e) => {
                e.preventDefault();

                const href = link.getAttribute('href');

                document.body.style.opacity = '0';
                document.body.style.transition = 'opacity 0.3s ease';

                setTimeout(() => {
                    window.location.href = href;
                }, 300);
            });
        });

        window.addEventListener('load', () => {
            document.body.style.opacity = '1';
        });
    }


    // ============================================
    // Settings Tab Navigation
    // ============================================
    function initSettingsTabs() {
        const tabLinks = document.querySelectorAll('.settings-nav-link[data-tab]');

        if (tabLinks.length === 0) return;

        tabLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();

                // Get target tab
                const tabId = link.getAttribute('data-tab');

                // Remove active class from all nav links
                document.querySelectorAll('.settings-nav-link').forEach(navLink => {
                    navLink.classList.remove('active');
                });

                // Add active class to clicked link
                link.classList.add('active');

                // Hide all tab contents
                document.querySelectorAll('.settings-tab-content').forEach(tab => {
                    tab.classList.remove('active');
                });

                // Show target tab content
                const targetTab = document.getElementById('tab-' + tabId);
                if (targetTab) {
                    targetTab.classList.add('active');
                }
            });
        });

        // Theme select sync with toggle
        const themeSelect = document.getElementById('theme-select');
        if (themeSelect) {
            const currentTheme = localStorage.getItem('theme') || 'dark';
            themeSelect.value = currentTheme;

            themeSelect.addEventListener('change', () => {
                const theme = themeSelect.value;
                if (theme === 'system') {
                    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                    document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
                } else {
                    document.documentElement.setAttribute('data-theme', theme);
                    localStorage.setItem('theme', theme);
                }

                // Update theme toggle icons
                const iconSun = document.querySelector('#theme-toggle .icon-sun');
                const iconMoon = document.querySelector('#theme-toggle .icon-moon');
                if (iconSun && iconMoon) {
                    const effectiveTheme = document.documentElement.getAttribute('data-theme');
                    if (effectiveTheme === 'light') {
                        iconSun.style.display = 'none';
                        iconMoon.style.display = 'block';
                    } else {
                        iconSun.style.display = 'block';
                        iconMoon.style.display = 'none';
                    }
                }
            });
        }
    }


    // ============================================
    // Fetch Total Cars Count
    // ============================================

    function animateCounter(element, target, duration = 2000) {
        const start = 0;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Ease-out cubic
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(start + (target - start) * easeOut);

            if (element.dataset.prefix) {
                element.textContent = element.dataset.prefix + current.toLocaleString() + (element.dataset.suffix || '');
            } else {
                element.textContent = current.toLocaleString() + (element.dataset.suffix || '');
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    // Fetch the number and animate once
    function fetchTotalCars() {
        fetch('http://127.0.0.1:8000/charts/total-cars')
            .then(response => response.json())
            .then(data => {
                const element = document.getElementById('total-cars');
                animateCounter(element, data.total, 2000); // animate over 2 seconds
            })
            .catch(error => console.error('Error fetching total cars:', error));
    }

    // Run only once when page loads
    window.addEventListener('DOMContentLoaded', fetchTotalCars);



    // ============================================
    // Fetch Fuel Type Count
    // ============================================

    function animateCounter(element, target, duration = 2000) {
        const start = 0;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Ease-out cubic
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(start + (target - start) * easeOut);

            if (element.dataset.prefix) {
                element.textContent = element.dataset.prefix + current.toLocaleString() + (element.dataset.suffix || '');
            } else {
                element.textContent = current.toLocaleString() + (element.dataset.suffix || '');
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    // Fetch the number and animate once
    function fetchFuelTypeCount() {
        fetch('http://127.0.0.1:8000/charts/fuel-types')
            .then(response => response.json())
            .then(data => {
                const element = document.getElementById('fuel-types');
                animateCounter(element, data.total, 2000); // animate over 2 seconds
            })
            .catch(error => console.error('Error fetching fuel type count:', error));
    }

    // Run only once when page loads
    window.addEventListener('DOMContentLoaded', fetchFuelTypeCount);


    // ============================================
    // Fetch Brand Count
    // ============================================

    function animateCounter(element, target, duration = 2000) {
        const start = 0;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Ease-out cubic
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(start + (target - start) * easeOut);

            if (element.dataset.prefix) {
                element.textContent = element.dataset.prefix + current.toLocaleString() + (element.dataset.suffix || '');
            } else {
                element.textContent = current.toLocaleString() + (element.dataset.suffix || '');
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    // Fetch the number and animate once
    function fetchBrandCount() {
        fetch('http://127.0.0.1:8000/charts/count-brands')
            .then(response => response.json())
            .then(data => {
                const element = document.getElementById('total-brands');
                animateCounter(element, data.brand_count, 2000); // animate over 2 seconds
            })
            .catch(error => console.error('Error fetching brand count:', error));
    }

    // Run only once when page loads
    window.addEventListener('DOMContentLoaded', fetchBrandCount);



    // ============================================
    // Fetch Model Count
    // ============================================

    function animateCounter(element, target, duration = 2000) {
        const start = 0;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Ease-out cubic
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(start + (target - start) * easeOut);

            if (element.dataset.prefix) {
                element.textContent = element.dataset.prefix + current.toLocaleString() + (element.dataset.suffix || '');
            } else {
                element.textContent = current.toLocaleString() + (element.dataset.suffix || '');
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    // Fetch the number and animate once
    function fetchModelCount() {
        fetch('http://127.0.0.1:8000/charts/count-models')
            .then(response => response.json())
            .then(data => {
                const element = document.getElementById('total-models');
                animateCounter(element, data.model_count, 2000); // animate over 2 seconds
            })
            .catch(error => console.error('Error fetching model count:', error));
    }

    // Run only once when page loads
    window.addEventListener('DOMContentLoaded', fetchModelCount);




    // ============================================
    // Fetch Model Per Models Data and Render Chart
    // ============================================
// ========================
// Color Per Bar (Dynamic)
// ========================
const colorPalette = [
    "#4BC0C0", "#FF6384", "#36A2EB", "#FFCE56", "#9966FF",
    "#FF9F40", "#E74C3C", "#3498DB", "#2ECC71", "#F39C12",
    "#A29BFE", "#FD79A8", "#55EFC4", "#FDCB6E", "#E17055",
    "#74B9FF", "#00CEC9", "#6C5CE7", "#FAB1A0", "#81ECEC",
    "#D63031", "#0984E3", "#00B894", "#E84393", "#FDCB6E",
    "#B2BEC3", "#636E72", "#2D3436", "#DFE6E9", "#F8EDEB"
];

function getColor(index) {
    return colorPalette[index % colorPalette.length];
}

// ========================
// Dynamic Y Axis
// ========================
function renderYAxis(maxCount, steps = 5) {
    const yAxis = document.querySelector('.chart-y-axis');
    if (!yAxis) return;

    yAxis.innerHTML = '';

    for (let i = steps; i >= 0; i--) {
        const value = Math.round((i / steps) * maxCount);
        const span = document.createElement('span');
        span.classList.add('y-value');
        span.textContent = value;
        yAxis.appendChild(span);
    }
}

// ========================
// Brands Per Model Chart
// ========================
function renderBrandsPerModelChart() {
    fetch('http://127.0.0.1:8000/charts/brands-per-model')
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('chart-placeholder');
            container.innerHTML = '';

            const maxCount = Math.max(...data.map(d => d.count)) || 1;

            renderYAxis(maxCount);

            data.forEach((item, index) => {
                const barGroup = document.createElement('div');
                barGroup.classList.add('chart-bar-group');

                const bar = document.createElement('div');
                bar.classList.add('chart-bar');

                const height = Math.round((item.count / maxCount) * 200);
                bar.style.height = '0px';
                // bar.style.backgroundColor = getColor(index); // ✅ unique color per bar
                bar.title = `${item.brand} - ${item.model}: ${item.count} cars`;

                barGroup.appendChild(bar);

                setTimeout(() => { bar.style.height = height + 'px'; }, 50);

                const label = document.createElement('span');
                label.classList.add('chart-label');
                label.textContent = item.model;
                barGroup.appendChild(label);

                container.appendChild(barGroup);
            });
        })
        .catch(err => console.error('Error loading brands per model:', err));
}


// ========================
// Owner type Per Price Chart
// ========================

function renderOwnerTypeChart() {
    fetch('http://127.0.0.1:8000/charts/owner-type-price')
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('owner-chart');
            const yAxis = document.getElementById('y-axis');

            container.innerHTML = '';
            yAxis.innerHTML = '';

            if (!data || data.length === 0) return;

            const colors = ['bar-emerald','bar-gold','bar-coral','bar-teal','bar-amber'];

            // ✅ Get max price
            const maxPrice = Math.max(...data.map(d => d.avg_price)) || 1;

            // ✅ Create Y-axis dynamically (5 steps)
            const steps = 5;
            for (let i = steps; i >= 0; i--) {
                const value = Math.round((maxPrice / steps) * i);

                const label = document.createElement('span');
                label.classList.add('y-value');

                // format (100000 -> 100K)
                label.textContent = value >= 1000 
                    ? (value / 1000).toFixed(0) + 'K'
                    : value;

                yAxis.appendChild(label);
            }

            // ✅ Create bars
            data.forEach((item, index) => {
                const barGroup = document.createElement('div');
                barGroup.classList.add('chart-bar-group');

                const bar = document.createElement('div');
                bar.classList.add('chart-bar', colors[index % colors.length]);

                const height = Math.round((item.avg_price / maxPrice) * 200);
                bar.style.height = '0px';

                // Tooltip
                bar.title = `Owner: ${item.owner_type}
Avg: ${item.avg_price}
Min: ${item.min_price}
Max: ${item.max_price}`;

                // Label
                const label = document.createElement('span');
                label.classList.add('chart-label');
                label.textContent = item.owner_type;

                barGroup.appendChild(bar);
                barGroup.appendChild(label);
                container.appendChild(barGroup);

                // Animate
                setTimeout(() => {
                    bar.style.height = height + 'px';
                }, 100);
            });
        })
        .catch(err => console.error('Error:', err));
}

window.addEventListener('DOMContentLoaded', renderOwnerTypeChart);


// ========================
// Random Car of the Day
// ========================
function loadRandomCar() {
    fetch('http://127.0.0.1:8000/charts/random-car')
        .then(res => res.json())
        .then(data => {
            const words = data.name.trim().split(' ');
            const initials = words.length >= 2
                ? words[0][0] + words[1][0]
                : words[0][0];

            document.getElementById('car-initials').textContent = initials.toUpperCase();
            document.getElementById('car-name').textContent = data.name;
            document.getElementById('car-location').textContent = data.location;
            document.getElementById('car-year').textContent = data.year;
            document.getElementById('car-fuel').textContent = data.fuel;
            document.getElementById('car-transmission').textContent = data.transmission;
            document.getElementById('car-km').textContent = data.km.toLocaleString() + ' km';
            document.getElementById('car-owner').textContent = data.owner;
            document.getElementById('car-price').textContent = '₹ ' + data.price + ' Lakhs';
        })
        .catch(err => console.error('Error loading random car:', err));
}

window.addEventListener('DOMContentLoaded', () => {
    loadRandomCar();
    setInterval(loadRandomCar, 5000); // ✅ updates every 5 seconds
});



// ========================
// Color Palette
// ========================
const colorPalettes = [
    "#4BC0C0", "#FF6384", "#36A2EB", "#FFCE56", "#9966FF",
    "#FF9F40", "#E74C3C", "#3498DB", "#2ECC71", "#F39C12"
];

// ========================
// Biggest Price Evolution per Year (Animated)
// ========================
function renderBiggestEvolutionChart() {
    fetch('http://127.0.0.1:8000/charts/biggest-price-evolution')
        .then(res => res.json())
        .then(data => {
            const canvas = document.getElementById('biggestEvolutionChart');
            if (!canvas) return;

            const allYears = [...new Set(
                data.flatMap(d => d.data.map(p => p.year))
            )].sort();

            const datasets = data.map((series, index) => ({
                label: series.label,
                data: allYears.map(year => {
                    const point = series.data.find(p => p.year === year);
                    return point ? point.avg_price : null;
                }),
                borderColor: colorPalettes[index % colorPalettes.length],
                backgroundColor: colorPalettes[index % colorPalettes.length] + '22',
                borderWidth: 2.5,
                tension: 0.4,
                spanGaps: true,
                pointRadius: 4,
                pointHoverRadius: 7,
                pointBackgroundColor: colorPalettes[index % colorPalettes.length],
                fill: false,
            }));

            new Chart(canvas, {
                type: 'line',
                data: { labels: allYears, datasets },
                options: {
                    responsive: true,
                    animation: {
                        duration: 2000,           // 2 second animation
                        easing: 'easeInOutQuart', // smooth easing
                        onProgress: function(animation) {
                            // draws a progress bar while animating
                            const ctx = canvas.getContext('2d');
                            const chart = animation.chart;
                            const progress = animation.currentStep / animation.numSteps;
                            ctx.save();
                            ctx.fillStyle = 'rgba(255,255,255,0.05)';
                            ctx.fillRect(0, chart.height - 4, chart.width * progress, 4);
                            ctx.restore();
                        }
                    },
                    interaction: {
                        mode: 'index',
                        intersect: false,
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: 'bottom',
                            labels: {
                                color: '#fff',
                                padding: 15,
                                font: { size: 11 }
                            }
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            backgroundColor: 'rgba(0,0,0,0.7)',
                            titleColor: '#fff',
                            bodyColor: '#ccc',
                            callbacks: {
                                afterBody: (items) => {
                                    const d = data[items[0]?.datasetIndex];
                                    if (d) return `📈 Biggest jump: ₹${d.evolution}L in ${d.year}`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            title: { display: true, text: 'Year', color: '#aaa' },
                            ticks: { color: '#aaa' },
                            grid: { color: 'rgba(255,255,255,0.05)' }
                        },
                        y: {
                            title: { display: true, text: 'Avg Price (Lakhs)', color: '#aaa' },
                            ticks: { color: '#aaa' },
                            grid: { color: 'rgba(255,255,255,0.05)' }
                        }
                    }
                }
            });
        })
        .catch(err => console.error('Error loading biggest evolution chart:', err));
}
window.addEventListener('DOMContentLoaded', () => {
    renderBiggestEvolutionChart();
});



    // ============================================
    // Initialize All Functions
    // ============================================
    function init() {
        initThemeToggle();
        initTiltEffect();
        initCounters();
        initMobileMenu();
        initFormValidation();
        initPasswordToggle();
        initPageTransitions();
        initSettingsTabs();
        fetchTotalCars();
        fetchFuelTypeCount();
        fetchBrandCount();
        fetchModelCount();
        renderBrandsPerModelChart();
        renderOwnerTypeChart();
        loadRandomCar();
        renderBiggestEvolutionChart();
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
