"use client";

import { useRef, useState } from "react";

const ACCEPTED_TYPES = ["video/mp4", "video/quicktime", "video/webm"];
const MAX_FILE_SIZE_BYTES = 2 * 1024 * 1024 * 1024; // 2 GB

function formatFileSize(bytes: number): string {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
}

type VideoDropzoneProps = {
  onFileSelected: (file: File | null) => void;
};

export default function VideoDropzone({ onFileSelected }: VideoDropzoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);

  function acceptFile(candidate: File | undefined) {
    if (!candidate) return;

    if (!ACCEPTED_TYPES.includes(candidate.type)) {
      setError("Unsupported format. Please use MP4, MOV, or WebM.");
      setFile(null);
      onFileSelected(null);
      return;
    }

    if (candidate.size > MAX_FILE_SIZE_BYTES) {
      setError("File is too large. The maximum size is 2 GB.");
      setFile(null);
      onFileSelected(null);
      return;
    }

    setError(null);
    setFile(candidate);
    onFileSelected(candidate);
  }

  function handleDrop(event: React.DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setIsDragging(false);
    acceptFile(event.dataTransfer.files[0]);
  }

  return (
    <div className="flex flex-col gap-3">
      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`cursor-pointer rounded-xl border-2 border-dashed p-8 text-center transition-colors ${
          isDragging
            ? "border-purple-500 bg-purple-950/30"
            : "border-neutral-700 hover:border-neutral-500"
        }`}
      >
        <p className="font-medium text-white">Drag and drop a video here</p>
        <p className="mt-1 text-sm text-neutral-400">or click to choose a file (MP4, MOV, WebM)</p>
        <input
          ref={inputRef}
          type="file"
          accept="video/mp4,video/quicktime,video/webm"
          className="hidden"
          onChange={(e) => acceptFile(e.target.files?.[0])}
        />
      </div>

      {error && <p className="text-sm text-red-400">{error}</p>}

      {file && (
        <div className="rounded-lg border border-neutral-700 bg-neutral-900 px-3 py-2 text-sm">
          <span className="text-white">{file.name}</span>
          <span className="ml-2 text-neutral-400">{formatFileSize(file.size)}</span>
        </div>
      )}
    </div>
  );
}