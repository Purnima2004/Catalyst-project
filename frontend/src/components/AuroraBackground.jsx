export default function AuroraBackground() {
  return (
    <div className="fixed inset-0 pointer-events-none z-0 bg-background">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_#ffffff_0%,_#f7f6f3_55%)]" />
      <div className="absolute top-0 right-0 w-[480px] h-[480px] bg-blue-50/60 rounded-full blur-3xl -translate-y-1/3 translate-x-1/4" />
    </div>
  )
}
