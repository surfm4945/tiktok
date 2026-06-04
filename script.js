const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
const urlInput = document.getElementById('video-url');
const processBtn = document.getElementById('download-btn');
const loader = document.getElementById('loader');
const resultArea = document.getElementById('result-area');
const previewPlayer = document.getElementById('preview-player');
const finalDownloadBtn = document.getElementById('final-download-btn');
const toast = document.getElementById('toast');

// Dark Mode Logic
function switchTheme(e) {
    if (e.target.checked) {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
    }    
}
toggleSwitch.addEventListener('change', switchTheme, false);

// Show Toast message
function showToast(message, type) {
    toast.textContent = message;
    toast.className = `toast slide-up ${type}`;
    toast.classList.remove('hidden');
    setTimeout(() => { toast.classList.add('hidden'); }, 5000);
}

// Handle Processing
processBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();
    if (!url) {
        showToast("Please enter a valid TikTok URL.", "error");
        return;
    }

    // UI State: Loading
    processBtn.disabled = true;
    loader.classList.remove('hidden');
    resultArea.classList.add('hidden');
    toast.classList.add('hidden');

    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong.");
        }

        // UI State: Success
        previewPlayer.src = data.file_url;
        finalDownloadBtn.href = data.file_url;
        resultArea.classList.remove('hidden');
        showToast("Video ready! You can preview or download it.", "success");

    } catch (error) {
        showToast(error.message, "error");
    } finally {
        processBtn.disabled = false;
        loader.classList.add('hidden');
    }
});