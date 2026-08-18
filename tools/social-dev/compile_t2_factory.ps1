param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,
    [Parameter(Mandatory = $true)]
    [string]$OutputAssembly,
    [Parameter(Mandatory = $true)]
    [string]$DiagnosticsPath,
    [string]$RoslynRoot = ''
)

$ErrorActionPreference = 'Stop'

if (-not $RoslynRoot) {
    $RoslynRoot = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell'
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

function Get-RootCause([string]$Id, [string]$Message) {
    if ($Id -in @('CS0101', 'CS0102', 'CS0111', 'CS0121')) { return 'DUPLICATE_MEMBER' }
    if ($Id -in @('CS0535', 'CS0539', 'CS0738', 'CS0737')) { return 'INTERFACE_CONTRACT' }
    if ($Id -in @('CS0506', 'CS0527', 'CS0528', 'CS0146', 'CS1721', 'CS0234')) { return 'INHERITANCE' }
    if ($Id -in @('CS0695', 'CS0305', 'CS7003', 'CS0412', 'CS0452')) { return 'GENERIC_ARITY' }
    if ($Id -in @('CS0206', 'CS1510', 'CS8170', 'CS8156')) { return 'BYREF_SIGNATURE' }
    if ($Id -in @('CS0029', 'CS0266', 'CS1503')) { return 'RETURN_CONVERSION' }
    if ($Id -in @('CS0246', 'CS0234')) { return 'BOUNDARY_TYPE' }
    if ($Id -in @('CS0171', 'CS0177', 'CS0188', 'CS0229')) { return 'FIELD_DECLARATION' }
    if ($Id -in @('CS1729', 'CS0516', 'CS1950')) { return 'CONSTRUCTOR_BASE' }
    if ($Id -in @('CS0122', 'CS0120', 'CS0050', 'CS0051')) { return 'ACCESSIBILITY' }
    if ($Id -in @('CS8370', 'CS8652', 'CS9058')) { return 'LANGUAGE_VERSION' }
    if ($Id -in @('CS0117', 'CS1061', 'CS1501', 'CS1929')) { return 'RUNTIME_TRAMPOLINE_API' }
    if ($Message -match 'nested|containing type|type parameter') { return 'NESTED_TYPE' }
    if ($Message -match 'return|conversion|cannot implicitly convert') { return 'RETURN_CONVERSION' }
    if ($Message -match 'field|unassigned') { return 'FIELD_DECLARATION' }
    return 'TYPE_DECLARATION'
}

function Get-MethodId([string]$File, [int]$Line) {
    if (-not (Test-Path -LiteralPath $File)) { return $null }
    $lines = [System.IO.File]::ReadAllLines($File)
    $start = [Math]::Min($Line, $lines.Length - 1)
    for ($index = $start; $index -ge 0; $index--) {
        $match = [regex]::Match($lines[$index], 'TwinCanonicalMethod\("([^"]+)"')
        if ($match.Success) { return $match.Groups[1].Value }
    }
    return $null
}

function Convert-Diagnostic($Diagnostic) {
    $span = $Diagnostic.Location.GetLineSpan()
    $file = $span.Path
    $line = $span.StartLinePosition.Line + 1
    $column = $span.StartLinePosition.Character + 1
    $message = $Diagnostic.GetMessage()
    [ordered]@{
        code = $Diagnostic.Id
        severity = $Diagnostic.Severity.ToString()
        message = $message
        message_fingerprint = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes($message))).ToLowerInvariant()
        file = $file
        line = $line
        column = $column
        method_id = if ($file) { Get-MethodId $file ($line - 1) } else { $null }
        root_cause_family = Get-RootCause $Diagnostic.Id $message
    }
}

$sources = @(Get-ChildItem -LiteralPath $ProjectRoot -Recurse -File -Filter '*.cs' | Sort-Object FullName)
if ($sources.Count -eq 0) { throw "No C# sources found under $ProjectRoot" }

$parseOptions = [Microsoft.CodeAnalysis.CSharp.CSharpParseOptions]::Default.WithLanguageVersion([Microsoft.CodeAnalysis.CSharp.LanguageVersion]::Latest)
$trees = [System.Collections.Generic.List[Microsoft.CodeAnalysis.SyntaxTree]]::new()
$parseDiagnostics = [System.Collections.Generic.List[object]]::new()
foreach ($source in $sources) {
    $text = [System.IO.File]::ReadAllText($source.FullName)
    $tree = [Microsoft.CodeAnalysis.CSharp.CSharpSyntaxTree]::ParseText($text, $parseOptions, $source.FullName)
    [void]$trees.Add($tree)
    foreach ($diagnostic in $tree.GetDiagnostics() | Where-Object Severity -eq ([Microsoft.CodeAnalysis.DiagnosticSeverity]::Error)) {
        [void]$parseDiagnostics.Add((Convert-Diagnostic $diagnostic))
    }
}

$tpa = [System.AppContext]::GetData('TRUSTED_PLATFORM_ASSEMBLIES')
$referencePaths = @()
if ($tpa) { $referencePaths = $tpa -split [System.IO.Path]::PathSeparator }
$references = [System.Collections.Generic.List[Microsoft.CodeAnalysis.MetadataReference]]::new()
foreach ($referencePath in $referencePaths | Sort-Object -Unique) {
    if (Test-Path -LiteralPath $referencePath) {
        [void]$references.Add([Microsoft.CodeAnalysis.MetadataReference]::CreateFromFile($referencePath))
    }
}

$compileDiagnostics = [System.Collections.Generic.List[object]]::new()
$emitSuccess = $false
$outputBytes = 0
if ($parseDiagnostics.Count -eq 0) {
    $options = [Microsoft.CodeAnalysis.CSharp.CSharpCompilationOptions]::new([Microsoft.CodeAnalysis.OutputKind]::DynamicallyLinkedLibrary)
    $options = $options.WithDeterministic($true).WithOptimizationLevel([Microsoft.CodeAnalysis.OptimizationLevel]::Release)
    $compilation = [Microsoft.CodeAnalysis.CSharp.CSharpCompilation]::Create(
        'SocialDev.T2WholeTwin',
        [Microsoft.CodeAnalysis.SyntaxTree[]]$trees.ToArray(),
        [Microsoft.CodeAnalysis.MetadataReference[]]$references.ToArray(),
        $options
    )
    foreach ($diagnostic in $compilation.GetDiagnostics() | Where-Object Severity -eq ([Microsoft.CodeAnalysis.DiagnosticSeverity]::Error)) {
        [void]$compileDiagnostics.Add((Convert-Diagnostic $diagnostic))
    }
    if ($compileDiagnostics.Count -eq 0) {
        $parent = Split-Path -Parent $OutputAssembly
        if ($parent) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
        $stream = [System.IO.File]::Open($OutputAssembly, [System.IO.FileMode]::Create, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
        try {
            $emit = $compilation.Emit($stream)
            $emitSuccess = $emit.Success
            if (-not $emit.Success) {
                foreach ($diagnostic in $emit.Diagnostics | Where-Object Severity -eq ([Microsoft.CodeAnalysis.DiagnosticSeverity]::Error)) {
                    [void]$compileDiagnostics.Add((Convert-Diagnostic $diagnostic))
                }
            }
        } finally {
            $stream.Dispose()
        }
        if (Test-Path -LiteralPath $OutputAssembly) { $outputBytes = (Get-Item -LiteralPath $OutputAssembly).Length }
    }
}

$allDiagnostics = @($parseDiagnostics.ToArray()) + @($compileDiagnostics.ToArray())
$byCode = [ordered]@{}
$byFamily = [ordered]@{}
foreach ($diagnostic in $allDiagnostics) {
    if (-not $byCode.Contains($diagnostic.code)) { $byCode[$diagnostic.code] = 0 }
    $byCode[$diagnostic.code]++
    if (-not $byFamily.Contains($diagnostic.root_cause_family)) { $byFamily[$diagnostic.root_cause_family] = 0 }
    $byFamily[$diagnostic.root_cause_family]++
}

$result = [ordered]@{
    schema_version = 't2-roslyn-compile-v1'
    roslyn_root = $RoslynRoot
    project_root = $ProjectRoot
    source_count = $sources.Count
    parse_pass = $parseDiagnostics.Count -eq 0
    parse_error_count = $parseDiagnostics.Count
    compile_pass = $emitSuccess
    compile_error_count = $compileDiagnostics.Count
    parse_errors = @($parseDiagnostics.ToArray())
    compile_errors = @($compileDiagnostics.ToArray())
    diagnostics_by_code = $byCode
    diagnostics_by_root_cause_family = $byFamily
    output_assembly = $OutputAssembly
    output_bytes = $outputBytes
}

$parentDiagnostics = Split-Path -Parent $DiagnosticsPath
if ($parentDiagnostics) { New-Item -ItemType Directory -Path $parentDiagnostics -Force | Out-Null }
$result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $DiagnosticsPath -Encoding UTF8
$result | ConvertTo-Json -Depth 12 -Compress
if (-not ($result.parse_pass -and $result.compile_pass)) { exit 1 }
