import React from 'react'

export default function AuroraBackground() {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 bg-background">
      {/* Animated Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-accent1/30 mix-blend-screen blur-[100px] animate-blob" />
      <div 
        className="absolute top-[10%] right-[-10%] w-[45vw] h-[45vw] rounded-full bg-accent2/30 mix-blend-screen blur-[100px] animate-blob" 
        style={{ animationDelay: '2s' }} 
      />
      <div 
        className="absolute bottom-[-20%] left-[20%] w-[60vw] h-[60vw] rounded-full bg-blue-600/20 mix-blend-screen blur-[120px] animate-blob" 
        style={{ animationDelay: '4s' }} 
      />

      {/* Mesh / Stars Overlay */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,255,255,0.03)_0%,transparent_100%)]" />
      <div 
        className="absolute inset-0 opacity-20" 
        style={{
          backgroundImage: 'radial-gradient(rgba(255, 255, 255, 0.4) 1px, transparent 1px)',
          backgroundSize: '40px 40px'
        }} 
      />
    </div>
  )
}
