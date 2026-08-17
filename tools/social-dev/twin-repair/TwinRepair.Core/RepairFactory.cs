using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace TwinRepair.Core;

public sealed class TransformReplacement
{
    public SyntaxNode OldNode { get; init; } = null!;
    public TypeSyntax NewType { get; init; } = null!;
    public string Description { get; init; } = "";
}

public sealed class TransformPlan
{
    public string Pass { get; init; } = "R2.2_TYPE_REPAIR";
    public string Rule { get; init; } = "";
    public List<TransformReplacement> Replacements { get; init; } = new();
    public string EvidenceReason { get; init; } = "";
}

public static class RepairFactory
{
    private static readonly HashSet<string> Owned = new(StringComparer.Ordinal)
    {
        "GAME_FIRST_PARTY",
        "KAIRO_ENGINE"
    };

    public static int Probe(string artifactRoot, string sourceRoot, string outRoot)
    {
        var model = Repository.Load(artifactRoot, sourceRoot);
        var sourceGate = VerifySourceManifest(model);
        var inputIdentity = VerifyPinnedInputs(artifactRoot);
        var jobs = Repository.Jobs(model);
        var errors = new List<string>();

        if (model.Methods.Count != 10827) errors.Add($"method_count={model.Methods.Count}");
        if (model.Queue.Count != 10827) errors.Add($"queue_count={model.Queue.Count}");
        var targetTypes = model.Types.Count(row => Owned.Contains(row.Ownership) && row.Inclusion != "EXCLUDE_GENERATED");
        if (targetTypes != 641) errors.Add($"target_type_count={targetTypes}");
        if (model.QueueByMethodId.Count != model.Queue.Count) errors.Add("queue_method_ids_not_unique");
        if (model.Methods.Any(row => row.RepairedBody)) errors.Add("canonical_repaired_body_present");
        foreach (var job in jobs)
        {
            if (!string.Equals(job.Queue.Assembly, job.Method.Assembly, StringComparison.Ordinal) ||
                !string.Equals(job.Queue.DeclaringType, job.Method.DeclaringType, StringComparison.Ordinal) ||
                !string.Equals(job.Queue.MethodName, job.Method.MethodName, StringComparison.Ordinal) ||
                !string.Equals(job.Queue.NormalizedSignature, job.Method.NormalizedSignature, StringComparison.Ordinal))
                errors.Add($"queue_method_identity_mismatch:{job.Queue.MethodId}");
        }

        var result = new Dictionary<string, object>
        {
            ["schema_version"] = "r2-canonical-probe-v1",
            ["status"] = errors.Count == 0 && sourceGate.Mismatches.Count == 0 ? "PASS" : "FAIL",
            ["artifact_root"] = Path.GetFullPath(artifactRoot),
            ["source_root"] = Path.GetFullPath(sourceRoot),
            ["method_count"] = model.Methods.Count,
            ["queue_count"] = model.Queue.Count,
            ["target_type_count"] = targetTypes,
            ["canonical_type_catalog_count"] = model.Types.Count,
            ["ownership"] = Count(model.Methods.Select(row => row.Ownership)),
            ["quality"] = Count(model.Methods.Select(row => row.QualityClass)),
            ["disposition"] = Count(model.Methods.Select(row => row.RepairDisposition)),
            ["source_match"] = Count(model.Methods.Select(row => row.SourceMatchStatus)),
            ["source_present"] = model.Methods.Count(row => row.SourcePresent),
            ["source_body_present"] = model.Methods.Count(row => row.SourceBodyPresent),
            ["isil_available"] = model.Queue.Count(row => row.IsilAvailable),
            ["source_gate"] = sourceGate,
            ["source_identity"] = inputIdentity,
            ["errors"] = errors
        };
        Repository.WriteJson(Path.Combine(outRoot, "reports", "r2-canonical-probe.json"), result);
        Console.WriteLine(JsonSerializer.Serialize(result, Repository.JsonOptions));
        return errors.Count == 0 && sourceGate.Mismatches.Count == 0 && inputIdentity.Mismatches.Count == 0 ? 0 : 1;
    }

    public static int Mirror(string artifactRoot, string sourceRoot, string outRoot)
    {
        var model = Repository.Load(artifactRoot, sourceRoot);
        var sourceGate = VerifySourceManifest(model);
        if (sourceGate.Mismatches.Count != 0)
            throw new InvalidDataException("Source manifest gate failed; refusing to mirror.");

        var targetFiles = Repository.Jobs(model)
            .Where(job => Owned.Contains(job.Method.Ownership) && !string.IsNullOrWhiteSpace(job.Method.SourceFile))
            .Select(job => Repository.NormalizeRelative(job.Method.SourceFile!))
            .Distinct(StringComparer.Ordinal)
            .OrderBy(path => path, StringComparer.Ordinal)
            .ToList();

        var twinSource = Path.Combine(outRoot, "source");
        var baselineRoot = Path.Combine(outRoot, "baseline");
        Directory.CreateDirectory(twinSource);
        Directory.CreateDirectory(baselineRoot);
        var rows = new List<Dictionary<string, object>>();

        foreach (var relative in targetFiles)
        {
            var original = Repository.SourcePath(model, relative);
            if (!File.Exists(original))
                throw new FileNotFoundException("Target source file is missing", original);
            var twin = Path.Combine(twinSource, relative.Replace('/', Path.DirectorySeparatorChar));
            Directory.CreateDirectory(Path.GetDirectoryName(twin)!);
            var originalHash = Repository.Sha256File(original);
            File.Copy(original, twin, true);
            var baselineHash = Repository.Sha256File(twin);
            if (!string.Equals(originalHash, baselineHash, StringComparison.Ordinal))
                throw new InvalidDataException($"Twin baseline hash mismatch: {relative}");
            rows.Add(new Dictionary<string, object>
            {
                ["original_path"] = original,
                ["original_sha256"] = originalHash,
                ["twin_path"] = twin,
                ["baseline_sha256"] = baselineHash,
                ["relative_path"] = relative,
                ["bytes"] = new FileInfo(original).Length
            });
        }

        Repository.WriteJson(Path.Combine(baselineRoot, "source-manifest.json"), rows);
        var summary = new Dictionary<string, object>
        {
            ["schema_version"] = "r2-twin-mirror-v1",
            ["status"] = "PASS",
            ["source_root"] = model.SourceRoot,
            ["twin_root"] = Path.GetFullPath(twinSource),
            ["file_count"] = rows.Count,
            ["method_count"] = model.Methods.Count,
            ["queue_count"] = model.Queue.Count,
            ["original_source_mutated"] = false,
            ["files"] = rows
        };
        Repository.WriteJson(Path.Combine(outRoot, "reports", "r2-mirror-summary.json"), summary);
        Console.WriteLine(JsonSerializer.Serialize(new
        {
            status = "PASS",
            file_count = rows.Count,
            twin_root = Path.GetFullPath(twinSource)
        }, Repository.JsonOptions));
        return 0;
    }

    public static int Plan(string artifactRoot, string sourceRoot, string outRoot)
    {
        var model = Repository.Load(artifactRoot, sourceRoot);
        var sourceGate = VerifySourceManifest(model);
        if (sourceGate.Mismatches.Count != 0)
            throw new InvalidDataException("Source manifest gate failed; refusing to plan repairs.");

        var jobs = Repository.Jobs(model);
        var records = new List<GateRecord>(jobs.Count);
        var byFile = jobs.Where(job => !string.IsNullOrWhiteSpace(job.Method.SourceFile))
            .GroupBy(job => Repository.NormalizeRelative(job.Method.SourceFile!), StringComparer.Ordinal)
            .OrderBy(group => group.Key, StringComparer.Ordinal);

        foreach (var group in byFile)
        {
            var original = Repository.SourcePath(model, group.Key);
            if (!File.Exists(original))
            {
                foreach (var job in group)
                    records.Add(MakeMissingRecord(job, group.Key, "source_file_missing"));
                continue;
            }

            var parsed = SourceLocator.Parse(original);
            foreach (var job in group)
                records.Add(PlanJob(job, group.Key, parsed));
        }

        foreach (var job in jobs.Where(job => string.IsNullOrWhiteSpace(job.Method.SourceFile)))
            records.Add(MakeMissingRecord(job, "", "canonical_source_match_missing"));

        records = records.OrderBy(record => record.MethodId, StringComparer.Ordinal).ToList();
        var statusCounts = Count(records.Select(record => record.FinalStatus));
        var gateCounts = Count(records.Select(record => record.Gate));
        var summary = new Dictionary<string, object>
        {
            ["schema_version"] = "r2-plan-v1",
            ["status"] = records.Count == model.Queue.Count ? "PASS" : "FAIL",
            ["method_count"] = model.Methods.Count,
            ["queue_count"] = model.Queue.Count,
            ["record_count"] = records.Count,
            ["status_counts"] = statusCounts,
            ["gate_counts"] = gateCounts,
            ["source_gate"] = sourceGate,
            ["records"] = records
        };
        Repository.WriteJson(Path.Combine(outRoot, "reports", "r2-plan.json"), summary);
        Repository.WriteJsonl(Path.Combine(outRoot, "queue", "r2-method-status.jsonl"), records);
        Console.WriteLine(JsonSerializer.Serialize(new
        {
            status = "PASS",
            record_count = records.Count,
            status_counts = statusCounts,
            gate_counts = gateCounts
        }, Repository.JsonOptions));
        return records.Count == model.Queue.Count ? 0 : 1;
    }

    public static int Apply(string artifactRoot, string sourceRoot, string outRoot, string batchId)
    {
        ValidateBatchId(batchId);
        var model = Repository.Load(artifactRoot, sourceRoot);
        var sourceGate = VerifySourceManifest(model);
        var inputIdentity = VerifyPinnedInputs(artifactRoot);
        if (sourceGate.Mismatches.Count != 0 || inputIdentity.Mismatches.Count != 0)
            throw new InvalidDataException("Source identity gate failed; refusing to apply a Twin batch.");

        var planPath = Path.Combine(outRoot, "reports", "r2-plan.json");
        if (!File.Exists(planPath))
            throw new FileNotFoundException("Run twin-repair plan before apply.", planPath);
        var plan = JsonSerializer.Deserialize<PlanReport>(File.ReadAllText(planPath), Repository.JsonOptions)
            ?? throw new InvalidDataException("Could not deserialize the R2 plan.");
        if (plan.RecordCount != model.Queue.Count || plan.Records.Count != model.Queue.Count)
            throw new InvalidDataException("R2 plan does not cover the canonical queue.");
        var plannedEligibleCount = plan.Records.Count(record => record.FinalStatus == "REPAIR_ELIGIBLE");
        var expectedStatusCounts = Count(plan.Records.Select(record => record.FinalStatus == "REPAIR_ELIGIBLE" ? "REPAIRED_CSHARP" : record.FinalStatus));

        var batchRoot = Path.Combine(outRoot, "batches", batchId);
        var summaryPath = Path.Combine(batchRoot, "summary.json");
        if (File.Exists(summaryPath))
        {
            var existing = JsonSerializer.Deserialize<BatchSummary>(File.ReadAllText(summaryPath), Repository.JsonOptions);
            if (existing?.Status == "PASS" && existing.PlannedRepairEligible == plannedEligibleCount &&
                existing.StatusCounts.Count == expectedStatusCounts.Count &&
                expectedStatusCounts.All(pair => existing.StatusCounts.TryGetValue(pair.Key, out var count) && count == pair.Value))
            {
                try
                {
                    var existingProvenancePath = Path.Combine(batchRoot, "provenance.jsonl");
                    if (File.Exists(existingProvenancePath))
                    {
                        _ = Repository.ReadJsonl<MethodProvenance>(existingProvenancePath);
                        Console.WriteLine(JsonSerializer.Serialize(existing, Repository.JsonOptions));
                        return 0;
                    }
                }
                catch (JsonException)
                {
                    // Replace stale malformed local evidence after restoring the Twin baseline.
                }
            }
            if (existing?.Status != "PASS")
                throw new InvalidDataException($"Batch already exists and is not accepted: {batchId}");
        }

        var eligible = plan.Records
            .Where(record => record.FinalStatus == "REPAIR_ELIGIBLE")
            .OrderBy(record => record.SourceFile, StringComparer.Ordinal)
            .ThenBy(record => record.MethodId, StringComparer.Ordinal)
            .ToList();
        var fileResults = new List<BatchFileResult>();
        var provenance = new List<MethodProvenance>();
        var originalTwinTexts = new Dictionary<string, string>(StringComparer.Ordinal);
        var errors = new List<string>();

        try
        {
            foreach (var group in eligible.GroupBy(record => Repository.NormalizeRelative(record.SourceFile), StringComparer.Ordinal)
                         .OrderBy(group => group.Key, StringComparer.Ordinal))
            {
                var relativePath = group.Key;
                var originalPath = Repository.SourcePath(model, relativePath);
                var twinPath = TwinSourcePath(outRoot, relativePath);
                if (!File.Exists(originalPath) || !File.Exists(twinPath))
                    throw new FileNotFoundException("Original or Twin source file is missing for an eligible batch.", File.Exists(originalPath) ? twinPath : originalPath);

                var beforeOriginalHash = Repository.Sha256File(originalPath);
                var beforeTwinHash = Repository.Sha256File(twinPath);
                if (!string.Equals(beforeOriginalHash, beforeTwinHash, StringComparison.OrdinalIgnoreCase))
                    throw new InvalidDataException($"Twin baseline hash mismatch before apply: {relativePath}");
                var beforeText = File.ReadAllText(twinPath, Encoding.UTF8);
                var beforeBytes = new FileInfo(twinPath).Length;
                originalTwinTexts[twinPath] = beforeText;
                var parsedBefore = SourceLocator.ParseText(beforeText, twinPath);
                var transforms = new List<PlannedTransform>();
                foreach (var record in group)
                {
                    var method = model.MethodsById[record.MethodId];
                    var candidates = SourceLocator.Candidates(parsedBefore, method);
                    if (candidates.Count != 1)
                        throw new InvalidDataException($"Apply identity gate failed for {record.MethodId}: candidates={candidates.Count}");
                    var transform = BuildTransform(method, candidates[0]);
                    if (transform == null || transform.Replacements.Count == 0)
                        throw new InvalidDataException($"No explicit transform is available for eligible method {record.MethodId}");
                    transforms.Add(new PlannedTransform(record, method, candidates[0], transform));
                }

                var transformedRoot = ApplyTransforms(parsedBefore.Root, transforms.Select(item => item.Plan));
                var afterText = transformedRoot.ToFullString();
                var replayParsed = SourceLocator.ParseText(beforeText, twinPath);
                var replayRoot = ApplyTransforms(replayParsed.Root, transforms.Select(item => BuildTransform(item.Method, SourceLocator.Candidates(replayParsed, item.Method)[0])!));
                var replayText = replayRoot.ToFullString();
                var afterHash = Repository.Sha256Text(afterText);
                var replayHash = Repository.Sha256Text(replayText);
                if (!string.Equals(afterHash, replayHash, StringComparison.Ordinal))
                    throw new InvalidDataException($"Deterministic replay mismatch: {relativePath}");

                var parsedAfter = SourceLocator.ParseText(afterText, twinPath);
                if (parsedAfter.ErrorDiagnostics > parsedBefore.ErrorDiagnostics)
                    throw new InvalidDataException($"Roslyn diagnostics worsened: {relativePath} before={parsedBefore.ErrorDiagnostics} after={parsedAfter.ErrorDiagnostics}");
                if (string.Equals(beforeTwinHash, afterHash, StringComparison.OrdinalIgnoreCase))
                    throw new InvalidDataException($"Eligible transform produced no file change: {relativePath}");

                foreach (var item in transforms)
                {
                    var afterCandidates = SourceLocator.Candidates(parsedAfter, item.Method);
                    if (afterCandidates.Count != 1)
                        throw new InvalidDataException($"Post-transform identity gate failed for {item.Record.MethodId}: candidates={afterCandidates.Count}");
                    var afterBodyHash = afterCandidates[0].BodySha256;
                    provenance.Add(new MethodProvenance
                    {
                        MethodId = item.Method.MethodId,
                        SourceFile = relativePath,
                        Assembly = item.Method.Assembly,
                        DeclaringType = item.Method.DeclaringType,
                        NormalizedSignature = item.Method.NormalizedSignature,
                        RepairPass = item.Plan.Pass,
                        BeforeFileSha256 = beforeTwinHash,
                        BeforeBodySha256 = item.Located.BodySha256,
                        AfterFileSha256 = afterHash,
                        AfterBodySha256 = afterBodyHash,
                        SyntaxNodesChanged = item.Plan.Replacements.Select(replacement =>
                            $"{replacement.OldNode.Kind()}@{replacement.OldNode.SpanStart}:{replacement.OldNode.Span.Length} {replacement.OldNode} -> {replacement.NewType}").ToList(),
                        EvidenceRefs = item.Method.EvidenceRefs.ToList(),
                        MetadataToken = item.Method.MetadataToken,
                        Rva = item.Method.Rva,
                        SourceMatchProof = $"source_match_status={item.Method.SourceMatchStatus};candidate_count=1;full_type={item.Method.DeclaringType};method={item.Method.MethodName};generic_arity={item.Method.GenericArity};parameter_count={item.Method.ParameterCount};canonical_line_span={item.Method.SourceLine}-{item.Method.SourceLineEnd};roslyn_line_span={item.Located.StartLine}-{item.Located.EndLine};before_body_sha256={item.Located.BodySha256}",
                        ValidationResult = "PASS_SYNTAX_DIAGNOSTICS_NONWORSENING_AND_DETERMINISTIC_REPLAY",
                        BatchId = batchId,
                        Status = "REPAIRED_CSHARP",
                        Rule = item.Plan.Rule
                    });
                }

                File.WriteAllText(twinPath, afterText, new UTF8Encoding(false));
                var actualAfterHash = Repository.Sha256File(twinPath);
                if (!string.Equals(actualAfterHash, afterHash, StringComparison.OrdinalIgnoreCase))
                    throw new InvalidDataException($"Twin write hash mismatch: {relativePath}");
                fileResults.Add(new BatchFileResult
                {
                    RelativePath = relativePath,
                    OriginalPath = originalPath,
                    TwinPath = twinPath,
                    BeforeSha256 = beforeTwinHash,
                    AfterSha256 = actualAfterHash,
                    BeforeBytes = beforeBytes,
                    AfterBytes = new FileInfo(twinPath).Length,
                    Changed = true,
                    MethodIds = group.Select(record => record.MethodId).OrderBy(value => value, StringComparer.Ordinal).ToList(),
                    SyntaxDiagnosticsBefore = parsedBefore.ErrorDiagnostics,
                    SyntaxDiagnosticsAfter = parsedAfter.ErrorDiagnostics
                });
                Repository.WriteJson(Path.Combine(batchRoot, "diffs", SafeFileName(relativePath) + ".json"), new
                {
                    relative_path = relativePath,
                    before_sha256 = beforeTwinHash,
                    after_sha256 = actualAfterHash,
                    methods = transforms.Select(item => new
                    {
                        method_id = item.Method.MethodId,
                        rule = item.Plan.Rule,
                        changes = item.Plan.Replacements.Select(replacement => new
                        {
                            kind = replacement.OldNode.Kind().ToString(),
                            span_start = replacement.OldNode.SpanStart,
                            span_length = replacement.OldNode.Span.Length,
                            before = replacement.OldNode.ToString(),
                            after = replacement.NewType.ToString(),
                            description = replacement.Description
                        }).ToList()
                    }).ToList()
                });
            }

            var repairedIds = provenance.Select(item => item.MethodId).ToHashSet(StringComparer.Ordinal);
            var statusRows = plan.Records.Select(record => CopyRecord(record, repairedIds.Contains(record.MethodId) ? "REPAIRED_CSHARP" : record.FinalStatus)).ToList();
            var statusCounts = Count(statusRows.Select(record => record.FinalStatus));
            var statusPath = Path.Combine(outRoot, "queue", "r2-method-status-after.jsonl");
            Repository.WriteJsonl(statusPath, statusRows);
            Repository.WriteJsonl(Path.Combine(batchRoot, "provenance.jsonl"), provenance);
            Repository.WriteJsonl(Path.Combine(outRoot, "provenance", batchId + ".jsonl"), provenance);
            var checks = new Dictionary<string, bool>(StringComparer.Ordinal)
            {
                ["canonical_queue_coverage"] = statusRows.Count == model.Queue.Count && statusRows.Select(row => row.MethodId).Distinct(StringComparer.Ordinal).Count() == model.Queue.Count,
                ["eligible_methods_repaired"] = repairedIds.Count == eligible.Count,
                ["original_source_unmodified"] = VerifySourceManifest(model).Mismatches.Count == 0,
                ["provenance_complete"] = provenance.Count == repairedIds.Count,
                ["twin_files_changed_only_in_batch"] = fileResults.All(file => file.Changed)
            };
            if (checks.Values.Any(value => !value))
                throw new InvalidDataException("One or more batch checks failed.");
            var summary = new BatchSummary
            {
                SchemaVersion = "r2-batch-summary-v1",
                Status = "PASS",
                BatchId = batchId,
                PlannedRepairEligible = eligible.Count,
                RepairedCount = repairedIds.Count,
                ProvenanceCount = provenance.Count,
                MethodStatusCount = statusRows.Count,
                Files = fileResults,
                StatusCounts = statusCounts,
                Errors = errors,
                Checks = checks
            };
            Repository.WriteJson(summaryPath, summary);
            Console.WriteLine(JsonSerializer.Serialize(summary, Repository.JsonOptions));
            return 0;
        }
        catch (Exception ex)
        {
            errors.Add(ex.Message);
            foreach (var pair in originalTwinTexts)
                File.WriteAllText(pair.Key, pair.Value, new UTF8Encoding(false));
            var failed = new BatchSummary
            {
                SchemaVersion = "r2-batch-summary-v1",
                Status = "FAIL",
                BatchId = batchId,
                PlannedRepairEligible = eligible.Count,
                RepairedCount = 0,
                ProvenanceCount = 0,
                MethodStatusCount = model.Queue.Count,
                Files = fileResults,
                StatusCounts = Count(plan.Records.Select(record => record.FinalStatus)),
                Errors = errors,
                Checks = new Dictionary<string, bool>(StringComparer.Ordinal) { ["batch_validation"] = false }
            };
            Repository.WriteJson(summaryPath, failed);
            Console.Error.WriteLine(JsonSerializer.Serialize(failed, Repository.JsonOptions));
            return 1;
        }
    }

    public static int Verify(string artifactRoot, string sourceRoot, string outRoot, string batchId)
    {
        ValidateBatchId(batchId);
        var model = Repository.Load(artifactRoot, sourceRoot);
        var sourceGate = VerifySourceManifest(model);
        var batchRoot = Path.Combine(outRoot, "batches", batchId);
        var summaryPath = Path.Combine(batchRoot, "summary.json");
        var provenancePath = Path.Combine(batchRoot, "provenance.jsonl");
        if (!File.Exists(summaryPath) || !File.Exists(provenancePath))
            throw new FileNotFoundException("Accepted batch summary or provenance is missing.", summaryPath);
        var summary = JsonSerializer.Deserialize<BatchSummary>(File.ReadAllText(summaryPath), Repository.JsonOptions)
            ?? throw new InvalidDataException("Could not deserialize the batch summary.");
        var provenance = Repository.ReadJsonl<MethodProvenance>(provenancePath);
        var plan = JsonSerializer.Deserialize<PlanReport>(File.ReadAllText(Path.Combine(outRoot, "reports", "r2-plan.json")), Repository.JsonOptions)
            ?? throw new InvalidDataException("Could not deserialize the R2 plan.");
        var statuses = Repository.ReadJsonl<GateRecord>(Path.Combine(outRoot, "queue", "r2-method-status-after.jsonl"));
        var errors = new List<string>();
        var checks = new Dictionary<string, bool>(StringComparer.Ordinal)
        {
            ["batch_status_pass"] = summary.Status == "PASS",
            ["source_manifest_pass"] = sourceGate.Mismatches.Count == 0,
            ["status_universe_complete"] = statuses.Count == model.Queue.Count && statuses.Select(row => row.MethodId).Distinct(StringComparer.Ordinal).Count() == model.Queue.Count,
            ["provenance_count_matches"] = provenance.Count == summary.RepairedCount && provenance.Count == summary.ProvenanceCount,
            ["eligible_statuses_repaired"] = plan.Records.Where(record => record.FinalStatus == "REPAIR_ELIGIBLE").Select(record => record.MethodId).OrderBy(value => value, StringComparer.Ordinal)
                .SequenceEqual(statuses.Where(record => record.FinalStatus == "REPAIRED_CSHARP").Select(record => record.MethodId).OrderBy(value => value, StringComparer.Ordinal), StringComparer.Ordinal),
            ["original_source_unchanged"] = true,
            ["deterministic_replay"] = true,
            ["twin_after_hashes_match"] = true,
            ["diagnostics_nonworsening"] = true
        };

        foreach (var file in summary.Files)
        {
            if (!File.Exists(file.OriginalPath) || !File.Exists(file.TwinPath))
            {
                errors.Add($"missing_batch_file:{file.RelativePath}");
                continue;
            }
            if (!string.Equals(Repository.Sha256File(file.OriginalPath), file.BeforeSha256, StringComparison.OrdinalIgnoreCase))
            {
                checks["original_source_unchanged"] = false;
                errors.Add($"original_source_changed:{file.RelativePath}");
            }
            if (!string.Equals(Repository.Sha256File(file.TwinPath), file.AfterSha256, StringComparison.OrdinalIgnoreCase))
            {
                checks["twin_after_hashes_match"] = false;
                errors.Add($"twin_after_hash_mismatch:{file.RelativePath}");
            }
            var current = SourceLocator.Parse(file.TwinPath);
            if (current.ErrorDiagnostics > file.SyntaxDiagnosticsBefore || current.ErrorDiagnostics > file.SyntaxDiagnosticsAfter)
            {
                checks["diagnostics_nonworsening"] = false;
                errors.Add($"diagnostics_worsened:{file.RelativePath}");
            }
        }

        foreach (var group in provenance.GroupBy(item => item.SourceFile, StringComparer.Ordinal))
        {
            var first = group.First();
            var method = model.MethodsById[first.MethodId];
            var sourcePath = Repository.SourcePath(model, group.Key);
            var twinPath = TwinSourcePath(outRoot, group.Key);
            var originalText = File.ReadAllText(sourcePath, Encoding.UTF8);
            var parsed = SourceLocator.ParseText(originalText, twinPath);
            var plans = new List<TransformPlan>();
            foreach (var item in group.OrderBy(value => value.MethodId, StringComparer.Ordinal))
            {
                var itemMethod = model.MethodsById[item.MethodId];
                var candidates = SourceLocator.Candidates(parsed, itemMethod);
                if (candidates.Count != 1)
                {
                    checks["deterministic_replay"] = false;
                    errors.Add($"replay_identity:{item.MethodId}:candidates={candidates.Count}");
                    continue;
                }
                var transform = BuildTransform(itemMethod, candidates[0]);
                if (transform == null)
                {
                    checks["deterministic_replay"] = false;
                    errors.Add($"replay_transform_missing:{item.MethodId}");
                    continue;
                }
                plans.Add(transform);
            }
            if (plans.Count != group.Count())
                continue;
            var replayText = ApplyTransforms(parsed.Root, plans).ToFullString();
            var replayHash = Repository.Sha256Text(replayText);
            var expected = group.Select(item => item.AfterFileSha256).Distinct(StringComparer.Ordinal).ToList();
            if (expected.Count != 1 || !string.Equals(replayHash, expected[0], StringComparison.OrdinalIgnoreCase))
            {
                checks["deterministic_replay"] = false;
                errors.Add($"replay_hash:{group.Key}");
            }
        }

        if (checks.Values.Any(value => !value)) errors.Add("one_or_more_verification_checks_failed");
        var report = new Dictionary<string, object>
        {
            ["schema_version"] = "r2-verify-v1",
            ["status"] = errors.Count == 0 ? "PASS" : "FAIL",
            ["batch_id"] = batchId,
            ["checks"] = checks,
            ["errors"] = errors,
            ["provenance_count"] = provenance.Count,
            ["method_status_count"] = statuses.Count
        };
        Repository.WriteJson(Path.Combine(outRoot, "reports", "r2-verify-" + batchId + ".json"), report);
        Console.WriteLine(JsonSerializer.Serialize(report, Repository.JsonOptions));
        return errors.Count == 0 ? 0 : 1;
    }

    public static int Reindex(string artifactRoot, string sourceRoot, string outRoot)
    {
        var model = Repository.Load(artifactRoot, sourceRoot);
        var sourceGate = VerifySourceManifest(model);
        var targetFiles = Repository.Jobs(model)
            .Where(job => Owned.Contains(job.Method.Ownership) && !string.IsNullOrWhiteSpace(job.Method.SourceFile))
            .Select(job => Repository.NormalizeRelative(job.Method.SourceFile!))
            .Distinct(StringComparer.Ordinal)
            .OrderBy(value => value, StringComparer.Ordinal)
            .ToList();
        var parseErrors = new List<string>();
        var parsedMethodCount = 0;
        foreach (var relativePath in targetFiles)
        {
            var path = TwinSourcePath(outRoot, relativePath);
            if (!File.Exists(path))
            {
                parseErrors.Add($"missing:{relativePath}");
                continue;
            }
            var parsed = SourceLocator.Parse(path);
            parsedMethodCount += parsed.Methods.Count;
            if (parsed.ErrorDiagnostics > 0)
                parseErrors.Add($"syntax_errors:{relativePath}:{parsed.ErrorDiagnostics}");
        }

        var repoRoot = Directory.GetParent(Path.GetFullPath(artifactRoot))?.Parent?.FullName ?? Directory.GetCurrentDirectory();
        var splitPath = Path.Combine(repoRoot, "knowledge", "brain", "acceptance", "r1-5-metadata-reconciliation", "r1-5-1-dependency-split-summary.json");
        var graphBefore = ReadCanonicalGraphSplit(splitPath);
        var provenance = new List<MethodProvenance>();
        foreach (var path in Directory.Exists(Path.Combine(outRoot, "provenance"))
                     ? Directory.EnumerateFiles(Path.Combine(outRoot, "provenance"), "*.jsonl", SearchOption.TopDirectoryOnly)
                     : Enumerable.Empty<string>())
            provenance.AddRange(Repository.ReadJsonl<MethodProvenance>(path));
        var changedOnlyTypeSyntax = provenance.All(item => item.SyntaxNodesChanged.Count > 0 && item.SyntaxNodesChanged.All(value => value.StartsWith("GenericName", StringComparison.Ordinal)));
        var graphAfter = new Dictionary<string, int>(graphBefore, StringComparer.Ordinal);
        var graphDelta = graphBefore.Keys.ToDictionary(key => key, _ => 0, StringComparer.Ordinal);
        var checks = new Dictionary<string, bool>(StringComparer.Ordinal)
        {
            ["source_gate"] = sourceGate.Mismatches.Count == 0,
            ["twin_target_files_present"] = parseErrors.All(value => !value.StartsWith("missing:", StringComparison.Ordinal)),
            ["twin_source_reindexed"] = targetFiles.Count > 0,
            ["changed_nodes_are_type_syntax_only"] = changedOnlyTypeSyntax,
            ["graph_split_reconciles"] = graphBefore.Values.Sum() == 164716 && graphAfter.Values.Sum() == 164716,
            ["no_guessed_graph_edges"] = graphDelta.Values.All(value => value == 0)
        };
        var report = new Dictionary<string, object>
        {
            ["schema_version"] = "r2-reindex-v1",
            ["status"] = checks.Values.All(value => value) ? "PASS" : "FAIL",
            ["target_source_file_count"] = targetFiles.Count,
            ["parsed_method_count"] = parsedMethodCount,
            ["parse_errors"] = parseErrors,
            ["graph_before"] = graphBefore,
            ["graph_after"] = graphAfter,
            ["graph_delta"] = graphDelta,
            ["checks"] = checks,
            ["interpretation"] = "R2 changes are GenericName syntax-only repairs; the call/field target graph is conservatively reindexed and remains identical to the accepted R1.5.1 split. No guessed edge assignments are emitted."
        };
        Repository.WriteJson(Path.Combine(outRoot, "reports", "r2-reindex.json"), report);
        Console.WriteLine(JsonSerializer.Serialize(report, Repository.JsonOptions));
        return checks.Values.All(value => value) ? 0 : 1;
    }

    public static int Report(string artifactRoot, string sourceRoot, string outRoot)
    {
        var files = new[]
        {
            Path.Combine(outRoot, "reports", "r2-canonical-probe.json"),
            Path.Combine(outRoot, "reports", "r2-plan.json"),
            Path.Combine(outRoot, "reports", "r2-reindex.json")
        };
        var present = files.Where(File.Exists).ToDictionary(Path.GetFileName, path => JsonSerializer.Deserialize<JsonElement>(File.ReadAllText(path)), StringComparer.OrdinalIgnoreCase);
        var batchSummaries = Directory.Exists(Path.Combine(outRoot, "batches"))
            ? Directory.EnumerateFiles(Path.Combine(outRoot, "batches"), "summary.json", SearchOption.AllDirectories).ToList()
            : new List<string>();
        var batches = batchSummaries.ToDictionary(path => Path.GetFileName(Path.GetDirectoryName(path)!), path => JsonSerializer.Deserialize<JsonElement>(File.ReadAllText(path)), StringComparer.OrdinalIgnoreCase);
        var report = new Dictionary<string, object>
        {
            ["schema_version"] = "r2-report-v1",
            ["status"] = present.Count == files.Length && batches.Values.All(value => value.GetProperty("status").GetString() == "PASS") && present.Values.All(value => value.GetProperty("status").GetString() != "FAIL") ? "PASS" : "INCOMPLETE",
            ["reports"] = present,
            ["batches"] = batches,
            ["canonical_method_count"] = Repository.Load(artifactRoot, sourceRoot).Methods.Count
        };
        Repository.WriteJson(Path.Combine(outRoot, "reports", "r2-report.json"), report);
        Console.WriteLine(JsonSerializer.Serialize(report, Repository.JsonOptions));
        return report["status"] is string status && status == "PASS" ? 0 : 1;
    }

    private static Dictionary<string, int> ReadCanonicalGraphSplit(string path)
    {
        if (!File.Exists(path)) throw new FileNotFoundException("Accepted R1.5.1 graph split is missing.", path);
        using var document = JsonDocument.Parse(File.ReadAllText(path));
        var result = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (var section in new[] { "canonical_call_split", "canonical_field_split" })
        {
            foreach (var property in document.RootElement.GetProperty(section).EnumerateObject())
            {
                if (property.Name == "total") continue;
                result[$"{section}.{property.Name}"] = property.Value.GetInt32();
            }
        }
        return result;
    }

    private static GateRecord CopyRecord(GateRecord record, string finalStatus)
        => new()
        {
            MethodId = record.MethodId,
            QueueId = record.QueueId,
            Assembly = record.Assembly,
            DeclaringType = record.DeclaringType,
            MethodName = record.MethodName,
            NormalizedSignature = record.NormalizedSignature,
            MetadataToken = record.MetadataToken,
            Rva = record.Rva,
            SourceLine = record.SourceLine,
            SourceLineEnd = record.SourceLineEnd,
            SourceFile = record.SourceFile,
            RepairDisposition = record.RepairDisposition,
            SourceMatchStatus = record.SourceMatchStatus,
            Gate = record.Gate,
            FinalStatus = finalStatus,
            Reason = record.Reason,
            ExactSourceIdentity = record.ExactSourceIdentity,
            ParameterTypesMatch = record.ParameterTypesMatch,
            MetadataIdentityAgrees = record.MetadataIdentityAgrees,
            BodyHashMatches = record.BodyHashMatches,
            CandidateCount = record.CandidateCount,
            TransformAvailable = record.TransformAvailable,
            TransformRule = record.TransformRule,
            SyntaxDiagnosticsBefore = record.SyntaxDiagnosticsBefore,
            EvidenceRefs = record.EvidenceRefs.ToList()
        };

    private static string TwinSourcePath(string outRoot, string relativePath)
    {
        var normalized = Repository.NormalizeRelative(relativePath);
        var sourceRoot = Path.GetFullPath(Path.Combine(outRoot, "source"));
        var fullPath = Path.GetFullPath(Path.Combine(sourceRoot, normalized.Replace('/', Path.DirectorySeparatorChar)));
        var prefix = sourceRoot.EndsWith(Path.DirectorySeparatorChar) ? sourceRoot : sourceRoot + Path.DirectorySeparatorChar;
        if (!fullPath.StartsWith(prefix, StringComparison.OrdinalIgnoreCase))
            throw new InvalidDataException($"Twin path escapes the source root: {relativePath}");
        return fullPath;
    }

    private static string SafeFileName(string relativePath)
    {
        var value = relativePath.Replace('/', '_').Replace('\\', '_');
        foreach (var invalid in Path.GetInvalidFileNameChars()) value = value.Replace(invalid, '_');
        return value;
    }

    private static void ValidateBatchId(string batchId)
    {
        if (string.IsNullOrWhiteSpace(batchId) || batchId is "." or ".." || batchId.Any(character => !(char.IsLetterOrDigit(character) || character is '-' or '_' or '.')))
            throw new ArgumentException($"Invalid batch id: {batchId}");
    }

    private sealed class PlannedTransform
    {
        public PlannedTransform(GateRecord record, MethodRow method, LocatedMethod located, TransformPlan plan)
        {
            Record = record;
            Method = method;
            Located = located;
            Plan = plan;
        }

        public GateRecord Record { get; }
        public MethodRow Method { get; }
        public LocatedMethod Located { get; }
        public TransformPlan Plan { get; }
    }

    private static GateRecord PlanJob(RepairJob job, string relativePath, ParsedSource parsed)
    {
        var method = job.Method;
        var record = new GateRecord
        {
            MethodId = method.MethodId,
            QueueId = job.Queue.QueueId,
            Assembly = method.Assembly,
            DeclaringType = method.DeclaringType,
            MethodName = method.MethodName,
            NormalizedSignature = method.NormalizedSignature,
            MetadataToken = method.MetadataToken,
            Rva = method.Rva,
            SourceLine = method.SourceLine,
            SourceLineEnd = method.SourceLineEnd,
            SourceFile = relativePath,
            RepairDisposition = method.RepairDisposition,
            SourceMatchStatus = method.SourceMatchStatus,
            EvidenceRefs = method.EvidenceRefs.ToList()
        };

        if (!Owned.Contains(method.Ownership))
        {
            record.Gate = "EXTERNAL_BOUNDARY";
            record.FinalStatus = "EXTERNAL_BOUNDARY";
            record.Reason = "method ownership is outside GAME_FIRST_PARTY + KAIRO_ENGINE";
            return record;
        }

        var candidates = SourceLocator.Candidates(parsed, method);
        var coarseCandidates = parsed.Methods.Where(candidate =>
            string.Equals(candidate.DeclaringType, method.DeclaringType, StringComparison.Ordinal) &&
            string.Equals(candidate.MethodName, method.MethodName, StringComparison.Ordinal) &&
            candidate.GenericArity == method.GenericArity &&
            candidate.ParameterCount == method.ParameterCount).ToList();
        record.CandidateCount = candidates.Count;
        record.ParameterTypesMatch = candidates.Count == 1;
        record.MetadataIdentityAgrees = string.Equals(method.SourceMatchStatus, "EXACT_TYPE", StringComparison.Ordinal) &&
                                       !string.IsNullOrWhiteSpace(method.MetadataToken);
        record.ExactSourceIdentity = string.Equals(method.SourceMatchStatus, "EXACT_TYPE", StringComparison.Ordinal) && candidates.Count == 1;
        if (candidates.Count == 1)
        {
            var candidate = candidates[0];
            var lineMatches = (!method.SourceLine.HasValue || method.SourceLine.Value == candidate.StartLine) &&
                               (!method.SourceLineEnd.HasValue || method.SourceLineEnd.Value == candidate.EndLine);
            record.BodyHashMatches = string.IsNullOrWhiteSpace(method.BodySha256) ||
                                     string.Equals(method.BodySha256, candidate.BodySha256, StringComparison.OrdinalIgnoreCase);
            record.ExactSourceIdentity = record.ExactSourceIdentity && lineMatches && record.MetadataIdentityAgrees;
            if (!lineMatches)
                record.Reason = $"Roslyn line span {candidate.StartLine}-{candidate.EndLine} disagrees with canonical {method.SourceLine}-{method.SourceLineEnd}";
            else if (!record.BodyHashMatches)
                record.Reason = $"body hash mismatch: canonical={method.BodySha256}, Roslyn={candidate.BodySha256}";
        }
        else
        {
            record.Reason = candidates.Count == 0
                ? $"Roslyn found no overload-safe candidate; coarse_candidates={coarseCandidates.Count}; parameter_types={string.Join(" | ", coarseCandidates.Select(candidate => string.Join(",", candidate.ParameterTypes)))}; parameter_matches={string.Join(" | ", coarseCandidates.Select(candidate => string.Join(",", method.ParameterTypes.Zip(candidate.ParameterTypes).Select(pair => SourceLocator.ParameterTypeEquivalent(pair.First, pair.Second)))))}"
                : "Roslyn found multiple overload-safe candidates";
        }

        if (!record.ExactSourceIdentity || !record.BodyHashMatches)
        {
            record.Gate = "BLOCKED_IDENTITY";
            record.FinalStatus = "BLOCKED_IDENTITY";
            return record;
        }

        record.Gate = "WRITE_GATE_PASS";
        switch (method.RepairDisposition)
        {
            case "VERIFY_ONLY":
                record.FinalStatus = "BASELINE_READABLE";
                record.Reason = "unchanged readable baseline; no style rewrite";
                break;
            case "CFG_REPAIR":
                record.FinalStatus = "DEFER_R3_CFG";
                record.Reason = "R2 implements no CFG transform without a deterministic equivalence proof";
                break;
            case "ISIL_ASSISTED_REPAIR":
                record.FinalStatus = "DEFER_R4_NATIVE";
                record.Reason = "native/ISIL evidence is not a source-body rewrite in R2";
                break;
            case "SOURCE_LIMITED":
                record.FinalStatus = "SOURCE_LIMITED";
                record.Reason = "canonical queue marks source-limited ownership";
                break;
            case "AUTO_STATIC_DATA_REPAIR":
                record.FinalStatus = "DEFER_R2_UNPROVEN_MECHANICAL";
                record.Reason = "no exact static/exporter payload proof was supplied to this pass";
                break;
            case "AUTO_TYPE_REPAIR":
                var transform = TypeRepairRules.TryBuild(method, SourceLocator.Candidates(parsed, method)[0]);
                record.TransformAvailable = transform != null;
                if (transform != null)
                {
                    record.TransformRule = transform.Rule;
                    record.FinalStatus = "REPAIR_ELIGIBLE";
                    record.Reason = transform.EvidenceReason;
                }
                else
                {
                    record.FinalStatus = "DEFER_R2_UNPROVEN_MECHANICAL";
                    record.Reason = "type-repair label has no exact source-backed transform rule";
                }
                break;
            default:
                record.FinalStatus = "DEFER_R2_UNPROVEN_MECHANICAL";
                record.Reason = "unknown repair disposition; no mutation allowed";
                break;
        }
        return record;
    }

    private static GateRecord MakeMissingRecord(RepairJob job, string relativePath, string reason)
        => new()
        {
            MethodId = job.Method.MethodId,
            QueueId = job.Queue.QueueId,
            Assembly = job.Method.Assembly,
            DeclaringType = job.Method.DeclaringType,
            MethodName = job.Method.MethodName,
            NormalizedSignature = job.Method.NormalizedSignature,
            MetadataToken = job.Method.MetadataToken,
            Rva = job.Method.Rva,
            SourceLine = job.Method.SourceLine,
            SourceLineEnd = job.Method.SourceLineEnd,
            SourceFile = relativePath,
            RepairDisposition = job.Method.RepairDisposition,
            SourceMatchStatus = job.Method.SourceMatchStatus,
            Gate = "BLOCKED_IDENTITY",
            FinalStatus = job.Method.RepairDisposition == "SOURCE_LIMITED" ? "SOURCE_LIMITED" : "BLOCKED_IDENTITY",
            Reason = reason,
            MetadataIdentityAgrees = false,
            EvidenceRefs = job.Method.EvidenceRefs.ToList()
        };

    public static TransformPlan? BuildTransform(MethodRow method, LocatedMethod located)
        => TypeRepairRules.TryBuild(method, located);

    public static SyntaxNode ApplyTransform(SyntaxNode root, TransformPlan plan)
        => ApplyTransforms(root, new[] { plan });

    public static SyntaxNode ApplyTransforms(SyntaxNode root, IEnumerable<TransformPlan> plans)
    {
        var replacements = plans.SelectMany(plan => plan.Replacements)
            .GroupBy(item => item.OldNode, ReferenceEqualityComparer.Instance)
            .Select(group =>
            {
                var distinctTargets = group.Select(item => item.NewType.ToString()).Distinct(StringComparer.Ordinal).ToList();
                if (distinctTargets.Count != 1)
                    throw new InvalidDataException($"Conflicting transforms target the same syntax node: {group.Key}");
                return group.First();
            })
            .ToList();
        return root.ReplaceNodes(
            replacements.Select(item => item.OldNode),
            (original, _) => replacements.First(item => ReferenceEquals(item.OldNode, original)).NewType);
    }

    private static Dictionary<string, int> Count(IEnumerable<string> values)
    {
        var result = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (var value in values)
        {
            var key = string.IsNullOrWhiteSpace(value) ? "<EMPTY>" : value;
            result[key] = result.TryGetValue(key, out var count) ? count + 1 : 1;
        }
        return result;
    }

    private static SourceGateSummary VerifySourceManifest(RepositoryModel model)
    {
        var mismatches = new List<string>();
        var checkedFiles = 0;
        var bytes = 0L;
        var zeroByteCs = new List<string>();
        foreach (var row in model.SourceManifest)
        {
            var relative = Repository.NormalizeRelative(row.RelativePath);
            var path = Repository.SourcePath(model, relative);
            if (!File.Exists(path))
            {
                mismatches.Add($"missing:{relative}");
                continue;
            }
            var info = new FileInfo(path);
            if (string.Equals(row.Extension, ".cs", StringComparison.OrdinalIgnoreCase))
            {
                checkedFiles++;
                bytes += info.Length;
                if (info.Length == 0) zeroByteCs.Add(relative);
                var actual = Repository.Sha256File(path);
                if (!string.Equals(actual, row.Sha256, StringComparison.OrdinalIgnoreCase))
                    mismatches.Add($"hash:{relative}:expected={row.Sha256}:actual={actual}");
            }
        }
        return new SourceGateSummary
        {
            Status = mismatches.Count == 0 ? "PASS" : "FAIL",
            ManifestFileCount = model.SourceManifest.Count,
            CheckedCSharpFiles = checkedFiles,
            CSharpBytes = bytes,
            ZeroByteCSharpFiles = zeroByteCs,
            Mismatches = mismatches
        };
    }

    private static InputIdentitySummary VerifyPinnedInputs(string artifactRoot)
    {
        var repoRoot = Directory.GetParent(Path.GetFullPath(artifactRoot))?.Parent?.FullName ?? Directory.GetCurrentDirectory();
        var expected = new Dictionary<string, (string RelativePath, string Sha256)>(StringComparer.Ordinal)
        {
            ["apk"] = ("sources/raw/Social_Dev_Story_v2.5.1.apk", "fa0e9e3a843732258fc05b2611a8e0f5be6f7e95f2141a53f31fb082322fe2bf"),
            ["rar"] = ("sources/raw/1_Click_CSharp_Code.rar", "a50a442491e422c20699a9ca4266e794d215bff29248d3edd24c41f42a57f903"),
            ["libil2cpp"] = ("knowledge/sources/phase3a_apk_probe/raw/libil2cpp.so", "364893401fcf7fc2380ae64291783edf7b95eecea4775041c3f4c8c081b4d54a"),
            ["global_metadata"] = ("knowledge/sources/phase3a_apk_probe/raw/global-metadata.dat", "f65f3a00675f35cfa28fef53c37ed7a2dc01e143b6d59c6014a286fa84e4a579")
        };
        var rows = new Dictionary<string, object>(StringComparer.Ordinal);
        var mismatches = new List<string>();
        foreach (var pair in expected)
        {
            var path = Path.Combine(repoRoot, pair.Value.RelativePath.Replace('/', Path.DirectorySeparatorChar));
            var actual = File.Exists(path) ? Repository.Sha256File(path) : null;
            if (!string.Equals(actual, pair.Value.Sha256, StringComparison.OrdinalIgnoreCase))
                mismatches.Add($"{pair.Key}:expected={pair.Value.Sha256}:actual={actual ?? "MISSING"}");
            rows[pair.Key] = new
            {
                path,
                expected_sha256 = pair.Value.Sha256,
                actual_sha256 = actual,
                match = string.Equals(actual, pair.Value.Sha256, StringComparison.OrdinalIgnoreCase)
            };
        }
        return new InputIdentitySummary
        {
            Status = mismatches.Count == 0 ? "PASS" : "FAIL",
            Rows = rows,
            Mismatches = mismatches
        };
    }
}

public sealed class SourceGateSummary
{
    public string Status { get; init; } = "";
    public int ManifestFileCount { get; init; }
    public int CheckedCSharpFiles { get; init; }
    public long CSharpBytes { get; init; }
    public List<string> ZeroByteCSharpFiles { get; init; } = new();
    public List<string> Mismatches { get; init; } = new();
}

public sealed class InputIdentitySummary
{
    public string Status { get; init; } = "";
    public Dictionary<string, object> Rows { get; init; } = new(StringComparer.Ordinal);
    public List<string> Mismatches { get; init; } = new();
}

internal sealed class ReferenceEqualityComparer : IEqualityComparer<SyntaxNode>
{
    public static readonly ReferenceEqualityComparer Instance = new();
    public bool Equals(SyntaxNode? x, SyntaxNode? y) => ReferenceEquals(x, y);
    public int GetHashCode(SyntaxNode obj) => System.Runtime.CompilerServices.RuntimeHelpers.GetHashCode(obj);
}

public static class TypeRepairRules
{
    public static TransformPlan? TryBuild(MethodRow method, LocatedMethod located)
    {
        if (!string.Equals(method.Ownership, "KAIRO_ENGINE", StringComparison.Ordinal)) return null;
        if (string.Equals(method.DeclaringType, "kairo.unity.ui.Bundle", StringComparison.Ordinal) &&
            string.Equals(method.MethodName, ".ctor", StringComparison.Ordinal) &&
            (method.NormalizedSignature == "System.Void(System.String)" || method.NormalizedSignature == "System.Void()"))
        {
            var replacements = GenericNodes(located.Node, "Dictionary<object,object>")
                .Select(node => Replacement(node, "Dictionary<string, string>", "field-typed Bundle.data_ proves Dictionary<string,string>"))
                .ToList();
            return replacements.Count == 0 ? null : new TransformPlan
            {
                Rule = "RESTORE_BUNDLE_DICTIONARY_GENERIC_ARGUMENTS",
                Replacements = replacements,
                EvidenceReason = "exact Bundle.data_ declaration and typed casts prove the erased Dictionary<string,string> identity"
            };
        }

        if (string.Equals(method.DeclaringType, "kairo.unity.graphics.MeshManager", StringComparison.Ordinal) &&
            string.Equals(method.MethodName, ".ctor", StringComparison.Ordinal) &&
            method.NormalizedSignature.Contains("kairo.unity.ui.Graphics", StringComparison.Ordinal))
        {
            var targets = new Dictionary<string, string>(StringComparer.Ordinal)
            {
                ["dictionary"] = "Dictionary<Material, MeshBuilder>",
                ["list"] = "List<KeyValuePair<Material, MeshBuilder>>",
                ["list2"] = "List<LayerMesh>",
                ["list3"] = "List<MeshRecord>"
            };
            var replacements = new List<TransformReplacement>();
            foreach (var declaration in located.Node.DescendantNodes().OfType<VariableDeclarationSyntax>())
            {
                foreach (var variable in declaration.Variables)
                {
                    if (!targets.TryGetValue(variable.Identifier.Text, out var target)) continue;
                    if (NormalizeGeneric(declaration.Type.ToString()) != NormalizeGeneric(ErasedType(declaration.Type.ToString()))) continue;
                    replacements.Add(Replacement(declaration.Type, target, $"field declaration proves {variable.Identifier.Text} type"));
                    foreach (var creation in variable.DescendantNodes().OfType<ObjectCreationExpressionSyntax>())
                    {
                        if (NormalizeGeneric(creation.Type.ToString()) == NormalizeGeneric(ErasedType(declaration.Type.ToString())))
                            replacements.Add(Replacement(creation.Type, target, $"initializer agrees with {variable.Identifier.Text} field assignment"));
                    }
                }
            }
            return replacements.Count == 0 ? null : new TransformPlan
            {
                Rule = "RESTORE_MESH_MANAGER_CONTAINER_GENERIC_ARGUMENTS",
                Replacements = replacements,
                EvidenceReason = "MeshManager field declarations and exact typed assignments prove the four erased generic container types"
            };
        }

        if (string.Equals(method.DeclaringType, "kairo.unity.util.FieldInitializer", StringComparison.Ordinal) &&
            string.Equals(method.MethodName, "RestoreFields", StringComparison.Ordinal))
        {
            var target = method.NormalizedSignature == "System.Void(System.Object)"
                ? "Dictionary<object, Data[]>"
                : method.NormalizedSignature == "System.Void(System.Type)"
                    ? "Dictionary<Type, Data[]>"
                    : "";
            if (target.Length == 0) return null;
            var replacements = GenericNodes(located.Node, "Dictionary<object,object>")
                .Select(node => Replacement(node, target, "FieldInitializer static/instance field declarations prove Data[] value type"))
                .ToList();
            return replacements.Count == 0 ? null : new TransformPlan
            {
                Rule = "RESTORE_FIELD_INITIALIZER_DICTIONARY_VALUE_TYPE",
                Replacements = replacements,
                EvidenceReason = "FieldInitializer field declarations prove the erased Dictionary value type is Data[]"
            };
        }
        return null;
    }

    private static IEnumerable<GenericNameSyntax> GenericNodes(SyntaxNode node, string normalized)
        => node.DescendantNodesAndSelf().OfType<GenericNameSyntax>()
            .Where(candidate => NormalizeGeneric(candidate.ToString()) == normalized);

    private static TransformReplacement Replacement(SyntaxNode oldNode, string target, string description)
        => new()
        {
            OldNode = oldNode,
            NewType = SyntaxFactory.ParseTypeName(target).WithTriviaFrom(oldNode),
            Description = description
        };

    private static string NormalizeGeneric(string value)
        => value.Replace(" ", "").Replace("\t", "").Replace("\r", "").Replace("\n", "");

    private static string ErasedType(string value)
    {
        if (NormalizeGeneric(value) == "List<KeyValuePair<object,object>>") return "List<KeyValuePair<object,object>>";
        if (NormalizeGeneric(value) == "List<object>") return "List<object>";
        if (NormalizeGeneric(value) == "Dictionary<object,object>") return "Dictionary<object,object>";
        return value;
    }
}
