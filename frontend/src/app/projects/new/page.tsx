"use client";

import { useState } from "react";
import VideoDropzone from "@/components/upload/VideoDropzone";
import {
  validateUpload,
  type ValidationResult,
} from "@/services/uploadService";

const categories = ["Gaming", "Podcasts", "Cricket", "Other Sports", "Other"];

export default function NewProjectPage() {
  const [name, setName] = useState("");
  const [category, setCategory] = useState(categories[0]);
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<ValidationResult | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!videoFile) {
      setResult({ valid: false, reason: "Please choose a video first." });
      return;
    }

    setIsSubmitting(true);
    setResult(null);
    try {
      const response = await validateUpload(videoFile);
      setResult(response);
      console.log("New project:", {
        name,
        category,
        file: videoFile.name,
        response,
      });
    } catch {
      setResult({
        valid: false,
        reason: "Could not reach the server. Is the backend running?",
      });
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="p-8">
      <h1 className="text-3xl font-semibold">New Project</h1>
      <p className="mt-2 text-neutral-400">
        Give your project a name and choose a content category.
      </p>

      <form
        onSubmit={handleSubmit}
        className="mt-8 flex max-w-md flex-col gap-6"
      >
        <label className="flex flex-col gap-2">
          <span className="text-sm text-neutral-300">Project name</span>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. Weekly stream highlights"
            required
            className="rounded-lg border border-neutral-700 bg-neutral-900 px-3 py-2 text-white outline-none focus:border-purple-500"
          />
        </label>

        <label className="flex flex-col gap-2">
          <span className="text-sm text-neutral-300">Content category</span>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="rounded-lg border border-neutral-700 bg-neutral-900 px-3 py-2 text-white outline-none focus:border-purple-500"
          >
            {categories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>

        <div className="flex flex-col gap-2">
          <span className="text-sm text-neutral-300">Video</span>
          <VideoDropzone onFileSelected={setVideoFile} />
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="rounded-lg bg-purple-600 px-4 py-2 font-medium text-white hover:bg-purple-500 disabled:opacity-50"
        >
          {isSubmitting ? "Checking video..." : "Create project"}
        </button>

        {result && (
          <p
            className={`text-sm ${result.valid ? "text-green-400" : "text-red-400"}`}
          >
            {result.valid
              ? `Server accepted: ${result.filename} (${result.size_bytes?.toLocaleString()} bytes)`
              : `Server rejected: ${result.reason}`}
          </p>
        )}
      </form>
    </main>
  );
}
