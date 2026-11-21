"use client";

import { useState } from "react";

const categories = ["Gaming", "Podcasts", "Cricket", "Other Sports", "Other"];

export default function NewProjectPage() {
  const [name, setName] = useState("");
  const [category, setCategory] = useState(categories[0]);

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    console.log("New project:", { name, category });
  }

  return (
    <main className="p-8">
      <h1 className="text-3xl font-semibold">New Project</h1>
      <p className="mt-2 text-neutral-400">
        Give your project a name and choose a content category.
      </p>

      <form onSubmit={handleSubmit} className="mt-8 flex max-w-md flex-col gap-6">
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

        <button
          type="submit"
          className="rounded-lg bg-purple-600 px-4 py-2 font-medium text-white hover:bg-purple-500"
        >
          Create project
        </button>
      </form>
    </main>
  );
}