import Link from "next/link";

const navItems = [
  { label: "Dashboard", href: "/" },
  { label: "New Project", href: "/projects/new" },
  { label: "My Projects", href: "/projects" },
  { label: "AI Clip Generator", href: "/clip-generator" },
  { label: "Caption Studio", href: "/caption-studio" },
  { label: "Music Library", href: "/music-library" },
  { label: "Export History", href: "/exports" },
  { label: "Settings", href: "/settings" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 shrink-0 border-r border-neutral-800 bg-neutral-900 p-4">
      <div className="mb-6 text-lg font-semibold text-white">AI Clipper</div>
      <nav className="flex flex-col gap-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="rounded-lg px-3 py-2 text-sm text-neutral-300 hover:bg-neutral-800 hover:text-white"
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}