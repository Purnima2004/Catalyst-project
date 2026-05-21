import React from 'react'

export default function AuroraBackground() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 bg-[#07080e]">
      {/* Editorial Sophisticated Ambient Glows */}
      <div className="absolute top-[-25%] left-[-10%] w-[60vw] h-[60vw] rounded-full bg-accent1/8 blur-[130px] mix-blend-normal pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[55vw] h-[55vw] rounded-full bg-accent2/4 blur-[130px] mix-blend-normal pointer-events-none" />
      <div className="absolute top-[30%] left-[40%] w-[40vw] h-[40vw] rounded-full bg-accent1/3 blur-[160px] mix-blend-normal pointer-events-none" />

      {/* Stationary Premium Micro-Fine Technical Grid */}
      <div className="absolute inset-0 opacity-[0.035]" 
           style={{
             backgroundImage: `
               linear-gradient(to right, rgba(255,255,255,0.15) 1px, transparent 1px),
               linear-gradient(to bottom, rgba(255,255,255,0.15) 1px, transparent 1px)
             `,
             backgroundSize: '48px 48px'
           }} 
      />

      {/* Radial overlay to soften grid edges and simulate lighting */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_20%,#07080e_95%)] opacity-85" />
      
      {/* Grain overlay for paper/editorial noise feel */}
      <div className="absolute inset-0 opacity-[0.015] bg-repeat pointer-events-none"
           style={{
             backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`
           }}
      />
    </div>
  )
}
