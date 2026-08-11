let records = window.BODYFACE_RECORDS || []; // Loaded locally without fetch

let currentBody = new Image();
let currentFace = new Image();
let scale = 8;
let currentMode = 0; // The active mode for the main preview
let animationFrameId = null;

// State for animation
let animState = 'idle'; // idle, walk, sit, cheer, sleep
let direction = 0; // 0: down, 1: left, 2: right, 3: up
let frameIndex = 0;
let lastTick = 0;

// Animation definitions based on the 42 modes table and C# logic
// Direction is now raw 0, 1, 2, 3
// Math Formula for basic movement: Mode = (Direction * 4) + State

// Special states that don't follow the *4 rule
const SPECIAL_ANIMATIONS = {
    typing: {
        0: [{mode: 18}, {mode: 19}], // SW
        1: [{mode: 20}, {mode: 21}], // SE
        2: [{mode: 25}, {mode: 26}], // NW
        3: [{mode: 16}, {mode: 17}]  // NE
    },
    meeting: {
        0: [{mode: 18}], // SW
        1: [{mode: 22}], // SE
        2: [{mode: 27}], // NW
        3: [{mode: 16}]  // NE
    },
    cheer: {
        0: [{mode: 19}], // SW
        1: [{mode: 24, flipX: true}], // SE
        2: [{mode: 24}], // NW
        3: [{mode: 19}]  // NE
    },
    exhausted: {
        0: [{mode: 29}], // SW
        1: [{mode: 29}], // SE
        2: [{mode: 29, flipX: true}], // NW
        3: [{mode: 29}]  // NE
    }
};
function init() {
    if (!records || records.length === 0) {
        alert("Failed to load BODYFACE_RECORDS. Ensure bodyface_records.js is included.");
        return;
    }

    // Populate Selects
    const bodySelect = document.getElementById('bodySelect');
    for (let i = 0; i <= 25; i++) {
        const opt = document.createElement('option');
        opt.value = `body${i}.png`;
        opt.textContent = `body${i}.png`;
        if(i===19) opt.selected = true;
        bodySelect.appendChild(opt);
    }

    const faceSelect = document.getElementById('faceSelect');
    for (let i = 0; i <= 35; i++) {
        const opt = document.createElement('option');
        opt.value = `face_${i}.png`;
        opt.textContent = `face_${i}.png`;
        if(i===30) opt.selected = true;
        faceSelect.appendChild(opt);
    }

    // Event Listeners
    bodySelect.addEventListener('change', loadAssets);
    faceSelect.addEventListener('change', loadAssets);
    
    document.getElementById('scaleRange').addEventListener('input', (e) => {
        scale = parseInt(e.target.value);
        document.getElementById('scaleValue').textContent = `${scale}x`;
        updateMainCanvas();
    });

    // Playback controls
    document.querySelectorAll('.playback-controls .btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.playback-controls .btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            animState = e.target.id.replace('btn', '').toLowerCase();
            frameIndex = 0;
        });
    });

    // Direction controls
    document.querySelectorAll('.dir-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.dir-btn').forEach(b => b.classList.remove('active'));
            e.currentTarget.classList.add('active');
            direction = parseInt(e.currentTarget.dataset.dir);
        });
    });

    // Initial load
    loadAssets();
    requestAnimationFrame(animationLoop);
}

function loadAssets() {
    const bodyName = document.getElementById('bodySelect').value;
    const faceName = document.getElementById('faceSelect').value;

    let loaded = 0;
    const checkReady = () => {
        loaded++;
        if (loaded === 2) {
            renderContactSheet();
            updateMainCanvas();
        }
    };

    currentBody.onload = checkReady;
    currentFace.onload = checkReady;

    currentBody.src = `assets/characters/${bodyName}`;
    currentFace.src = `assets/characters/${faceName}`;
}

// Draw a single mode to a given context
function drawMode(ctx, modeData, customScale = 1) {
    if (!records || records.length === 0) return;
    
    const modeIndex = typeof modeData === 'object' ? modeData.mode : modeData;
    const bobY = typeof modeData === 'object' ? (modeData.bobY || 0) : 0;
    
    const rec = records[modeIndex];
    if (!rec) return;

    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    // Kairosoft Native Frame is 36x38. Base X offset for drawing is 8.
    const baseX = 8;
    
    // Disable smoothing
    ctx.imageSmoothingEnabled = false;

    ctx.save();
    
    // Viewer-side manual flipX support for specific special modes (e.g. cheer SE)
    const flipX = typeof modeData === 'object' ? (modeData.flipX || false) : false;
    if (flipX) {
        ctx.translate(36 * customScale, 0);
        ctx.scale(-1, 1);
    }

    // Draw Body based PURELY on JSON, no artificial viewer mirroring!
    ctx.drawImage(
        currentBody,
        rec.body_src_x, rec.body_src_y, rec.body_width, rec.body_height,
        (baseX + rec.body_dst_x) * customScale, rec.body_dst_y * customScale,
        rec.body_width * customScale, rec.body_height * customScale
    );

    // Draw Face based PURELY on JSON
    ctx.drawImage(
        currentFace,
        rec.face_src_x, rec.face_src_y, rec.face_width, rec.face_height,
        (baseX + rec.face_dst_x) * customScale, (rec.face_dst_y + bobY) * customScale,
        rec.face_width * customScale, rec.face_height * customScale
    );
    
    ctx.restore();
    
    if (customScale === scale) {
        document.getElementById('debug-mode').textContent = modeIndex.toString().padStart(2, '0');
        document.getElementById('debug-face').textContent = rec.face_src_x;
        document.getElementById('debug-body').textContent = `${rec.body_src_x}, ${rec.body_src_y}`;
    }
}

function updateMainCanvas() {
    const canvas = document.getElementById('previewCanvas');
    const ctx = canvas.getContext('2d');
    
    // Native frame size is 36x38
    canvas.width = 36 * scale;
    canvas.height = 38 * scale;
    
    drawMode(ctx, currentMode, scale);
}

function renderContactSheet() {
    const container = document.getElementById('contactSheet');
    container.innerHTML = '';

    for (let i = 0; i < records.length; i++) {
        const item = document.createElement('div');
        item.className = 'sheet-item';
        item.onclick = () => {
            currentMode = i;
            // Temporarily stop automatic animation if they click a static mode
            document.querySelectorAll('.playback-controls .btn').forEach(b => b.classList.remove('active'));
            animState = 'manual';
            updateMainCanvas();
        };

        const canvas = document.createElement('canvas');
        canvas.width = 36 * 2; // 2x scale for contact sheet
        canvas.height = 38 * 2;
        const ctx = canvas.getContext('2d');
        
        drawMode(ctx, i, 2);

        const label = document.createElement('div');
        label.className = 'sheet-label';
        label.textContent = `Mode ${i.toString().padStart(2, '0')}`;

        item.appendChild(canvas);
        item.appendChild(label);
        container.appendChild(item);
    }
}

function animationLoop(timestamp) {
    if (!lastTick) lastTick = timestamp;
    
    if (timestamp - lastTick > 250) {
        lastTick = timestamp;
        
        if (animState !== 'manual') {
            if (animState === 'idle' || animState === 'walk' || animState === 'desk') {
                let stateOffset = 0;
                let bobY = 0;
                let currentFormula = '';
                
                if (animState === 'idle') {
                    const frames = [0, 0, 0, 0];
                    const bobs = [0, 0, 1, 0];
                    frameIndex = (frameIndex + 1) % 4;
                    stateOffset = frames[frameIndex];
                    bobY = bobs[frameIndex];
                    currentFormula = `(${direction} * 4) + ${stateOffset} (Bob Y: ${bobY})`;
                } else if (animState === 'walk') {
                    const frames = [0, 2, 0, 3];
                    frameIndex = (frameIndex + 1) % 4;
                    stateOffset = frames[frameIndex];
                    currentFormula = `(${direction} * 4) + ${stateOffset}`;
                } else if (animState === 'desk') {
                    stateOffset = 1;
                    currentFormula = `(${direction} * 4) + ${stateOffset}`;
                }
                
                currentMode = {
                    mode: (direction * 4) + stateOffset,
                    bobY: bobY
                };
                
                document.getElementById('debug-formula').textContent = currentFormula;
            } else if (SPECIAL_ANIMATIONS[animState]) {
                const frames = SPECIAL_ANIMATIONS[animState][direction];
                if (frames) {
                    frameIndex = (frameIndex + 1) % frames.length;
                    currentMode = frames[frameIndex];
                    document.getElementById('debug-formula').textContent = `Special State Mapping`;
                }
            }
            
            updateMainCanvas();
        }
    }
    
    requestAnimationFrame(animationLoop);
}

// Start
init();
