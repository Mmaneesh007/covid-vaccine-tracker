import streamlit.components.v1 as components

def show_particle_background():
    """
    Injects the interactive particle background into the main Streamlit app.
    Uses window.parent to attach the canvas to the main document body,
    ensuring it covers the full screen and reacts to mouse movements globally.
    """
    js_code = """
    <script>
    (function() {
        // Access the parent document (main Streamlit app)
        const parentDoc = window.parent.document;
        const parentWindow = window.parent;
        
        // Check if canvas already exists to prevent duplicates on rerun
        if (parentDoc.getElementById('particle-canvas')) {
            return;
        }

        // Create Canvas
        const canvas = parentDoc.createElement('canvas');
        canvas.id = 'particle-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.zIndex = '-1'; // Behind everything
        canvas.style.pointerEvents = 'none'; // Let clicks pass through
        parentDoc.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        let DPR = Math.max(1, parentWindow.devicePixelRatio || 1);
        let W = parentWindow.innerWidth;
        let H = parentWindow.innerHeight;
        
        function resizeCanvas() {
            W = parentWindow.innerWidth;
            H = parentWindow.innerHeight;
            canvas.width = Math.floor(W * DPR);
            canvas.height = Math.floor(H * DPR);
            canvas.style.width = W + 'px';
            canvas.style.height = H + 'px';
            ctx.scale(DPR, DPR);
        }
        resizeCanvas();

        // Configuration
        const particleCount = 80;
        const speedFactor = 1.6;
        
        // Mouse state
        const mouse = {x: W/2, y: H/2, active: false};
        
        parentWindow.addEventListener('mousemove', (e) => { 
            mouse.x = e.clientX; 
            mouse.y = e.clientY; 
            mouse.active = true; 
        });
        
        parentWindow.addEventListener('touchmove', (e) => { 
            if(e.touches[0]){ 
                mouse.x = e.touches[0].clientX; 
                mouse.y = e.touches[0].clientY; 
                mouse.active = true; 
            } 
        }, {passive:true});
        
        parentWindow.addEventListener('mouseleave', () => mouse.active = false);
        parentWindow.addEventListener('resize', resizeCanvas);

        // Particle Class
        class Particle {
            constructor(x, y) {
                this.x = x; 
                this.y = y;
                this.vx = (Math.random()-0.5)*0.5; 
                this.vy = (Math.random()-0.5)*0.5;
                this.size = 0.3 + Math.random()*0.8;
                this.h = 210 + Math.random()*80; // Blue-Purple Hue (210-290)
            }
            
            update(dt) {
                // Flow field
                const nx = this.x * 0.006;
                const ny = this.y * 0.006;
                const t = performance.now() * 0.0005;
                const angle = (Math.sin(nx * 6 + t*1.0) + Math.cos(ny * 5 - t*0.9)) * Math.PI;

                const ax = Math.cos(angle) * 0.05 * speedFactor;
                const ay = Math.sin(angle) * 0.05 * speedFactor;

                // Mouse interaction
                if(mouse.active) {
                    const dx = this.x - mouse.x;
                    const dy = this.y - mouse.y;
                    const dist2 = dx*dx + dy*dy + 0.0001;
                    const dist = Math.sqrt(dist2);
                    const influence = Math.max(0, 1 - dist / 260);
                    const repulseStrength = 0.6 * influence * speedFactor;
                    this.vx += ax + (dx / dist) * repulseStrength * 0.2;
                    this.vy += ay + (dy / dist) * repulseStrength * 0.2;
                } else {
                    this.vx += ax; 
                    this.vy += ay;
                }

                // Damping
                this.vx *= 0.96; 
                this.vy *= 0.96;

                // Move
                this.x += this.vx * dt;
                this.y += this.vy * dt;

                // Wrap edges
                if(this.x < -10) this.x = W + 10;
                if(this.x > W + 10) this.x = -10;
                if(this.y < -10) this.y = H + 10;
                if(this.y > H + 10) this.y = -10;
            }
            
            draw(ctx) {
                const speed = Math.min(5, Math.hypot(this.vx, this.vy));
                const alpha = 0.01 + Math.min(0.02, speed * 0.01);
                ctx.beginPath();
                ctx.fillStyle = `hsla(${this.h}, 35%, 65%, ${alpha})`;
                ctx.ellipse(this.x, this.y, this.size, this.size*0.9, 0, 0, Math.PI*2);
                ctx.fill();
            }
        }

        // Initialize Particles
        let particles = [];
        for(let i=0; i<particleCount; i++) {
            particles.push(new Particle(Math.random()*W, Math.random()*H));
        }

        // Animation Loop
        let last = performance.now();
        function frame(now) {
            const dt = Math.min(1/10, (now - last) / 16.6667);
            last = now;

            // Trails effect
            ctx.fillStyle = 'rgba(255, 255, 255, 0.25)';
            ctx.fillRect(0, 0, W, H);

            // Dot grid
            drawDotGrid();

            // Update & Draw Particles
            for(let p of particles) {
                p.update(dt);
                p.draw(ctx);
            }
            
            requestAnimationFrame(frame);
        }

        // Dot Grid Helper
        const dotCanvas = parentDoc.createElement('canvas');
        const dctx = dotCanvas.getContext('2d');
        
        function drawDotGrid() {
            if(!dotCanvas.width || dotCanvas.width !== W || dotCanvas.height !== H) {
                dotCanvas.width = W; 
                dotCanvas.height = H;
                const s = 18;
                dctx.clearRect(0, 0, W, H);
                dctx.fillStyle = 'rgba(0, 0, 0, 0.03)';
                for(let y=0; y<H; y+=s) {
                    for(let x=0; x<W; x+=s) {
                        dctx.fillRect(x+1.5, y+1.5, 1.2, 1.2);
                    }
                }
            }
            ctx.drawImage(dotCanvas, 0, 0);
        }

        // Start
        requestAnimationFrame(frame);

    })();
    </script>
    """
    components.html(js_code, height=0, width=0)
