/**
 * script.js — NovaMind Chatbot Frontend
 *
 * Responsibilities:
 *  - Render user & bot messages into the feed
 *  - POST to /chat and display the response
 *  - Show a typing indicator while waiting
 *  - Support Enter key, sidebar hint shortcuts, clear button
 *  - Add timestamps and randomised typing delay for realism
 */

"use strict";

// ── DOM References ──────────────────────────────────────────────────────────
const feed      = document.getElementById("messageFeed");
const inputEl   = document.getElementById("userInput");
const sendBtn   = document.getElementById("sendBtn");
const typingEl  = document.getElementById("typingIndicator");

// ── Config ──────────────────────────────────────────────────────────────────
const BOT_NAME  = "Nova";
const USER_NAME = "You";

// Typing delay range in ms — makes the bot feel more natural
const TYPING_DELAY_MIN = 600;
const TYPING_DELAY_MAX = 1600;

// ── Helpers ─────────────────────────────────────────────────────────────────

/** Returns current time formatted as HH:MM AM/PM */
function currentTimestamp() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

/** Scrolls the feed to the very bottom */
function scrollBottom() {
  feed.scrollTop = feed.scrollHeight;
}

/** Returns a random integer between min and max (inclusive) */
function randBetween(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/** Escapes HTML special chars to prevent XSS */
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ── Message Rendering ────────────────────────────────────────────────────────

/**
 * Appends a message bubble to the feed.
 *
 * @param {string} text    - The message content
 * @param {"user"|"bot"}   - Side of the chat
 */
function appendMessage(text, role) {
  const row = document.createElement("div");
  row.className = `msg-row ${role}`;

  // Sender label
  const sender = document.createElement("div");
  sender.className = "msg-sender";
  sender.textContent = role === "user" ? USER_NAME : BOT_NAME;

  // Bubble — note: we use innerText not innerHTML to keep it safe,
  // but we allow newlines to render as <br> for formatted bot replies
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  // Replace \n with actual newlines in the DOM
  bubble.textContent = text;

  // Timestamp
  const time = document.createElement("div");
  time.className = "msg-time";
  time.textContent = currentTimestamp();

  row.appendChild(sender);
  row.appendChild(bubble);
  row.appendChild(time);

  feed.appendChild(row);
  scrollBottom();
}

// ── Typing Indicator ─────────────────────────────────────────────────────────

function showTyping()  { typingEl.classList.add("visible"); scrollBottom(); }
function hideTyping()  { typingEl.classList.remove("visible"); }

// ── Core Send Logic ──────────────────────────────────────────────────────────

/**
 * Reads input, sends to /chat API, then displays the response.
 */
async function sendMessage() {
  const raw = inputEl.value.trim();
  if (!raw) return;

  // Clear input & disable while processing
  inputEl.value = "";
  inputEl.disabled = true;
  sendBtn.disabled = true;

  // Show user bubble immediately
  appendMessage(raw, "user");

  // Show typing indicator
  showTyping();

  // Randomised delay to simulate "thinking"
  const delay = randBetween(TYPING_DELAY_MIN, TYPING_DELAY_MAX);

  try {
    // Fetch response from Flask backend
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: raw }),
    });

    if (!response.ok) {
      throw new Error(`Server responded with status ${response.status}`);
    }

    const data = await response.json();

    // Wait for the simulated delay before showing the reply
    await new Promise(resolve => setTimeout(resolve, delay));

    hideTyping();
    appendMessage(data.reply || "…", "bot");

  } catch (err) {
    await new Promise(resolve => setTimeout(resolve, 500));
    hideTyping();
    appendMessage("⚠ Couldn't reach the server. Is Flask running?", "bot");
    console.error("Chat fetch error:", err);
  } finally {
    // Re-enable input
    inputEl.disabled = false;
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

// ── Sidebar Hint Shortcut ────────────────────────────────────────────────────

/**
 * Triggered by sidebar nav items — pre-fills and sends a canned message.
 * @param {string} text
 */
function sendHint(text) {
  inputEl.value = text;
  sendMessage();
}

// ── Clear Chat ───────────────────────────────────────────────────────────────

function clearChat() {
  // Remove all children except the intro is re-added
  while (feed.firstChild) feed.removeChild(feed.firstChild);
  showIntro();
}

// ── Keyboard Shortcut ────────────────────────────────────────────────────────

inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// ── Intro Message ────────────────────────────────────────────────────────────

/**
 * Displays the bot's welcome message on load / after clear.
 */
function showIntro() {
  // Small delay so the page feels settled before the bot speaks
  setTimeout(() => {
    appendMessage(
      `Hey! I'm ${BOT_NAME}, your rule-based assistant. ⬡\n\nI understand natural phrases — try asking:\n• "Tell me a joke"\n• "What time is it?"\n• "Give me a fun fact"\n• "Motivate me"\n\nType "help" for the full list!`,
      "bot"
    );
  }, 400);
}

// ── Init ─────────────────────────────────────────────────────────────────────

showIntro();
inputEl.focus();
