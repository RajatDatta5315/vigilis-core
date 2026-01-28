// VIGILIS NEURAL UNIVERSE ENGINE
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.domElement.style.position = 'fixed';
renderer.domElement.style.top = '0';
renderer.domElement.style.left = '0';
renderer.domElement.style.zIndex = '-1'; // Sabke peeche
document.body.appendChild(renderer.domElement);

// Create Particles
const geometry = new THREE.BufferGeometry();
const count = 2000;
const posArray = new Float32Array(count * 3);

for(let i = 0; i < count * 3; i++) {
    posArray[i] = (Math.random() - 0.5) * 15; // Spread
}

geometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
const material = new THREE.PointsMaterial({
    size: 0.005,
    color: 0x00ff41, // Neon Green
    transparent: true,
    opacity: 0.8,
});

const particlesMesh = new THREE.Points(geometry, material);
scene.add(particlesMesh);

camera.position.z = 2;

// Mouse Interaction
let mouseX = 0;
let mouseY = 0;
document.addEventListener('mousemove', (event) => {
    mouseX = event.clientX / window.innerWidth - 0.5;
    mouseY = event.clientY / window.innerHeight - 0.5;
});

const animate = () => {
    requestAnimationFrame(animate);
    
    // Rotation
    particlesMesh.rotation.y += 0.001;
    particlesMesh.rotation.x += 0.001;

    // Mouse Parallax
    particlesMesh.rotation.y += mouseX * 0.05;
    particlesMesh.rotation.x += mouseY * 0.05;

    renderer.render(scene, camera);
};

animate();

// Resize Fix
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
