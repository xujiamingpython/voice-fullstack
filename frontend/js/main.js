/**
 * 前端入口：UI 绑定 + 事件流渲染 + 设置管理。
 */
import { ChatSocket } from "./ws.js";
import { Recorder } from "./recorder.js";

const WS_URL = `ws://${location.hostname}:8000/ws/chat?session_id=${localStorage.getItem("session_id") || "default"}`;

// ---------- 状态 ----------
const state = {
  socket: null,
  recorder: null,
  ttsEnabled: localStorage.getItem("tts_enabled") !== "false",
  provider: localStorage.getItem("llm_provider") || "aliyun",
  voice: localStorage.getItem("tts_voice") || "ailiao",
  audioQueue: [],
  isSpeaking: false,
};

// ---------- DOM ----------
const $ = (id) => document.getElementById(id);
const messageList = $("messageList");

// ---------- 事件处理器 ----------
const handlers = {
  onEvent(msg) {
    switch (msg.type) {
      case "asr_final":
        renderUserMessage(msg.text);
        break;
      case "llm_thinking":
        renderThinking();
        break;
      case "llm_chunk":
        appendStreamingText(msg.text);
        break;
      case "tool_calling":
        renderToolCard(msg.tool, msg.args, "running");
        break;
      case "tool_result":
        updateToolCard(msg.tool, msg.summary, "done");
        break;
      case "tts_audio":
        if (state.ttsEnabled) enqueueAudio(msg.data);
        break;
      case "tts_end":
        break;
      case "done":
        removeThinking();
        break;
      case "error":
        toast(msg.message || "出错了");
        removeThinking();
        break;
      case "interrupted":
        removeThinking();
        break;
    }
  },
  onAudio(blob) {
    // 二进制音频帧（备用路径）
    playBlob(blob);
  },
  onOpen() {
    console.log("[ws] connected");
  },
  onClose() {
    toast("连接已断开，正在重连…");
  },
  onError(e) {
    console.error("[ws] error", e);
  },
};

// ---------- 渲染 ----------
function renderUserMessage(text) {
  removeThinking();
  const div = document.createElement("div");
  div.className = "msg user";
  div.innerHTML = `<div class="bubble"></div>`;
  div.querySelector(".bubble").textContent = text;
  messageList.appendChild(div);
  scrollBottom();
}

function renderThinking() {
  removeThinking();
  const div = document.createElement("div");
  div.className = "msg ai";
  div.innerHTML = `
    <div class="avatar">灵</div>
    <div class="bubble">
      <div class="thinking-dots"><span></span><span></span><span></span></div>
    </div>`;
  messageList.appendChild(div);
  scrollBottom();
}

function appendStreamingText(text) {
  let bubble = document.querySelector(".msg.ai .bubble");
  if (!bubble) {
    renderThinking();
    bubble = document.querySelector(".msg.ai .bubble");
    bubble.innerHTML = "";
  }
  bubble.appendChild(document.createTextNode(text));
  scrollBottom();
}

function removeThinking() {
  const dots = document.querySelectorAll(".thinking-dots");
  dots.forEach((d) => d.closest(".msg").remove());
}

function renderToolCard(name, args, status) {
  const card = document.createElement("div");
  card.className = "tool-card";
  card.dataset.tool = name;
  card.innerHTML = `
    <div class="tool-card-header">
      <span class="dot ${status === "done" ? "done" : ""}"></span>
      <span>🛠️ ${name}</span>
      <button class="icon-btn" style="margin-left:auto;font-size:12px">▾</button>
    </div>
    <div class="tool-card-body">
      <pre>${JSON.stringify(args, null, 2)}</pre>
    </div>`;
  const lastAi = [...messageList.querySelectorAll(".msg.ai")].pop();
  (lastAi || messageList).appendChild(card);
  scrollBottom();
}

function updateToolCard(name, summary, status) {
  const card = document.querySelector(`.tool-card[data-tool="${name}"]`);
  if (!card) return;
  const dot = card.querySelector(".dot");
  dot.className = `dot ${status}`;
  const body = card.querySelector(".tool-card-body");
  const pre = body.querySelector("pre");
  pre.textContent = `✅ 结果: ${summary}`;
  card.querySelector(".icon-btn").addEventListener("click", () => {
    body.classList.toggle("open");
  });
  scrollBottom();
}

// ---------- 音频播放 ----------
function enqueueAudio(base64) {
  const bytes = Uint8Array.from(atob(base64), (c) => c.charCodeAt(0));
  const blob = new Blob([bytes], { type: "audio/mpeg" });
  playBlob(blob);
}

function playBlob(blob) {
  const url = URL.createObjectURL(blob);
  const audio = new Audio(url);
  audio.onended = () => URL.revokeObjectURL(url);
  audio.play().catch(() => {});
}

// ---------- 录音 ----------
async function startRecording() {
  try {
    await state.recorder.start();
    $("btnMic").classList.add("recording");
    $("btnMic").querySelector(".mic-hint").textContent = "聆听中…";
  } catch (e) {
    toast("无法使用麦克风，请检查浏览器权限");
  }
}

async function stopRecording() {
  $("btnMic").classList.remove("recording");
  $("btnMic").querySelector(".mic-hint").textContent = "按住说话";
  state.recorder.stop();
  state.socket.sendAudioEnd();
}

// ---------- 设置 ----------
function openSettings() {
  $("setProvider").value = state.provider;
  $("setTTS").checked = state.ttsEnabled;
  $("setVoice").value = state.voice;
  $("settingsOverlay").classList.remove("hidden");
}

function saveSettings() {
  state.provider = $("setProvider").value;
  state.ttsEnabled = $("setTTS").checked;
  state.voice = $("setVoice").value;
  localStorage.setItem("llm_provider", state.provider);
  localStorage.setItem("tts_enabled", state.ttsEnabled);
  localStorage.setItem("tts_voice", state.voice);
  $("modelBadge").textContent = state.provider === "aliyun" ? "qwen-plus" : "deepseek-chat";
  $("settingsOverlay").classList.add("hidden");
  toast("设置已保存");
}

// ---------- 工具函数 ----------
function scrollBottom() {
  messageList.scrollTop = messageList.scrollHeight;
}

function toast(text) {
  const el = $("toast");
  el.textContent = text;
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 2500);
}

function renderEmptyState() {
  messageList.innerHTML = `
    <div class="empty-state">
      <div class="emoji">🎙️</div>
      <h2>开启你的第一次对话</h2>
      <p>按住下方按钮说话，或直接输入文字</p>
      <div class="suggestions">
        <button class="suggestion-chip">今天北京天气怎么样？</button>
        <button class="suggestion-chip">附近 1 公里内有什么咖啡馆？</button>
        <button class="suggestion-chip">从国贸到大兴机场怎么走？</button>
      </div>
    </div>`;
  messageList.querySelectorAll(".suggestion-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      messageList.innerHTML = "";
      renderUserMessage(chip.textContent);
      state.socket.sendText(chip.textContent);
    });
  });
}

// ---------- 初始化 ----------
async function init() {
  renderEmptyState();
  $("modelBadge").textContent = state.provider === "aliyun" ? "qwen-plus" : "deepseek-chat";

  // 录音
  state.recorder = new Recorder(
    (b64) => state.socket.sendAudioChunk(b64, "webm"),
    () => {}
  );

  // WebSocket
  state.socket = new ChatSocket(WS_URL, handlers);
  state.socket.connect().catch(() => toast("无法连接后端服务，请确认后端已启动"));

  // 事件绑定
  const micBtn = $("btnMic");
  let pressTimer = null;
  micBtn.addEventListener("pointerdown", () => {
    pressTimer = setTimeout(() => startRecording(), 200);
  });
  micBtn.addEventListener("pointerup", () => {
    clearTimeout(pressTimer);
    if (state.recorder?.recording) stopRecording();
  });
  micBtn.addEventListener("pointerleave", () => {
    clearTimeout(pressTimer);
    if (state.recorder?.recording) stopRecording();
  });

  $("textInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      const text = e.target.value.trim();
      if (!text) return;
      e.target.value = "";
      messageList.innerHTML = "";
      renderUserMessage(text);
      state.socket.sendText(text);
    }
  });

  $("btnSettings").addEventListener("click", openSettings);
  $("btnCloseSettings").addEventListener("click", () => $("settingsOverlay").classList.add("hidden"));
  $("btnSaveSettings").addEventListener("click", saveSettings);
  $("btnResetSettings").addEventListener("click", () => {
    localStorage.clear();
    location.reload();
  });

  $("btnSidebar").addEventListener("click", () => $("sidebar").classList.toggle("open"));
  $("btnNewSession").addEventListener("click", () => {
    localStorage.removeItem("session_id");
    location.reload();
  });

  $("btnTheme").addEventListener("click", () => {
    const cur = document.documentElement.dataset.theme || "light";
    document.documentElement.dataset.theme = cur === "light" ? "dark" : "light";
    $("btnTheme").textContent = cur === "light" ? "☀️" : "🌙";
  });
}

document.addEventListener("DOMContentLoaded", init);
