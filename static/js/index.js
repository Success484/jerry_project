fetch("https://api.ipify.org?format=json")
  .then((response) => response.json())
  .then((data) => {
    const ip = data.ip;
    document.getElementById("ip-address").textContent = ip;

    // Fetch additional info, such as country code, using ipapi.co
    return fetch(`https://ipapi.co/${ip}/json/`);
  })
  .then((response) => response.json())
  .then((data) => {
    if (data.country_code) {
      // Set the country flag using the country code
      const flagUrl = `https://flagcdn.com/w40/${data.country_code.toLowerCase()}.png`;
      document.getElementById("country-flag").src = flagUrl;
      document.getElementById("country-flag").alt = data.country_name;
    } else {
      document.getElementById("country-flag").alt = "Country flag unavailable";
    }
  })
  .catch((error) => {
    console.error("Error fetching country details:", error);
    document.getElementById("ip-address").textContent = "Unable to retrieve IP";
  });

// Select elements
const chatIcon = document.getElementById("chat-icon");
const chatSection = document.getElementById("chat-section");
const closeChat = document.getElementById("close-chat");

// Show chat section when the chat icon is clicked
chatIcon.addEventListener("click", () => {
  if (chatSection.style.display === "flex") {
    chatSection.style.display = "none";
  } else {
    chatSection.style.display = "flex";
  }
});


document.addEventListener("DOMContentLoaded", () => {
  const toggleButton = document.getElementById("toggle-sidebar");
  const sidebar = document.getElementById("side-full-section");

  if (toggleButton) {
    toggleButton.addEventListener("click", () => {
      if (sidebar.style.display === "none" || sidebar.style.display === "") {
        sidebar.style.display = "block";
      } else {
        sidebar.style.display = "none";
      }
    });
  } else {
    console.error("Toggle button not found");
  }
});

// Show the loading modal
