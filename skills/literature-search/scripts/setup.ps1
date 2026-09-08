param(
    [switch]$InstallPython,
    [switch]$InitConfig
)
$ErrorActionPreference = 'Stop'

function Find-TaskPython {
    $options = @(
        @{ File = 'python'; Prefix = @() },
        @{ File = 'python3'; Prefix = @() },
        @{ File = 'py'; Prefix = @('-3') },
        @{ File = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"; Prefix = @() }
    )
    foreach ($option in $options) {
        if (-not (Get-Command $option.File -ErrorAction SilentlyContinue)) { continue }
        $binary = $option.File
        $prefixArgs = $option.Prefix
        try {
            $probe = & $binary @prefixArgs -c 'import sys; print(sys.executable); sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>$null
            if ($LASTEXITCODE -eq 0) { return ($probe | Select-Object -Last 1) }
        } catch { continue }
    }
    return $null
}

$taskPython = Find-TaskPython
if (-not $taskPython -and $InstallPython) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Write-Host 'Install Python 3.10+ from https://www.python.org/downloads/windows/ and rerun setup.'
        exit 2
    }
    & winget install --id Python.Python.3.13 --exact --source winget --scope user --silent --accept-source-agreements --accept-package-agreements
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $taskPython = Find-TaskPython
}
if (-not $taskPython) {
    Write-Host 'Python 3.10+ is required. Rerun with -InstallPython or use https://www.python.org/downloads/windows/'
    exit 2
}
Write-Host "Python ready: $taskPython"
Write-Host 'This skill uses the Python standard library. No pip packages, Node.js, uv, or MCP server are required.'
if ($InitConfig) {
    & $taskPython (Join-Path $PSScriptRoot 'configure.py') --init
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
& $taskPython (Join-Path $PSScriptRoot 'literature_search.py') doctor
exit $LASTEXITCODE
