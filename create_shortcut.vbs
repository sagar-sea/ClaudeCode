Set objShell = CreateObject("WScript.Shell")
strDesktop = objShell.SpecialFolders("Desktop")
Set objShortCut = objShell.CreateShortcut(strDesktop & "\Ollama Claude Launcher.lnk")
objShortCut.TargetPath = objShell.ExpandEnvironmentStrings("%USERPROFILE%\ClaudeCode\ollama_claude_launcher.bat")
objShortCut.WorkingDirectory = objShell.ExpandEnvironmentStrings("%USERPROFILE%\ClaudeCode")
objShortCut.WindowStyle = 1
objShortCut.IconLocation = "shell32.dll, 13"
objShortCut.Description = "Ollama + Claude Code Launcher"
objShortCut.Save