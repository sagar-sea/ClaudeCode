Set objShell = CreateObject("WScript.Shell")
strDesktop = objShell.SpecialFolders("Desktop")
Set objShortCut = objShell.CreateShortcut(strDesktop & "\Ollama Claude Launcher Enhanced.lnk")
objShortCut.TargetPath = "C:\Users\Sagar\ClaudeCode\ollama_claude_launcher_enhanced.bat"
objShortCut.WorkingDirectory = "C:\Users\Sagar\ClaudeCode"
objShortCut.WindowStyle = 1
objShortCut.IconLocation = "shell32.dll, 13"
objShortCut.Description = "Enhanced Ollama + Claude Code Launcher"
objShortCut.Save