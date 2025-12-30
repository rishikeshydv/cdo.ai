export default function Testimonial({ quote, author, role }: { quote: string; author: string; role: string }) {
  return (
    <figure className="p-4 border rounded-md bg-white">
      <blockquote className="text-sm text-slate-800">“{quote}”</blockquote>
      <figcaption className="mt-3 text-xs text-slate-600">
        <div className="font-medium">{author}</div>
        <div>{role}</div>
      </figcaption>
    </figure>
  );
}
