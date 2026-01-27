document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const mainContent = document.querySelector(".main-content");
  const isHidden = localStorage.getItem("sidebarHidden") === "true";

  if (isHidden) {
    sidebar.style.display = "none";
    mainContent.style.marginLeft = "0";
  }
});

function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  const mainContent = document.querySelector(".main-content");

  if (sidebar.style.display === "none") {
    sidebar.style.display = "block";
    mainContent.style.marginLeft = "220px";
    localStorage.setItem("sidebarHidden", "false");
  } else {
    sidebar.style.display = "none";
    mainContent.style.marginLeft = "0";
    localStorage.setItem("sidebarHidden", "true");
  }
}


// Capture Quill editor content and preserve alignments
function captureEditor() {
  const content = quill.root.innerHTML;

  // Create a temporary container to modify HTML
  const container = document.createElement("div");
  container.innerHTML = content;

  // Mapping Quill classes to inline alignment styles
  const alignMap = {
    "ql-align-center": "center",
    "ql-align-right": "right",
    "ql-align-justify": "justify"
  };

  // Loop through all elements and apply inline text-align styles
  container.querySelectorAll("*").forEach(el => {
    for (const cls in alignMap) {
      if (el.classList.contains(cls)) {
        el.style.textAlign = alignMap[cls];
        el.classList.remove(cls); // Optional: remove Quill class
      }
    }
  });

  // Set the modified HTML into hidden input
  document.getElementById("hidden-body").value = container.innerHTML;
  return true;
}
