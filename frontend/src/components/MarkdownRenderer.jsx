import React from 'react'

export default function MarkdownRenderer({ content = '' }) {
  if (!content) return null

  // Split by code blocks to isolate formatted code
  const parts = content.split(/(```[\s\S]*?```)/g)

  return (
    <div className="space-y-3.5 text-[14px] leading-relaxed text-primaryText/90">
      {parts.map((part, index) => {
        if (part.startsWith('```')) {
          // Extract language and code block content
          const match = part.match(/```(\w*)\n([\s\S]*?)```/)
          const lang = match ? match[1] : ''
          const code = match ? match[2] : part.slice(3, -3)

          return (
            <div key={index} className="my-4 rounded-xl overflow-hidden border border-white/10 shadow-lg">
              {lang && (
                <div className="bg-white/5 px-4 py-1.5 text-xs text-primaryText/40 border-b border-white/5 font-mono select-none flex justify-between items-center">
                  <span>{lang.toUpperCase()}</span>
                  <span className="text-[10px]">Code Block</span>
                </div>
              )}
              <pre className="bg-[#05060f] p-4 overflow-x-auto font-mono text-xs text-[#a5b4fc] leading-relaxed">
                <code>{code.trim()}</code>
              </pre>
            </div>
          )
        }

        // Parse paragraphs, lists, and inline markdown
        return (
          <div key={index} className="space-y-3">
            {part.split('\n\n').map((paragraph, pIdx) => {
              const trimmed = paragraph.trim()
              if (!trimmed) return null

              // Check if it's a bulleted list
              if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
                // Split correctly into items
                const items = trimmed.split(/\n[-*] /g).map(item => item.replace(/^[-*] /, ''))
                return (
                  <ul key={pIdx} className="list-disc pl-5 space-y-2 my-2 text-primaryText/80">
                    {items.map((item, liIdx) => (
                      <li key={liIdx}>
                        {parseInlineFormatting(item)}
                      </li>
                    ))}
                  </ul>
                )
              }

              // Check for headings (e.g. ## Heading)
              if (trimmed.startsWith('#')) {
                const match = trimmed.match(/^(#{1,6})\s+(.*)$/)
                if (match) {
                  const level = match[1].length
                  const text = match[2]
                  const classes = level === 1 ? 'text-2xl font-bold text-white' 
                                : level === 2 ? 'text-xl font-bold text-accent2' 
                                : 'text-lg font-semibold text-accent1'
                  return React.createElement(`h${level}`, { key: pIdx, className: `${classes} mt-4 mb-2` }, parseInlineFormatting(text))
                }
              }

              return (
                <p key={pIdx} className="text-primaryText/85 leading-relaxed">
                  {parseInlineFormatting(paragraph)}
                </p>
              )
            })}
          </div>
        )
      })}
    </div>
  )
}

function parseInlineFormatting(text) {
  // Split on bold (**), italics (*), and inline code (`) tokens
  const tokens = text.split(/(\*\*.*?\*\*|`.*?`|\*.*?\*)/g)
  
  return tokens.map((token, idx) => {
    if (token.startsWith('**') && token.endsWith('**')) {
      return <strong key={idx} className="font-semibold text-white">{token.slice(2, -2)}</strong>
    }
    if (token.startsWith('*') && token.endsWith('*')) {
      return <em key={idx} className="italic text-primaryText/90">{token.slice(1, -1)}</em>
    }
    if (token.startsWith('`') && token.endsWith('`')) {
      return <code key={idx} className="bg-white/10 px-1.5 py-0.5 rounded font-mono text-[12px] text-fuchsia-300">{token.slice(1, -1)}</code>
    }
    return token
  })
}
