# Records VS Code running the review-loop tasks (Terminal > Run Task), as videos/vscode-tasks.mp4.
# It opens a separate VS Code with a clean profile (no extensions, none of your settings or tabs), drives it with
# keystrokes and records only that window with ffmpeg. Do not touch the keyboard or mouse while it runs (about 60 s).
# Usage: powershell -File record-vscode.ps1 -Repo <a git repository with REVIEW.sweeps and .vscode\tasks.json> -Out <mp4>
param([Parameter(Mandatory)][string]$Repo, [Parameter(Mandatory)][string]$Out, [string]$Base = 'HEAD~7', [string]$Tip = 'HEAD', [string]$BinDir = '')
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type @'
using System; using System.Runtime.InteropServices;
public class W {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr a, int x, int y, int w, int h2, uint f);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
}
'@
[void][W]::SetProcessDPIAware()
$tmp = Join-Path $env:TEMP 'review-loop-vscode-profile'
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force "$tmp\ud\User" | Out-Null
@'
{
  "workbench.startupEditor": "none",
  "workbench.colorTheme": "Default Dark Modern",
  "window.zoomLevel": 2,
  "editor.fontSize": 16,
  "terminal.integrated.fontSize": 16,
  "terminal.integrated.defaultProfile.windows": "PowerShell",
  "update.mode": "none",
  "telemetry.telemetryLevel": "off",
  "chat.disableAIFeatures": true,
  "workbench.tips.enabled": false,
  "workbench.enableExperiments": false,
  "extensions.autoUpdate": false,
  "security.workspace.trust.enabled": false,
  "editor.minimap.enabled": false,
  "workbench.layoutControl.enabled": false
}
'@ | Set-Content "$tmp\ud\User\settings.json" -Encoding utf8

'[ { "key": "f9", "command": "workbench.action.tasks.runTask" } ]' | Set-Content "$tmp\ud\User\keybindings.json" -Encoding utf8
if ($BinDir) { $env:PATH = "$BinDir;$env:PATH" }   # use this checkout's review-loop, not an older installed copy
$code = Join-Path $env:LOCALAPPDATA 'Programs\Microsoft VS Code\Code.exe'
$p = Start-Process $code -ArgumentList @('--user-data-dir', "$tmp\ud", '--extensions-dir', "$tmp\ext", '--new-window', $Repo) -PassThru
$leaf = Split-Path $Repo -Leaf
$h = [IntPtr]::Zero
for ($i = 0; $i -lt 60 -and $h -eq [IntPtr]::Zero; $i++) {
  Start-Sleep -Milliseconds 500
  $w = Get-Process Code -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*$leaf*" } | Select-Object -First 1
  if ($w) { $h = $w.MainWindowHandle }
}
if ($h -eq [IntPtr]::Zero) { throw 'VS Code window not found' }
$scr = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$winW = [Math]::Min(1920, $scr.Width - 80); $winH = [int]($winW * 9 / 16)
[void][W]::ShowWindow($h, 9)
[void][W]::SetWindowPos($h, [IntPtr]::Zero, 20, 20, $winW, $winH, 0x0040)
Start-Sleep -Seconds 4
[void][W]::SetForegroundWindow($h)
$r = New-Object W+RECT; [void][W]::GetWindowRect($h, [ref]$r)
$ox = [Math]::Max(0, $r.L); $oy = [Math]::Max(0, $r.T)
$vw = [int](([Math]::Min($r.R, $scr.Width) - $ox) / 2) * 2; $vh = [int](([Math]::Min($r.B, $scr.Height) - $oy) / 2) * 2
"window $($r.L),$($r.T) ${vw}x${vh} screen $($scr.Width)x$($scr.Height)"

if ($vw -lt 800 -or $vh -lt 450) { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue; throw "window rectangle is wrong ($vw x $vh); nothing was typed" }
function Test-Focus { if ([W]::GetForegroundWindow() -ne $h) { Get-Process Code -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*$leaf*" } | Stop-Process -Force; Stop-Process -Name ffmpeg -Force -ErrorAction SilentlyContinue; throw 'VS Code lost the focus; stopped before typing' } }
function Keys($s, $ms = 700) { Test-Focus; [System.Windows.Forms.SendKeys]::SendWait($s); Start-Sleep -Milliseconds $ms } function KeysOld($s, $ms = 700) { [System.Windows.Forms.SendKeys]::SendWait($s); Start-Sleep -Milliseconds $ms }
function Enter-Text($s, $ms = 60) { foreach ($c in $s.ToCharArray()) { Test-Focus; $t = [string]$c; if ('+^%~(){}[]'.Contains($t)) { $t = '{' + $t + '}' }; [System.Windows.Forms.SendKeys]::SendWait($t); Start-Sleep -Milliseconds $ms }; Start-Sleep -Milliseconds 500 }

$ff = Start-Process ffmpeg -ArgumentList @('-y', '-loglevel', 'error', '-f', 'gdigrab', '-framerate', '30', '-offset_x', $ox, '-offset_y', $oy, '-video_size', "${vw}x${vh}", '-i', 'desktop', '-vf', 'scale=1920:1080:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-t', '52', "$Out.mkv") -PassThru -NoNewWindow -RedirectStandardError "$tmp\ff.log"
Start-Sleep -Seconds 2
# Run Task > review-loop: sweeps
Keys '^b' 1000
Keys '{F9}' 1800
Enter-Text 'review-loop: sweeps'
Keys '{ENTER}' 1800
Enter-Text $Base
Keys '{ENTER}' 1200
Enter-Text $Tip
Keys '{ENTER}' 15000
# Problems panel, then step through the hits
Keys '^+m' 2500
Keys '{DOWN}' 800
Keys '{ENTER}' 4500
Keys '{F8}' 4000
Start-Sleep -Seconds 2
# stop the recording cleanly
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public class K { [DllImport("kernel32.dll")] public static extern bool GenerateConsoleCtrlEvent(uint e, uint g); }' -ErrorAction SilentlyContinue
[void]$ff.WaitForExit(30000)
Get-Content "$tmp\ff.log" -ErrorAction SilentlyContinue | Select-Object -First 5
Start-Sleep -Seconds 1
Stop-Process -Id $p.Id -ErrorAction SilentlyContinue
Get-Process Code -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*$leaf*" } | Stop-Process -Force -ErrorAction SilentlyContinue
ffmpeg -y -loglevel error -i "$Out.mkv" -c copy $Out
Remove-Item "$Out.mkv"
"done"
