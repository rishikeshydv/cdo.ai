export default function Badge({ label }: { label: string }) {
  return (
    <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded bg-slate-50 border border-slate-100 text-sm text-slate-700">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden>
        <path d="M12 1l3 6 6 1-4.5 4 1 6L12 17l-5.5 3 1-6L3 8l6-1 3-6z" stroke="#0b6e4f" strokeWidth="0.8" strokeLinejoin="round" />
      </svg>
      <span>{label}</span>
    </div>
  );
}
