create table projects (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 1 and 120),
  category text not null,
  video_filename text,
  video_size_bytes bigint check (video_size_bytes >= 0),
  video_path text,
  transcript_text text,
  transcript_segments jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now()
);

-- Block public access through the anon key. The backend uses the service key, which bypasses this.
alter table projects enable row level security;

grant select, insert, update, delete on public.projects to service_role;