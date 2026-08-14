/**
 * WebSocket 客户端：承载整段对话事件流。
 * 事件 → 回调映射见 index.html / main.js 中的 handler。
 */
export class ChatSocket {
  constructor(url, handlers = {}) {
    this.url = url;
    this.handlers = handlers;
    this.ws = null;
    this.connected = false;
    this.reconnectTimer = null;
    this.pendingChunks = []; // 断线时缓存的音频
  }

  connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.connected = true;
        this.handlers.onOpen?.();
        resolve();
      };

      this.ws.onmessage = (ev) => {
        // 二进制帧 = TTS 音频
        if (ev.data instanceof Blob) {
          this.handlers.onAudio?.(ev.data);
          return;
        }
        try {
          const msg = JSON.parse(ev.data);
          this.handlers.onEvent?.(msg);
        } catch {
          /* 忽略非 JSON 消息 */
        }
      };

      this.ws.onclose = () => {
        this.connected = false;
        this.handlers.onClose?.();
        this._scheduleReconnect();
      };

      this.ws.onerror = (e) => {
        this.handlers.onError?.(e);
      };
    });
  }

  _scheduleReconnect() {
    if (this.reconnectTimer) return;
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.connect().catch(() => {});
    }, 3000);
  }

  sendText(text) {
    this._send({ type: "text", content: text });
  }

  sendAudioChunk(base64, format = "webm") {
    this._send({ type: "audio_chunk", data: base64, format });
  }

  sendAudioEnd() {
    this._send({ type: "audio_end" });
  }

  interrupt() {
    this._send({ type: "interrupt" });
  }

  _send(obj) {
    if (!this.connected) return;
    this.ws.send(JSON.stringify(obj));
  }

  close() {
    this.connected = false;
    this.ws?.close();
  }
}
