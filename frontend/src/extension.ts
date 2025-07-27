import * as vscode from 'vscode';
import axios from 'axios';

let panel: vscode.WebviewPanel | undefined;

export function activate(context: vscode.ExtensionContext) {
  let disposable = vscode.commands.registerCommand('extension.optimizeCode', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor found');
      return;
    }
    const selection = editor.selection;
    const code = editor.document.getText(selection);
    if (!code) {
      vscode.window.showErrorMessage('No code selected');
      return;
    }

    try {
      const response = await axios.post('http://localhost:8000/optimize', {
        code,
        language: editor.document.languageId,
      });

      const optimizedCode = response.data.optimized_code;

      if (!panel) {
        panel = vscode.window.createWebviewPanel(
          'cyberpunkCodeOptimizer',
          'Cyberpunk Code Optimizer',
          vscode.ViewColumn.Beside,
          {
            enableScripts: true,
            localResourceRoots: []
          }
        );

        panel.onDidDispose(() => {
          panel = undefined;
        });
      }

      panel.webview.html = getWebviewContent(optimizedCode, editor.document.languageId);
    } catch (error: any) {
      vscode.window.showErrorMessage(`Optimization failed: ${error.message}`);
    }
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}

function getWebviewContent(code: string, language: string) {
  const escapedCode = code.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Cyberpunk Code Optimizer</title>
  <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css');
    body {
      margin: 0; padding: 1rem;
      background: #0f0f1a;
      color: #f0f0f7;
      font-family: 'Courier New', Courier, monospace;
      user-select: text;
      height: 100vh;
    }
    h2 {
      color: #ff007f;
      text-shadow: 0 0 10px #ff007f;
      font-weight: bold;
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
      font-family: 'Orbitron', sans-serif;
    }
    pre {
      background: linear-gradient(45deg, #1f0037, #0f001a);
      padding: 1rem;
      border-radius: 10px;
      overflow-x: auto;
      box-shadow: 0 0 15px #ff00bf;
      font-size: 14px;
      line-height: 1.4;
    }
    /* Neon glow effect on code */
    code {
      color: #ff79c6;
      text-shadow:
        0 0 5px #ff79c6,
        0 0 10px #ff79c6,
        0 0 20px #ff79c6;
    }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
</head>
<body>
  <h2>Optimized Code</h2>
  <pre><code class="language-${language}" id="code-block">${escapedCode}</code></pre>

  <script>
    Prism.highlightAll();
  </script>
</body>
</html>`;
}