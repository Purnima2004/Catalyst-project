/**
 * Slow-moving iridescent mesh gradient — landing hero only.
 * Pure CSS, no canvas deps.
 */
export default function GradientBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden bg-[#ece8e4]" aria-hidden>
      {/* Pearl base wash */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#f8f6f3] via-[#ede9e6] to-[#e4e0ec]" />

      {/* Animated color blobs */}
      <div className="gradient-blob gradient-blob-1" />
      <div className="gradient-blob gradient-blob-2" />
      <div className="gradient-blob gradient-blob-3" />
      <div className="gradient-blob gradient-blob-4" />
      <div className="gradient-blob gradient-blob-5" />

      {/* Iridescent sheen overlay */}
      <div className="absolute inset-0 bg-gradient-to-tr from-white/50 via-transparent to-violet-100/30 mix-blend-overlay" />
      <div className="absolute inset-0 bg-gradient-to-bl from-rose-100/20 via-transparent to-sky-100/25 mix-blend-soft-light" />

      {/* Soft vignette so text stays readable */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_0%,rgba(248,246,243,0.4)_100%)]" />
    </div>
  )
}
