# Drives a real VS Code window step by step and records only that window. Used for the Copilot chat recording.
#   vscode-drive.ps1 start <repo> <out.mp4> [minutes]   open VS Code on the repo (your normal profile), start recording
#   vscode-drive.ps1 keys "<SendKeys string>"           send keys, only if that window has the focus
#   vscode-drive.ps1 text "<text>"                      type text, character by character
#   vscode-drive.ps1 shot <png>                         one picture of the window (to look at what is on screen)
#   vscode-drive.ps1 stop                               stop recording, write the mp4, close the window
# Nothing is typed unless the VS Code window is the foreground window. Do not use the keyboard or mouse meanwhile.
param([Parameter(Mandatory)][string]$Cmd, [string]$A = '', [string]$B = '', [int]$Minutes = 8)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type @'
using System; using System.Runtime.InteropServices;
public class V {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr a, int x, int y, int w, int hh, uint f);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc p, IntPtr l);
  [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, System.Text.StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint m, IntPtr w, IntPtr l);
  public static IntPtr Find(string leaf) {
    IntPtr found = IntPtr.Zero;
    EnumWindows((h, l) => {
      if (!IsWindowVisible(h)) return true;
      var sb = new System.Text.StringBuilder(512); GetWindowText(h, sb, 512);
      string t = sb.ToString();
      if (t.Contains(leaf) && t.Contains("Visual Studio Code")) { found = h; return false; }
      return true;
    }, IntPtr.Zero);
    return found;
  }
}
'@
[void][V]::SetProcessDPIAware()
$state = Join-Path $env:TEMP 'vscode-drive.json'

function Get-Win($leaf) {
  $h = [V]::Find($leaf)
  if ($h -eq [IntPtr]::Zero) { throw "no VS Code window for $leaf" }
  return $h
}
function Get-Rect($h) {
  $r = New-Object V+RECT; [void][V]::GetWindowRect($h, [ref]$r)
  $scr = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
  $ox = [Math]::Max(0, $r.L) + 8; $oy = [Math]::Max(0, $r.T)
  $w = [int](([Math]::Min($r.R, $scr.Width) - $ox - 8) / 2) * 2; $ht = [int](([Math]::Min($r.B, $scr.Height) - $oy - 12) / 2) * 2
  return @{ x = $ox; y = $oy; w = $w; h = $ht }
}
function Assert-Focus($h) {
  [void][V]::SetForegroundWindow($h); Start-Sleep -Milliseconds 150
  if ([V]::GetForegroundWindow() -ne $h) { throw 'VS Code does not have the focus; nothing was typed' }
}

switch ($Cmd) {
  'start' {
    $repo = $A; $out = $B; $leaf = Split-Path $repo -Leaf
    $code = Join-Path $env:LOCALAPPDATA 'Programs\Microsoft VS Code\Code.exe'
    Start-Process $code -ArgumentList @('--new-window', '--disable-workspace-trust', $repo) | Out-Null
    $h = [IntPtr]::Zero
    for ($i = 0; $i -lt 80 -and $h -eq [IntPtr]::Zero; $i++) { Start-Sleep -Milliseconds 500; try { $h = Get-Win $leaf } catch {} }
    if ($h -eq [IntPtr]::Zero) { throw 'window not found' }
    $scr = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $ww = [Math]::Min(1920, $scr.Width - 80); $wh = [int]($ww * 9 / 16)
    [void][V]::ShowWindow($h, 9); [void][V]::SetWindowPos($h, [IntPtr]::Zero, 20, 20, $ww, $wh, 0x0040)
    Start-Sleep -Seconds 25   # let the account and chat finish loading before anything is recorded
    Assert-Focus $h
    $g = Get-Rect $h
    $ff = Start-Process ffmpeg -ArgumentList @('-y', '-loglevel', 'error', '-f', 'gdigrab', '-framerate', '30', '-offset_x', $g.x, '-offset_y', $g.y, '-video_size', "$($g.w)x$($g.h)", '-i', 'desktop', '-vf', 'scale=1920:1080:flags=lanczos,format=yuv420p', '-c:v', 'libx264', '-crf', '22', '-preset', 'veryfast', '-t', ($Minutes * 60), "$out.mkv") -PassThru -NoNewWindow -RedirectStandardOutput "$out.log" -RedirectStandardError "$out.err"
    @{ leaf = $leaf; out = $out; ff = $ff.Id } | ConvertTo-Json | Set-Content $state
    "started: window $($g.w)x$($g.h) at $($g.x),$($g.y)"
  }
  'keys' { $s = Get-Content $state | ConvertFrom-Json; $h = Get-Win $s.leaf; Assert-Focus $h; [System.Windows.Forms.SendKeys]::SendWait($A); Start-Sleep -Milliseconds 400; 'sent' }
  'text' {
    $s = Get-Content $state | ConvertFrom-Json; $h = Get-Win $s.leaf
    foreach ($c in $A.ToCharArray()) { Assert-Focus $h; $t = [string]$c; if ('+^%~(){}[]'.Contains($t)) { $t = '{' + $t + '}' }; [System.Windows.Forms.SendKeys]::SendWait($t); Start-Sleep -Milliseconds 55 }
    'typed'
  }
  'shot' {
    $s = Get-Content $state | ConvertFrom-Json; $h = Get-Win $s.leaf; $g = Get-Rect $h
    ffmpeg -y -loglevel error -f gdigrab -framerate 1 -offset_x $g.x -offset_y $g.y -video_size "$($g.w)x$($g.h)" -i desktop -frames:v 1 -vf 'scale=1280:720' $A
    'shot ' + $A
  }
  'stop' {
    $s = Get-Content $state | ConvertFrom-Json
    Stop-Process -Id $s.ff -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2
    ffmpeg -y -loglevel error -i "$($s.out).mkv" -c copy $s.out 2>&1 | Out-Null
    Remove-Item "$($s.out).mkv" -ErrorAction SilentlyContinue
    [void][V]::PostMessage((Get-Win $s.leaf), 0x0010, [IntPtr]::Zero, [IntPtr]::Zero)
    'stopped'
  }
}
