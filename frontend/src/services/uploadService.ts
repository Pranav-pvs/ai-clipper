export type ValidationResult = {
  valid: boolean;
  reason?: string;
  filename?: string;
  size_bytes?: number;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export async function validateUpload(file: File): Promise<ValidationResult> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_URL}/projects/validate-upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }

  return (await response.json()) as ValidationResult;
}