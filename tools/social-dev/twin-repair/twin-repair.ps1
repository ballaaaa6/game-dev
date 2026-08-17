$ErrorActionPreference = 'Stop'

if ($PSEdition -ne 'Core') {
    $bundledPwsh = 'C:\Users\WINDOW XI\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'
    if (-not (Test-Path -LiteralPath $bundledPwsh)) {
        $bundledPwshCommand = Get-Command pwsh -ErrorAction SilentlyContinue
        if ($null -eq $bundledPwshCommand) {
            throw 'A .NET Core PowerShell host with the local Roslyn assemblies is required.'
        }
        $bundledPwsh = $bundledPwshCommand.Source
    }
    & $bundledPwsh -NoLogo -NoProfile -NonInteractive -File $PSCommandPath @args
    exit $LASTEXITCODE
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$roslynRoot = $PSHOME
$roslynPath = Join-Path $roslynRoot 'Microsoft.CodeAnalysis.dll'
$roslynCSharpPath = Join-Path $roslynRoot 'Microsoft.CodeAnalysis.CSharp.dll'
if (-not (Test-Path -LiteralPath $roslynPath) -or -not (Test-Path -LiteralPath $roslynCSharpPath)) {
    throw "Local Roslyn assemblies are unavailable under $roslynRoot"
}

foreach ($assemblyPath in @(
    (Join-Path $roslynRoot 'System.Collections.Immutable.dll'),
    (Join-Path $roslynRoot 'System.Reflection.Metadata.dll'),
    $roslynPath,
    $roslynCSharpPath
)) {
    if (Test-Path -LiteralPath $assemblyPath) {
        Add-Type -Path $assemblyPath
    }
}

$sourceFiles = @(
    Get-ChildItem -File -LiteralPath (Join-Path $PSScriptRoot 'TwinRepair.Core') -Filter '*.cs'
    Get-ChildItem -File -LiteralPath (Join-Path $PSScriptRoot 'TwinRepair.Cli') -Filter '*.cs'
) | Sort-Object FullName

$trees = [Microsoft.CodeAnalysis.SyntaxTree[]]@(
    foreach ($sourceFile in $sourceFiles) {
        $text = [System.IO.File]::ReadAllText($sourceFile.FullName)
        [Microsoft.CodeAnalysis.CSharp.CSharpSyntaxTree]::ParseText(
            $text,
            [Microsoft.CodeAnalysis.CSharp.CSharpParseOptions]::Default.WithLanguageVersion([Microsoft.CodeAnalysis.CSharp.LanguageVersion]::Preview),
            $sourceFile.FullName,
            [System.Text.Encoding]::UTF8)
    }
)

$trustedPlatformAssemblies = [AppContext]::GetData('TRUSTED_PLATFORM_ASSEMBLIES') -split [IO.Path]::PathSeparator
$referencePaths = @($trustedPlatformAssemblies + $roslynPath + $roslynCSharpPath) |
    Where-Object { $_ -and (Test-Path -LiteralPath $_) } |
    Select-Object -Unique
$references = [Microsoft.CodeAnalysis.MetadataReference[]]@(
    foreach ($referencePath in $referencePaths) {
        [Microsoft.CodeAnalysis.MetadataReference]::CreateFromFile($referencePath)
    }
)

$options = [Microsoft.CodeAnalysis.CSharp.CSharpCompilationOptions]::new(
    [Microsoft.CodeAnalysis.OutputKind]::DynamicallyLinkedLibrary)
$compilation = [Microsoft.CodeAnalysis.CSharp.CSharpCompilation]::Create(
    'TwinRepair.Dynamic',
    $trees,
    $references,
    $options)
$diagnostics = @($compilation.GetDiagnostics())
$errors = @($diagnostics | Where-Object { $_.Severity -eq [Microsoft.CodeAnalysis.DiagnosticSeverity]::Error })
if ($errors.Count -gt 0) {
    $errors | Select-Object -First 50 | ForEach-Object { [Console]::Error.WriteLine($_.ToString()) }
    throw "TwinRepair C# compilation failed with $($errors.Count) errors."
}

$assemblyStream = [System.IO.MemoryStream]::new()
$emit = $compilation.Emit([System.IO.Stream]$assemblyStream)
if (-not $emit.Success) {
    $emit.Diagnostics | ForEach-Object { [Console]::Error.WriteLine($_.ToString()) }
    throw 'TwinRepair dynamic assembly emission failed.'
}

$dotnetCommand = Get-Command dotnet -ErrorAction SilentlyContinue
$sdkRows = @()
if ($null -ne $dotnetCommand) {
    $sdkRows = @(& $dotnetCommand.Source --list-sdks 2>$null)
}
$toolchainReport = [ordered]@{
    schema_version = 'r2-toolchain-v1'
    status = 'PASS'
    host = [ordered]@{
        powershell = $PSHOME
        powershell_edition = $PSEdition
        powershell_version = $PSVersionTable.PSVersion.ToString()
        dotnet_host = if ($null -ne $dotnetCommand) { $dotnetCommand.Source } else { $null }
        dotnet_sdk_rows = $sdkRows
    }
    roslyn = [ordered]@{
        microsoft_codeanalysis = $roslynPath
        microsoft_codeanalysis_csharp = $roslynCSharpPath
        assembly_version = ([Microsoft.CodeAnalysis.SyntaxTree].Assembly.GetName().Version.ToString())
        offline_roslyn_compile = $true
        emitted_dynamic_assembly = $true
    }
    network_package_install = $false
    regex_primary_mutation = $false
}
$toolchainPath = Join-Path $repoRoot 'artifacts\r2-reference-twin\reports\r2-toolchain.json'
[System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($toolchainPath)) | Out-Null
[System.IO.File]::WriteAllText($toolchainPath, ($toolchainReport | ConvertTo-Json -Depth 8) + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))
$assemblyStream.Position = 0
$assembly = [System.Runtime.Loader.AssemblyLoadContext]::Default.LoadFromStream($assemblyStream)
$programType = $assembly.GetType('TwinRepair.Cli.Program', $true, $true)
$runMethod = $programType.GetMethod('Run', [Type[]]@([string[]]))
$cliArgs = [string[]]$args
$invokeArgs = [object[]]::new(1)
$invokeArgs[0] = $cliArgs
$exitCode = [int]$runMethod.Invoke($null, $invokeArgs)
exit $exitCode
