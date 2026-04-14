"""
patterns.py — All chatbot rules for Nova.

Each rule has:
  priority   : lower = checked first
  patterns   : list of regex strings (case-insensitive)
  responses  : list of possible replies (one picked at random)

Special sentinel values in responses:
  __TIME__  → replaced with live server time
  __DATE__  → replaced with live server date
"""

import re

RULE_SET = [
    {
        "priority": 1,
        "patterns": [r"\b(hi|hello|hey|howdy|hiya|greetings|what'?s up|sup)\b"],
        "responses": [
            "Hey there! 👋 I'm Nova. What's on your mind?",
            "Hello! Great to see you here. How can I help today?",
            "Hi! I'm Nova — your rule-based assistant. Ask me anything!",
            "Hey! Nova here, ready to chat. What do you need?",
        ],
    },
    {
        "priority": 2,
        "patterns": [r"\b(what'?s? (is )?your name|who are you|introduce yourself|tell me about yourself)\b"],
        "responses": [
            "I'm Nova — a rule-based chatbot built with Python & Flask. No ML, just clean logic! 🤖",
            "The name's Nova. I run on if-else logic and regex patterns, not neural networks.",
        ],
    },
    {
        "priority": 3,
        "patterns": [r"\b(what can you do|your purpose|how do you work|what are you (for|capable of)|your (function|job|role))\b"],
        "responses": [
            "Here's what I can help with:\n• Greetings & small talk\n• Current time & date\n• Jokes & fun facts\n• Motivational quotes\n• And more — just ask!",
            "I'm a rule-based bot. Try asking me the time, a joke, or a fun fact!",
        ],
    },
    {
        "priority": 4,
        "patterns": [r"\b(help|assist|support|guide me|what do i (say|type|ask))\b"],
        "responses": [
            "Sure! Try these:\n→ 'Hello'\n→ 'What's your name?'\n→ 'What time is it?'\n→ 'Tell me a joke'\n→ 'Fun fact'\n→ 'Motivate me'\n→ 'How are you?'\n→ 'Bye'",
        ],
    },
    {
        "priority": 5,
        "patterns": [
            r"\b(what.?s? (is )?the (time|current time)|time (now|please|right now)|tell me the time)\b",
            r"\bwhat time is it\b",
        ],
        "responses": ["__TIME__"],
    },
    {
        "priority": 6,
        "patterns": [r"\b(what.?s? (is )?the (date|today s? date)|what day is (it|today)|today s? date|what is today)\b"],
        "responses": ["__DATE__"],
    },
    {
        "priority": 7,
        "patterns": [r"\b(how are you|how.?re you doing|you okay|how do you feel|are you (well|good|fine|okay))\b"],
        "responses": [
            "Doing great, thanks! 😊 Circuits are humming nicely. You?",
            "Running at full capacity! No bugs today (fingers crossed 🤞). How about you?",
            "Fantastic! Pattern matching is my cardio, and I've been very active. How can I help?",
        ],
    },
    {
        "priority": 8,
        "patterns": [r"\b(tell (me )?a joke|joke|make me laugh|say something funny|funny)\b"],
        "responses": [
            "Why don't scientists trust atoms? They make up everything! 😂",
            "I told my computer I needed a break… now it won't stop sending me Kit-Kat ads. 🍫",
            "Why did the programmer quit? They didn't get arrays. 🥁",
            "A SQL query walks into a bar and asks two tables: 'Can I join you?' 😄",
            "Why do Java devs wear glasses? They don't C#. 👓",
        ],
    },
    {
        "priority": 9,
        "patterns": [r"\b(fun fact|interesting fact|tell me something (interesting|cool|new)|did you know|fact)\b"],
        "responses": [
            "🧠 Honey never spoils — archaeologists found 3,000-year-old honey in Egyptian tombs, still edible!",
            "🐙 Octopuses have three hearts, blue blood, and can taste with their arms.",
            "💡 The first computer bug was an actual moth, found in a Harvard Mark II relay in 1947.",
            "🌍 There are more possible chess games than atoms in the observable universe.",
            "🦈 Sharks are older than trees — sharks: ~450M years old; trees: ~350M years old.",
        ],
    },
    {
        "priority": 10,
        "patterns": [r"(motivat\w+|inspire me|\bquote\b|keep going|encouragement|cheer me up)"],
        "responses": [
            "💪 'The secret of getting ahead is getting started.' — Mark Twain",
            "🔥 'Don't watch the clock; do what it does — keep going.' — Sam Levenson",
            "🚀 'You don't have to be great to start, but you have to start to be great.' — Zig Ziglar",
            "⭐ 'Believe you can and you're halfway there.' — Theodore Roosevelt",
        ],
    },
    {
        "priority": 11,
        "patterns": [r"\b(weather|temperature|rain|sunny|forecast|climate today)\b"],
        "responses": [
            "I can't fetch live weather — I'm rule-based with no internet access. Try weather.com! 🌤️",
        ],
    },
    {
        "priority": 12,
        "patterns": [r"\b(how old are you|your age|when were you (born|created|made)|your birthday)\b"],
        "responses": [
            "I was born the moment someone ran 'python app.py' for the first time. Ageless! ✨",
            "Age is a human concept. I'm as young as Flask and as old as if-else logic. 😄",
        ],
    },
    {
        "priority": 13,
        "patterns": [
            r"\b(i am (sad|unhappy|depressed|upset|stressed|anxious|worried|lonely))\b",
            r"\bfeeling (down|low|bad|terrible|awful)\b",
        ],
        "responses": [
            "I'm sorry to hear that. 💙 It's okay not to be okay. Things will improve.",
            "That sounds tough 😔. I hope you feel better soon. Talking to someone you trust can really help.",
        ],
    },
    {
        "priority": 14,
        "patterns": [
            r"\b(i am (happy|great|awesome|fantastic|good|excited|wonderful|amazing))\b",
            r"\bfeeling (good|great|amazing|wonderful|on top of the world)\b",
        ],
        "responses": [
            "That's wonderful! 🎉 Keep that energy going!",
            "Love that! 😄 Good vibes only — what else can I help with?",
        ],
    },
    {
        "priority": 15,
        "patterns": [r"\b(bye|goodbye|see you|later|take care|farewell|gotta go|ttyl|cya)\b"],
        "responses": [
            "Goodbye! It was great chatting. Come back anytime! 👋",
            "See you later! Take care and stay curious. 🌟",
            "Bye! Every great journey starts with a single question. 🚀",
        ],
    },
    {
        "priority": 16,
        "patterns": [r"\b(thank(s| you)|thx|ty|much appreciated|appreciate it)\b"],
        "responses": [
            "You're very welcome! 😊 Anything else I can help with?",
            "Happy to help! Ask me anything anytime.",
            "No problem at all! That's what I'm here for. 🤖",
        ],
    },
    {
        "priority": 17,
        "patterns": [r"\b(who (made|built|created|designed) you|your (creator|developer|author|maker))\b"],
        "responses": [
            "I was built with Python & Flask as a rule-based chatbot project. Clean code, zero ML! 🛠️",
            "A passionate coder brought me to life with Flask, regex, and a lot of coffee. ☕",
        ],
    },
    {
        "priority": 18,
        "patterns": [r"\b(stupid|dumb|idiot|useless|hate you|worst bot|terrible)\b"],
        "responses": [
            "Ouch! 😅 I know I have limits, but I'm doing my best with if-else & regex. Be kind! 💙",
            "A bit harsh, but fair — I'm not perfect. Type 'help' and I'll do my best. 🙏",
        ],
    },
]

FALLBACK_RESPONSES = [
    "Hmm, I'm not sure about that. Try 'help' to see what I can do!",
    "That one's beyond my rules. 🤔 Type 'help' for my capabilities.",
    "Interesting! But I'm rule-based with a fixed playbook. Try 'help'!",
    "I didn't quite catch that. Could you rephrase? Or type 'help'!",
]

# Pre-compile all patterns at import time for speed
def _compile(rule_set):
    compiled = []
    for rule in sorted(rule_set, key=lambda r: r["priority"]):
        compiled.append({
            "patterns": [re.compile(p, re.IGNORECASE) for p in rule["patterns"]],
            "responses": rule["responses"],
        })
    return compiled

COMPILED_RULES = _compile(RULE_SET)