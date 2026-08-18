param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,
    [Parameter(Mandatory = $true)]
    [string]$OutputAssembly,
    [string]$RoslynRoot = ''
)

$ErrorActionPreference = 'Stop'

if (-not $RoslynRoot) {
    $RoslynRoot = Join-Path $PSScriptRoot '..\..\..\Users\WINDOW XI\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell'
    if (-not (Test-Path -LiteralPath $RoslynRoot)) {
        $RoslynRoot = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell'
    }
}

$required = @(
    'System.Collections.Immutable.dll',
    'System.Reflection.Metadata.dll',
    'Microsoft.CodeAnalysis.dll',
    'Microsoft.CodeAnalysis.CSharp.dll'
)
foreach ($name in $required) {
    $path = Join-Path $RoslynRoot $name
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Roslyn dependency missing: $path"
    }
}
Add-Type -Path ($required | ForEach-Object { Join-Path $RoslynRoot $_ })

$sources = Get-ChildItem -LiteralPath $ProjectRoot -Recurse -File -Filter '*.cs' | Sort-Object FullName
if ($sources.Count -eq 0) {
    throw "No C# sidecar sources found under $ProjectRoot"
}

$trees = [System.Collections.Generic.List[Microsoft.CodeAnalysis.SyntaxTree]]::new()
$parseDiagnostics = [System.Collections.Generic.List[string]]::new()
foreach ($source in $sources) {
    $text = [System.IO.File]::ReadAllText($source.FullName)
    $tree = [Microsoft.CodeAnalysis.CSharp.CSharpSyntaxTree]::ParseText(
        $text,
        [Microsoft.CodeAnalysis.CSharp.CSharpParseOptions]::Default,
        $source.FullName
    )
    [void]$trees.Add($tree)
    foreach ($diagnostic in $tree.GetDiagnostics()) {
        if ($diagnostic.Severity -eq [Microsoft.CodeAnalysis.DiagnosticSeverity]::Error) {
            [void]$parseDiagnostics.Add($diagnostic.ToString())
        }
    }
}

$tpa = [System.AppContext]::GetData('TRUSTED_PLATFORM_ASSEMBLIES')
$referencePaths = @()
if ($tpa) {
    $referencePaths = $tpa -split [System.IO.Path]::PathSeparator
}
$references = [System.Collections.Generic.List[Microsoft.CodeAnalysis.MetadataReference]]::new()
foreach ($referencePath in $referencePaths | Sort-Object -Unique) {
    if (Test-Path -LiteralPath $referencePath) {
        [void]$references.Add([Microsoft.CodeAnalysis.MetadataReference]::CreateFromFile($referencePath))
    }
}

$parsePass = $parseDiagnostics.Count -eq 0
$compileDiagnostics = @()
$emitSuccess = $false
$outputBytes = 0
if ($parsePass) {
    $options = [Microsoft.CodeAnalysis.CSharp.CSharpCompilationOptions]::new(
        [Microsoft.CodeAnalysis.OutputKind]::DynamicallyLinkedLibrary
    )
    $treeArray = [Microsoft.CodeAnalysis.SyntaxTree[]]$trees.ToArray()
    $referenceArray = [Microsoft.CodeAnalysis.MetadataReference[]]$references.ToArray()
    $compilation = [Microsoft.CodeAnalysis.CSharp.CSharpCompilation]::Create(
        'SocialDev.T1Pilot.Sidecars',
        $treeArray,
        $referenceArray,
        $options
    )
    $compileDiagnostics = @($compilation.GetDiagnostics() | Where-Object Severity -eq ([Microsoft.CodeAnalysis.DiagnosticSeverity]::Error) | ForEach-Object ToString)
    if ($compileDiagnostics.Count -eq 0) {
        $parent = Split-Path -Parent $OutputAssembly
        if ($parent) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
        $stream = [System.IO.File]::Open($OutputAssembly, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
        try {
            $emit = $compilation.Emit($stream)
            $emitSuccess = $emit.Success
            if (-not $emit.Success) {
                $compileDiagnostics = @($emit.Diagnostics | Where-Object Severity -eq ([Microsoft.CodeAnalysis.DiagnosticSeverity]::Error) | ForEach-Object ToString)
            }
        } finally {
            $stream.Dispose()
        }
        if (Test-Path -LiteralPath $OutputAssembly) {
            $outputBytes = (Get-Item -LiteralPath $OutputAssembly).Length
        }
    }
}

$result = [ordered]@{
    schema_version = 't1-0-sidecar-compile-v1'
    roslyn_root = $RoslynRoot
    source_count = $sources.Count
    sidecar_method_source_count = @($sources | Where-Object FullName -match '\\Methods\\').Count
    parse_pass = $parsePass
    parse_error_count = $parseDiagnostics.Count
    parse_errors = @($parseDiagnostics)
    compile_pass = $emitSuccess
    compile_error_count = $compileDiagnostics.Count
    compile_errors = @($compileDiagnostics)
    output_assembly = $OutputAssembly
    output_bytes = $outputBytes
}
$result | ConvertTo-Json -Depth 6 -Compress
if (-not ($parsePass -and $emitSuccess)) {
    exit 1
}
