import React from 'react'

export default function MarkdownRenderer({ content = '', inverted = false }) {
  if (!content) return null

  const textMain = inverted ? 'text-white/95' : 'text-ink'
  const textMuted = inverted ? 'text-white/75' : 'text-ink-muted'
  const textStrong = inverted ? 'text-white' : 'text-ink'
  const codeBg = inverted ? 'bg-white/15 border-white/20 text-white' : 'bg-stone-100 border-border text-ink'
  const headingBorder = inverted ? 'border-white/20' : 'border-border'

  const parts = content.split(/(```[\s\S]*?```)/g)

  return (
    <div className={`space-y-3 text-sm leading-relaxed ${textMain}`}>
      {parts.map((part, index) => {
        if (part.startsWith('```')) {
          const match = part.match(/```(\w*)\n([\s\S]*?)```/)
          const code = match ? match[2] : part.slice(3, -3)

          return (
            <pre
              key={index}
              className={`my-3 rounded-lg border p-3 overflow-x-auto text-xs font-mono leading-relaxed ${codeBg}`}
            >
              <code>{code.trim()}</code>
            </pre>
          )
        }

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

          line = line.replace(/:\* /g, ': ')
          line = line.replace(/:\*/g, ': ')

          const headingMatch = line.match(/^(#{1,6})\s+(.*)$/)
          if (headingMatch) {
            flushParagraph()
            blocks.push({ type: 'heading', level: headingMatch[1].length, content: headingMatch[2] })
            continue
          }

          if (line.startsWith('- ') || line.startsWith('* ')) {
            flushParagraph()
            const listItems = []
            while (i < lines.length) {
              const li = lines[i].trim()
              if (li.startsWith('- ') || li.startsWith('* ')) {
                listItems.push(li.replace(/^[-*]\s*/, ''))
                i++
              } else {
                break
              }
            }
            i--
            blocks.push({ type: 'list', items: listItems })
            continue
          }

          currentParagraph.push(line)
        }
        flushParagraph()

        return (
          <div key={index} className="space-y-3">
            {blocks.map((block, bIdx) => {
              if (block.type === 'heading') {
                const classes = block.level === 1
                  ? `font-serif text-xl font-semibold ${textStrong} mt-6 mb-3 pb-2 border-b ${headingBorder}`
                  : block.level === 2
                    ? `text-base font-semibold ${textStrong} mt-5 mb-2`
                    : `text-sm font-semibold ${textStrong} mt-4 mb-1`
                return React.createElement(`h${block.level}`, { key: bIdx, className: classes }, parseInlineFormatting(block.content, inverted))
              }

              if (block.type === 'list') {
                return (
                  <ul key={bIdx} className={`list-disc pl-5 space-y-1.5 my-2 ${textMuted}`}>
                    {block.items.map((item, liIdx) => (
                      <li key={liIdx} className="leading-relaxed">
                        {parseInlineFormatting(item, inverted)}
                      </li>
                    ))}
                  </ul>
                )
              }

              return (
                <p key={bIdx} className={`${textMuted} leading-relaxed`}>
                  {parseInlineFormatting(block.content, inverted)}
                </p>
              )
            })}
          </div>
        )
      })}
    </div>
  )
}

function parseInlineFormatting(text, inverted) {
  const tokens = text.split(/(\*\*.*?\*\*|`.*?`|\*.*?\*)/g)

  return tokens.map((token, idx) => {
    if (token.startsWith('**') && token.endsWith('**')) {
      return <strong key={idx} className={`font-semibold ${inverted ? 'text-white' : 'text-ink'}`}>{token.slice(2, -2)}</strong>
    }
    if (token.startsWith('*') && token.endsWith('*')) {
      return <em key={idx}>{token.slice(1, -1)}</em>
    }
    if (token.startsWith('`') && token.endsWith('`')) {
      return (
        <code
          key={idx}
          className={`px-1 py-0.5 rounded text-xs font-mono ${inverted ? 'bg-white/15 text-white' : 'bg-stone-100 text-ink'}`}
        >
          {token.slice(1, -1)}
        </code>
      )
    }
    return token
  })
}
