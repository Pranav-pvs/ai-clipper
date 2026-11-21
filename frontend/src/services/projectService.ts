export type Project = {
  id: string;
  name: string;
  category: string;
  video_filename?: string | null;
  video_size_bytes?: number | null;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export async function createProject(input: {
  name: string;
  category: string;
  video_filename?: string;
  video_size_bytes?: number;
}): Promise<Project> {
  const response = await fetch(`${API_URL}/projects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });

  if (!response.ok) {
    throw new Error(`Could not create project (${response.status})`);
  }

  return (await response.json()) as Project;
}