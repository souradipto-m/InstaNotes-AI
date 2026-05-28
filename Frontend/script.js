let generatedMarkdown = ""

async function generateNotes() {

  const topic =
    document.getElementById("topic").value

  const level =
    document.getElementById("level").value

  const semester =
    document.getElementById("semester").value

  const notesType =
    document.getElementById("notesType").value

  const notesOutput =
    document.getElementById("notesOutput")

  if (!topic.trim()) {

    alert("Please enter a topic")

    return
  }

  notesOutput.innerHTML = `
  
    <div class="loader">
      ✨ Generating intelligent notes...
    </div>
  
  `

  try {

    const response = await fetch(
      "http://127.0.0.1:8000/generate-notes",
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          topic: topic,
          level: level,
          semester: semester,
          notes_type: notesType
        })
      }
    )

    const data = await response.json()

    generatedMarkdown = data.notes

    notesOutput.innerHTML =
      marked.parse(generatedMarkdown)

    hljs.highlightAll()

  } catch (error) {

    console.error(error)

    notesOutput.innerHTML = `
    
      <div class="placeholder">
        ❌ Error generating notes.
      </div>
    
    `
    
  }
}

function downloadDOC() {

  if (!generatedMarkdown) {

    alert("Generate notes first")

    return
  }

  const topic =
    document.getElementById("topic").value

  const htmlContent = `
  
  <html>

    <head>

      <meta charset="utf-8">

      <title>${topic} Notes</title>

      <style>

        body {
          font-family: Arial, sans-serif;
          padding: 40px;
          line-height: 1.8;
          color: #111;
        }

        h1, h2, h3 {
          color: #6d28d9;
        }

        table {
          width: 100%;
          border-collapse: collapse;
          margin: 20px 0;
        }

        th, td {
          border: 1px solid #ccc;
          padding: 12px;
          text-align: left;
        }

        th {
          background: #f3f4f6;
        }

        pre {
          background: #111827;
          color: white;
          padding: 16px;
          border-radius: 8px;
          overflow-x: auto;
        }

        code {
          background: #f3f4f6;
          padding: 2px 6px;
          border-radius: 4px;
        }

      </style>

    </head>

    <body>

      ${marked.parse(generatedMarkdown)}

    </body>

  </html>

  `

  const blob = new Blob(
    [htmlContent],
    {
      type: "application/msword"
    }
  )

  const link =
    document.createElement("a")

  link.href =
    URL.createObjectURL(blob)

  link.download =
    `${topic}_Notes.doc`

  document.body.appendChild(link)

  link.click()

  document.body.removeChild(link)
}