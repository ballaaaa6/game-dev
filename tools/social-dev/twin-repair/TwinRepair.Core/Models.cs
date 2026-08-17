using System;
using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace TwinRepair.Core;

public sealed class MethodRow
{
    [JsonPropertyName("method_id")] public string MethodId { get; set; } = "";
    [JsonPropertyName("assembly")] public string Assembly { get; set; } = "";
    [JsonPropertyName("declaring_type")] public string DeclaringType { get; set; } = "";
    [JsonPropertyName("method_name")] public string MethodName { get; set; } = "";
    [JsonPropertyName("generic_arity")] public int GenericArity { get; set; }
    [JsonPropertyName("normalized_signature")] public string NormalizedSignature { get; set; } = "";
    [JsonPropertyName("ownership")] public string Ownership { get; set; } = "";
    [JsonPropertyName("quality_class")] public string QualityClass { get; set; } = "";
    [JsonPropertyName("repair_disposition")] public string RepairDisposition { get; set; } = "";
    [JsonPropertyName("verification_status")] public string VerificationStatus { get; set; } = "";
    [JsonPropertyName("source_file")] public string? SourceFile { get; set; }
    [JsonPropertyName("source_line")] public int? SourceLine { get; set; }
    [JsonPropertyName("source_line_end")] public int? SourceLineEnd { get; set; }
    [JsonPropertyName("source_match_status")] public string SourceMatchStatus { get; set; } = "";
    [JsonPropertyName("source_present")] public bool SourcePresent { get; set; }
    [JsonPropertyName("source_body_present")] public bool SourceBodyPresent { get; set; }
    [JsonPropertyName("body_sha256")] public string BodySha256 { get; set; } = "";
    [JsonPropertyName("body_lines")] public int? BodyLines { get; set; }
    [JsonPropertyName("metadata_token")] public string? MetadataToken { get; set; }
    [JsonPropertyName("rva")] public int? Rva { get; set; }
    [JsonPropertyName("evidence_refs")] public List<string> EvidenceRefs { get; set; } = new();
    [JsonPropertyName("r0_signals")] public Dictionary<string, int> R0Signals { get; set; } = new();
    [JsonPropertyName("parameter_count")] public int ParameterCount { get; set; }
    [JsonPropertyName("parameter_types")] public List<string> ParameterTypes { get; set; } = new();
    [JsonPropertyName("return_type")] public string ReturnType { get; set; } = "";
    [JsonPropertyName("repaired_body")] public bool RepairedBody { get; set; }
}

public sealed class TypeRow
{
    [JsonPropertyName("type_id")] public string TypeId { get; set; } = "";
    [JsonPropertyName("assembly")] public string Assembly { get; set; } = "";
    [JsonPropertyName("full_name")] public string FullName { get; set; } = "";
    [JsonPropertyName("ownership")] public string Ownership { get; set; } = "";
    [JsonPropertyName("inclusion")] public string Inclusion { get; set; } = "";
    [JsonPropertyName("source_file")] public string? SourceFile { get; set; }
}

public sealed class QueueRow
{
    [JsonPropertyName("queue_id")] public string QueueId { get; set; } = "";
    [JsonPropertyName("method_id")] public string MethodId { get; set; } = "";
    [JsonPropertyName("assembly")] public string Assembly { get; set; } = "";
    [JsonPropertyName("declaring_type")] public string DeclaringType { get; set; } = "";
    [JsonPropertyName("method_name")] public string MethodName { get; set; } = "";
    [JsonPropertyName("normalized_signature")] public string NormalizedSignature { get; set; } = "";
    [JsonPropertyName("ownership")] public string Ownership { get; set; } = "";
    [JsonPropertyName("quality_class")] public string QualityClass { get; set; } = "";
    [JsonPropertyName("repair_disposition")] public string RepairDisposition { get; set; } = "";
    [JsonPropertyName("verification_status")] public string VerificationStatus { get; set; } = "";
    [JsonPropertyName("source_present")] public bool SourcePresent { get; set; }
    [JsonPropertyName("isil_available")] public bool IsilAvailable { get; set; }
    [JsonPropertyName("native_available")] public bool NativeAvailable { get; set; }
    [JsonPropertyName("priority")] public int Priority { get; set; }
}

public sealed class SourceFileRow
{
    [JsonPropertyName("relative_path")] public string RelativePath { get; set; } = "";
    [JsonPropertyName("bytes")] public long Bytes { get; set; }
    [JsonPropertyName("sha256")] public string Sha256 { get; set; } = "";
    [JsonPropertyName("extension")] public string Extension { get; set; } = "";
}

public sealed class RepairJob
{
    public QueueRow Queue { get; init; } = new();
    public MethodRow Method { get; init; } = new();
}

public sealed class LocatedMethod
{
    public string DeclaringType { get; init; } = "";
    public string MethodName { get; init; } = "";
    public int GenericArity { get; init; }
    public int ParameterCount { get; init; }
    public List<string> ParameterTypes { get; init; } = new();
    public int StartLine { get; init; }
    public int EndLine { get; init; }
    public string BodySha256 { get; init; } = "";
    public Microsoft.CodeAnalysis.CSharp.Syntax.BaseMethodDeclarationSyntax Node { get; init; } = null!;
}

public sealed class GateRecord
{
    [JsonPropertyName("method_id")]
    public string MethodId { get; init; } = "";
    [JsonPropertyName("queue_id")]
    public string QueueId { get; init; } = "";
    [JsonPropertyName("assembly")]
    public string Assembly { get; init; } = "";
    [JsonPropertyName("declaring_type")]
    public string DeclaringType { get; init; } = "";
    [JsonPropertyName("method_name")]
    public string MethodName { get; init; } = "";
    [JsonPropertyName("normalized_signature")]
    public string NormalizedSignature { get; init; } = "";
    [JsonPropertyName("metadata_token")]
    public string? MetadataToken { get; init; }
    [JsonPropertyName("rva")]
    public int? Rva { get; init; }
    [JsonPropertyName("source_line")]
    public int? SourceLine { get; init; }
    [JsonPropertyName("source_line_end")]
    public int? SourceLineEnd { get; init; }
    [JsonPropertyName("source_file")]
    public string SourceFile { get; init; } = "";
    [JsonPropertyName("repair_disposition")]
    public string RepairDisposition { get; init; } = "";
    [JsonPropertyName("source_match_status")]
    public string SourceMatchStatus { get; init; } = "";
    [JsonPropertyName("gate")]
    public string Gate { get; set; } = "";
    [JsonPropertyName("final_status")]
    public string FinalStatus { get; set; } = "";
    [JsonPropertyName("reason")]
    public string Reason { get; set; } = "";
    [JsonPropertyName("exact_source_identity")]
    public bool ExactSourceIdentity { get; set; }
    [JsonPropertyName("parameter_types_match")]
    public bool ParameterTypesMatch { get; set; }
    [JsonPropertyName("metadata_identity_agrees")]
    public bool MetadataIdentityAgrees { get; set; }
    [JsonPropertyName("body_hash_matches")]
    public bool BodyHashMatches { get; set; }
    [JsonPropertyName("candidate_count")]
    public int CandidateCount { get; set; }
    [JsonPropertyName("transform_available")]
    public bool TransformAvailable { get; set; }
    [JsonPropertyName("transform_rule")]
    public string TransformRule { get; set; } = "";
    [JsonPropertyName("syntax_diagnostics_before")]
    public int SyntaxDiagnosticsBefore { get; set; }
    [JsonPropertyName("evidence_refs")]
    public List<string> EvidenceRefs { get; init; } = new();
}

public sealed class PlanReport
{
    [JsonPropertyName("schema_version")] public string SchemaVersion { get; set; } = "";
    [JsonPropertyName("status")] public string Status { get; set; } = "";
    [JsonPropertyName("method_count")] public int MethodCount { get; set; }
    [JsonPropertyName("queue_count")] public int QueueCount { get; set; }
    [JsonPropertyName("record_count")] public int RecordCount { get; set; }
    [JsonPropertyName("records")] public List<GateRecord> Records { get; set; } = new();
}

public sealed class BatchFileResult
{
    [JsonPropertyName("relative_path")] public string RelativePath { get; init; } = "";
    [JsonPropertyName("original_path")] public string OriginalPath { get; init; } = "";
    [JsonPropertyName("twin_path")] public string TwinPath { get; init; } = "";
    [JsonPropertyName("before_sha256")] public string BeforeSha256 { get; init; } = "";
    [JsonPropertyName("after_sha256")] public string AfterSha256 { get; init; } = "";
    [JsonPropertyName("before_bytes")] public long BeforeBytes { get; init; }
    [JsonPropertyName("after_bytes")] public long AfterBytes { get; init; }
    [JsonPropertyName("changed")] public bool Changed { get; init; }
    [JsonPropertyName("method_ids")] public List<string> MethodIds { get; init; } = new();
    [JsonPropertyName("syntax_diagnostics_before")] public int SyntaxDiagnosticsBefore { get; init; }
    [JsonPropertyName("syntax_diagnostics_after")] public int SyntaxDiagnosticsAfter { get; init; }
}

public sealed class BatchSummary
{
    [JsonPropertyName("schema_version")] public string SchemaVersion { get; set; } = "";
    [JsonPropertyName("status")] public string Status { get; set; } = "";
    [JsonPropertyName("batch_id")] public string BatchId { get; set; } = "";
    [JsonPropertyName("planned_repair_eligible")] public int PlannedRepairEligible { get; set; }
    [JsonPropertyName("repaired_count")] public int RepairedCount { get; set; }
    [JsonPropertyName("provenance_count")] public int ProvenanceCount { get; set; }
    [JsonPropertyName("method_status_count")] public int MethodStatusCount { get; set; }
    [JsonPropertyName("files")] public List<BatchFileResult> Files { get; set; } = new();
    [JsonPropertyName("status_counts")] public Dictionary<string, int> StatusCounts { get; set; } = new(StringComparer.Ordinal);
    [JsonPropertyName("errors")] public List<string> Errors { get; set; } = new();
    [JsonPropertyName("checks")] public Dictionary<string, bool> Checks { get; set; } = new(StringComparer.Ordinal);
}

public sealed class MethodProvenance
{
    [JsonPropertyName("method_id")] public string MethodId { get; init; } = "";
    [JsonPropertyName("source_file")] public string SourceFile { get; init; } = "";
    [JsonPropertyName("assembly")] public string Assembly { get; init; } = "";
    [JsonPropertyName("declaring_type")] public string DeclaringType { get; init; } = "";
    [JsonPropertyName("normalized_signature")] public string NormalizedSignature { get; init; } = "";
    [JsonPropertyName("repair_pass")] public string RepairPass { get; init; } = "R2.2_TYPE_REPAIR";
    [JsonPropertyName("before_file_sha256")] public string BeforeFileSha256 { get; init; } = "";
    [JsonPropertyName("before_body_sha256")] public string BeforeBodySha256 { get; init; } = "";
    [JsonPropertyName("after_file_sha256")] public string AfterFileSha256 { get; init; } = "";
    [JsonPropertyName("after_body_sha256")] public string AfterBodySha256 { get; init; } = "";
    [JsonPropertyName("syntax_nodes_changed")] public List<string> SyntaxNodesChanged { get; init; } = new();
    [JsonPropertyName("evidence_refs")] public List<string> EvidenceRefs { get; init; } = new();
    [JsonPropertyName("metadata_token")] public string? MetadataToken { get; init; }
    [JsonPropertyName("rva")] public int? Rva { get; init; }
    [JsonPropertyName("source_match_proof")] public string SourceMatchProof { get; init; } = "";
    [JsonPropertyName("validation_result")] public string ValidationResult { get; init; } = "";
    [JsonPropertyName("batch_id")] public string BatchId { get; init; } = "";
    [JsonPropertyName("status")] public string Status { get; init; } = "REPAIRED_CSHARP";
    [JsonPropertyName("rule")] public string Rule { get; init; } = "";
}
