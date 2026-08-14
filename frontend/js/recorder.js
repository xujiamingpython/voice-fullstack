/**
 * 录音模块：基于浏览器 MediaRecorder（webm/opus）。
 * 支持长按录音 + 实时声波可视化。
 */
export class Recorder {
  constructor(onChunk, onStop) {
    this.onChunk = onChunk;  // (base64, format) => void
    this.onStop = onStop;    // () => void
    this.mediaRecorder = null;
    this.stream = null;
    this.recording = false;
    this.chunks = [];
    this.timer = null;
    this.startTime = 0;
  }

  async ensurePermission() {
    if (this.stream) return this.stream;
    this.stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
      },
    });
    return this.stream;
  }

  async start() {
    const stream = await this.ensurePermission();
    this.chunks = [];
    this.recording = true;
    this.startTime = Date.now();

    this.mediaRecorder = new MediaRecorder(stream, {
      mimeType: this._pickMimeType(),
    });

    this.mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        this.chunks.push(e.data);
        this._emitChunk(e.data);
      }
    };

    this.mediaRecorder.onstop = () => {
      this.recording = false;
      this.onStop?.();
    };

    this.mediaRecorder.start(500); // 每 500ms 切一片，边录边传
  }

  stop() {
    if (this.mediaRecorder && this.mediaRecorder.state !== "inactive") {
      this.mediaRecorder.stop();
    }
  }

  async getBlob() {
    const type = this.mediaRecorder?.mimeType || "audio/webm";
    return new Blob(this.chunks, { type });
  }

  getDuration() {
    return (Date.now() - this.startTime) / 1000;
  }

  _pickMimeType() {
    const candidates = [
      "audio/webm;codecs=opus",
      "audio/webm",
      "audio/mp4",
      "audio/ogg;codecs=opus",
    ];
    for (const c of candidates) {
      if (MediaRecorder.isTypeSupported(c)) return c;
    }
    return "";
  }

  async _emitChunk(blob) {
    const buf = await blob.arrayBuffer();
    const b64 = this._bufToBase64(new Uint8Array(buf));
    this.onChunk?.(b64, "webm");
  }

  _bufToBase64(u8) {
    let bin = "";
    for (let i = 0; i < u8.length; i++) bin += String.fromCharCode(u8[i]);
    return btoa(bin);
  }

  /** 声波可视化：返回 analyzer（可选，骨架） */
  static async createAnalyzer(stream) {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const src = ctx.createMediaStreamSource(stream);
    const analyser = ctx.createAnalyser();
    analyser.fftSize = 128;
    src.connect(analyser);
    return analyser;
  }
}
