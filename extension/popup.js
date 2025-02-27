document.getElementById('evaluateBtn').addEventListener('click', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (tab.url && tab.url.includes("youtube.com/watch")) {
    const videoId = getVideoIdFromUrl(tab.url);
    document.getElementById('output').innerText = "Evaluating content, please wait...";
    
    try {
      const response = await fetch('http://127.0.0.1:3000/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ videoId })
      });
      const data = await response.json();
      document.getElementById('output').innerText = formatEvaluation(data.evaluation);
    } catch (error) {
      document.getElementById('output').innerText = "Error during evaluation.";
      console.error(error);
    }
  } else {
    document.getElementById('output').innerText = "Not a YouTube video page.";
  }
});

function getVideoIdFromUrl(url) {
  const urlObj = new URL(url);
  return urlObj.searchParams.get("v");
}

function formatEvaluation(evaluationText) {
  return evaluationText.split('\n').map(line => line.trim()).join('\n\n');
}

// Draggable resize functionality
const resizeHandle = document.getElementById("resize-handle");
const container = document.querySelector(".container");

resizeHandle.addEventListener("mousedown", (event) => {
  event.preventDefault();
  document.addEventListener("mousemove", resize);
  document.addEventListener("mouseup", stopResize);
});

function resize(event) {
  container.style.width = event.clientX - container.offsetLeft + "px";
  container.style.height = event.clientY - container.offsetTop + "px";
}

function stopResize() {
  document.removeEventListener("mousemove", resize);
  document.removeEventListener("mouseup", stopResize);
}
