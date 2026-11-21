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

export async function uploadProjectVideo(projectId: string, file: File): Promise<Project> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/projects/${projectId}/video`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? `Could not upload video (${response.status})`);
  }

  return (await response.json()) as Project;
}