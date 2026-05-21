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

        // Parse blocks robustly line by line
        const lines = part.split('\n')
        const blocks = []
        let currentParagraph = []

        const flushParagraph = () => {
          if (currentParagraph.length > 0) {
            blocks.push({ type: 'paragraph', content: currentParagraph.join(' ') })
            currentParagraph = []
          }
        }

        for (let i = 0; i < lines.length; i++) {
          let line = lines[i].trim()
          if (!line) {
            flushParagraph()
            continue
          }

          // Fix common LLM markdown glitches like "Weekly Goal:*"
          line = line.replace(/:\* /g, ': ')
          line = line.replace(/:\*/g, ': ')

          // Check heading
          const headingMatch = line.match(/^(#{1,6})\s+(.*)$/)
          if (headingMatch) {
            flushParagraph()
            blocks.push({ type: 'heading', level: headingMatch[1].length, content: headingMatch[2] })
            continue
          }

          // Check list item
          if (line.startsWith('- ') || line.startsWith('* ')) {
            flushParagraph()
            const listItems = []
            while (i < lines.length) {
              const li = lines[i].trim()
              if (li.startsWith('- ') || li.startsWith('* ')) {
                // Fix missing spaces after * like "*Item"
                listItems.push(li.replace(/^[-*]\s*/, ''))
                i++
              } else {
                break
              }
            }
            i-- // step back
            blocks.push({ type: 'list', items: listItems })
            continue
          }

          currentParagraph.push(line)
        }
        flushParagraph()

        return (
          <div key={index} className="space-y-4">
            {blocks.map((block, bIdx) => {
              if (block.type === 'heading') {
                const classes = block.level === 1 ? 'font-serif italic text-xl sm:text-2xl font-semibold text-white mt-8 mb-4 border-b border-white/5 pb-2 tracking-wide' 
                              : block.level === 2 ? 'font-serif italic text-lg sm:text-xl font-medium text-white mt-6 mb-3' 
                              : block.level === 3 ? 'text-xs font-semibold text-accent2 uppercase tracking-wider mt-5 mb-2 font-mono'
                              : 'text-xs font-semibold text-accent1 uppercase tracking-wider mt-4 mb-2 font-mono'
                return React.createElement(`h${block.level}`, { key: bIdx, className: classes }, parseInlineFormatting(block.content))
              }
              
              if (block.type === 'list') {
                return (
                  <ul key={bIdx} className="list-none space-y-3.5 my-4 text-text-muted">
                    {block.items.map((item, liIdx) => (
                      <li key={liIdx} className="leading-relaxed pl-5 relative text-xs font-light">
                        <span className="absolute left-0 top-[6px] w-1.5 h-1.5 rounded-full border border-accent1 bg-accent1/25 shrink-0" />
                        {parseInlineFormatting(item)}
                      </li>
                    ))}
                  </ul>
                )
              }

              return (
                <p key={bIdx} className="text-text-muted text-xs leading-relaxed mb-4 font-light">
                  {parseInlineFormatting(block.content)}
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
      return <strong key={idx} className="font-semibold text-white tracking-wide">{token.slice(2, -2)}</strong>
    }
    if (token.startsWith('*') && token.endsWith('*')) {
      return <em key={idx} className="font-serif italic text-white/95">{token.slice(1, -1)}</em>
    }
    if (token.startsWith('`') && token.endsWith('`')) {
      return <code key={idx} className="bg-white/5 border border-white/10 px-1.5 py-0.5 rounded font-mono text-[10px] text-accent2">{token.slice(1, -1)}</code>
    }
    return token
  })
}
