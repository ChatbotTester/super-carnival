<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fun Car Crash Game!</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Arial', sans-serif;
        }
        
        #gameContainer {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        canvas {
            border: 4px solid #fff;
            border-radius: 10px;
            background: #87CEEB;
            display: block;
            margin: 0 auto;
        }
        
        #score {
            color: white;
            font-size: 24px;
            margin: 10px 0;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        #instructions {
            color: white;
            font-size: 18px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        button {
            background: #ff6b6b;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 18px;
            border-radius: 25px;
            cursor: pointer;
            margin: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: scale(1.05);
        }
        
        button:active {
            transform: scale(0.95);
        }
    </style>
</head>
<body>
    <div id="gameContainer">
        <h1 style="color: white; text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);">🚗 Car Crash Fun! 🚗</h1>
        <div id="instructions">Use Arrow Keys to Move!</div>
        <div id="score">Score: 0</div>
        <canvas id="gameCanvas" width="800" height="500"></canvas>
        <br>
        <button onclick="resetGame()">New Game</button>
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        let score = 0;
        let particles = [];
        let cars = [];
        let powerUps = [];
        
        // Player car
        const player = {
            x: 100,
            y: 250,
            width: 60,
            height: 30,
            speed: 0,
            angle: 0,
            color: '#ff6b6b',
            crashed: false,
            crashCooldown: 0
        };
        
        // Car colors for variety
        const carColors = ['#4ecdc4', '#f7dc6f', '#bb8fce', '#85c1e9', '#f8b500'];
        
        // Keyboard state
        const keys = {};
        
        // Initialize game
        function init() {
            // Create some AI cars
            for (let i = 0; i < 5; i++) {
                cars.push(createCar());
            }
            
            // Create power-ups
            for (let i = 0; i < 3; i++) {
                powerUps.push(createPowerUp());
            }
        }
        
        function createCar() {
            return {
                x: Math.random() * (canvas.width - 60) + 30,
                y: Math.random() * (canvas.height - 30) + 15,
                width: 60,
                height: 30,
                speed: Math.random() * 2 + 1,
                angle: Math.random() * Math.PI * 2,
                color: carColors[Math.floor(Math.random() * carColors.length)],
                spinning: false,
                spinSpeed: 0
            };
        }
        
        function createPowerUp() {
            return {
                x: Math.random() * (canvas.width - 40) + 20,
                y: Math.random() * (canvas.height - 40) + 20,
                size: 20,
                type: Math.random() > 0.5 ? 'star' : 'boost',
                collected: false
            };
        }
        
        function createParticle(x, y, color) {
            return {
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 10,
                vy: (Math.random() - 0.5) * 10,
                size: Math.random() * 5 + 2,
                color: color,
                life: 1
            };
        }
        
        function drawCar(car) {
            ctx.save();
            ctx.translate(car.x, car.y);
            ctx.rotate(car.angle);
            
            // Car body
            ctx.fillStyle = car.color;
            ctx.fillRect(-car.width/2, -car.height/2, car.width, car.height);
            
            // Windows
            ctx.fillStyle = '#333';
            ctx.fillRect(-car.width/2 + 10, -car.height/2 + 5, 20, car.height - 10);
            
            // Wheels
            ctx.fillStyle = '#000';
            ctx.fillRect(-car.width/2 + 5, -car.height/2 - 5, 10, 8);
            ctx.fillRect(-car.width/2 + 5, car.height/2 - 3, 10, 8);
            ctx.fillRect(car.width/2 - 15, -car.height/2 - 5, 10, 8);
            ctx.fillRect(car.width/2 - 15, car.height/2 - 3, 10, 8);
            
            ctx.restore();
        }
        
        function drawPowerUp(powerUp) {
            if (powerUp.collected) return;
            
            ctx.save();
            ctx.translate(powerUp.x, powerUp.y);
            
            if (powerUp.type === 'star') {
                // Draw star
                ctx.fillStyle = '#ffd700';
                ctx.beginPath();
                for (let i = 0; i < 5; i++) {
                    const angle = (i * 2 * Math.PI / 5) - Math.PI / 2;
                    const x = Math.cos(angle) * powerUp.size;
                    const y = Math.sin(angle) * powerUp.size;
                    if (i === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                    
                    const innerAngle = angle + Math.PI / 5;
                    const innerX = Math.cos(innerAngle) * (powerUp.size / 2);
                    const innerY = Math.sin(innerAngle) * (powerUp.size / 2);
                    ctx.lineTo(innerX, innerY);
                }
                ctx.closePath();
                ctx.fill();
            } else {
                // Draw boost arrow
                ctx.fillStyle = '#00ff00';
                ctx.beginPath();
                ctx.moveTo(0, -powerUp.size);
                ctx.lineTo(-powerUp.size/2, powerUp.size/2);
                ctx.lineTo(0, 0);
                ctx.lineTo(powerUp.size/2, powerUp.size/2);
                ctx.closePath();
                ctx.fill();
            }
            
            ctx.restore();
        }
        
        function update() {
            // Update player
            if (!player.crashed) {
                if (keys['ArrowUp']) player.speed = Math.min(player.speed + 0.3, 8);
                if (keys['ArrowDown']) player.speed = Math.max(player.speed - 0.3, -3);
                if (keys['ArrowLeft']) player.angle -= 0.1;
                if (keys['ArrowRight']) player.angle += 0.1;
            }
            
            // Apply friction
            player.speed *= 0.95;
            
            // Update player position
            player.x += Math.cos(player.angle) * player.speed;
            player.y += Math.sin(player.angle) * player.speed;
            
            // Keep player in bounds
            player.x = Math.max(30, Math.min(canvas.width - 30, player.x));
            player.y = Math.max(15, Math.min(canvas.height - 15, player.y));
            
            // Update crash cooldown
            if (player.crashCooldown > 0) {
                player.crashCooldown--;
                player.crashed = false;
            }
            
            // Update AI cars
            cars.forEach(car => {
                if (!car.spinning) {
                    car.x += Math.cos(car.angle) * car.speed;
                    car.y += Math.sin(car.angle) * car.speed;
                    
                    // Bounce off walls
                    if (car.x < 30 || car.x > canvas.width - 30) {
                        car.angle = Math.PI - car.angle;
                        car.x = Math.max(30, Math.min(canvas.width - 30, car.x));
                    }
                    if (car.y < 15 || car.y > canvas.height - 15) {
                        car.angle = -car.angle;
                        car.y = Math.max(15, Math.min(canvas.height - 15, car.y));
                    }
                    
                    // Random direction change
                    if (Math.random() < 0.02) {
                        car.angle += (Math.random() - 0.5) * 0.5;
                    }
                } else {
                    // Spinning from crash
                    car.angle += car.spinSpeed;
                    car.spinSpeed *= 0.95;
                    if (Math.abs(car.spinSpeed) < 0.01) {
                        car.spinning = false;
                    }
                }
            });
            
            // Check collisions with AI cars
            cars.forEach(car => {
                if (checkCollision(player, car) && player.crashCooldown === 0) {
                    // Create crash effect
                    for (let i = 0; i < 20; i++) {
                        particles.push(createParticle(
                            (player.x + car.x) / 2,
                            (player.y + car.y) / 2,
                            i % 2 === 0 ? player.color : car.color
                        ));
                    }
                    
                    // Bounce cars apart
                    const dx = player.x - car.x;
                    const dy = player.y - car.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    
                    player.speed = -player.speed * 0.5 + 3;
                    player.angle = Math.atan2(dy, dx);
                    
                    car.spinning = true;
                    car.spinSpeed = (Math.random() - 0.5) * 0.5;
                    car.speed *= -0.5;
                    
                    score += 100;
                    player.crashCooldown = 30;
                    
                    updateScore();
                }
            });
            
            // Check power-up collection
            powerUps.forEach(powerUp => {
                if (!powerUp.collected && checkPowerUpCollision(player, powerUp)) {
                    powerUp.collected = true;
                    
                    if (powerUp.type === 'star') {
                        score += 50;
                        // Create sparkle effect
                        for (let i = 0; i < 10; i++) {
                            particles.push(createParticle(powerUp.x, powerUp.y, '#ffd700'));
                        }
                    } else {
                        // Boost
                        player.speed = 10;
                        for (let i = 0; i < 5; i++) {
                            particles.push(createParticle(player.x, player.y, '#00ff00'));
                        }
                    }
                    
                    updateScore();
                    
                    // Respawn power-up after delay
                    setTimeout(() => {
                        powerUp.x = Math.random() * (canvas.width - 40) + 20;
                        powerUp.y = Math.random() * (canvas.height - 40) + 20;
                        powerUp.collected = false;
                    }, 3000);
                }
            });
            
            // Update particles
            particles = particles.filter(particle => {
                particle.x += particle.vx;
                particle.y += particle.vy;
                particle.vy += 0.3; // Gravity
                particle.life -= 0.02;
                particle.size *= 0.98;
                return particle.life > 0;
            });
        }
        
        function checkCollision(car1, car2) {
            const dx = car1.x - car2.x;
            const dy = car1.y - car2.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            return distance < (car1.width + car2.width) / 2;
        }
        
        function checkPowerUpCollision(car, powerUp) {
            const dx = car.x - powerUp.x;
            const dy = car.y - powerUp.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            return distance < car.width/2 + powerUp.size;
        }
        
        function draw() {
            // Clear canvas with road effect
            ctx.fillStyle = '#87CEEB';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw road
            ctx.fillStyle = '#555';
            ctx.fillRect(0, 100, canvas.width, 300);
            
            // Draw road lines
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 3;
            ctx.setLineDash([20, 10]);
            ctx.beginPath();
            ctx.moveTo(0, 250);
            ctx.lineTo(canvas.width, 250);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // Draw grass
            ctx.fillStyle = '#90EE90';
            ctx.fillRect(0, 0, canvas.width, 100);
            ctx.fillRect(0, 400, canvas.width, 100);
            
            // Draw power-ups
            powerUps.forEach(drawPowerUp);
            
            // Draw cars
            cars.forEach(drawCar);
            drawCar(player);
            
            // Draw particles
            particles.forEach(particle => {
                ctx.fillStyle = particle.color;
                ctx.globalAlpha = particle.life;
                ctx.beginPath();
                ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                ctx.fill();
            });
            ctx.globalAlpha = 1;
        }
        
        function gameLoop() {
            update();
            draw();
            requestAnimationFrame(gameLoop);
        }
        
        function updateScore() {
            document.getElementById('score').textContent = `Score: ${score}`;
        }
        
        function resetGame() {
            score = 0;
            updateScore();
            player.x = 100;
            player.y = 250;
            player.speed = 0;
            player.angle = 0;
            player.crashed = false;
            player.crashCooldown = 0;
            particles = [];
            cars = [];
            powerUps = [];
            init();
        }
        
        // Keyboard controls
        window.addEventListener('keydown', (e) => {
            keys[e.key] = true;
            e.preventDefault();
        });
        
        window.addEventListener('keyup', (e) => {
            keys[e.key] = false;
            e.preventDefault();
        });
        
        // Start game
        init();
        gameLoop();
    </script>
</body>
</html>