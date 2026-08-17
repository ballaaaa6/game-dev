using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace TwinRepair.Core;

public sealed class R3TransformDecision
{
    public string Family { get; init; } = "";
    public bool Eligible { get; init; }
    public string Reason { get; init; } = "";
    public SyntaxNode? RewrittenRoot { get; init; }
}

/// <summary>
/// Roslyn-only CFG-family transformer entry point for R3.
/// It deliberately exposes a narrow proof gate; a syntax parse is never
/// treated as semantic equivalence evidence.
/// </summary>
public static class R3CfgTransformers
{
    public static readonly IReadOnlyList<string> Families = new[]
    {
        "LOCAL_GOTO_BRANCH_CFG",
        "LOOP_CFG_COLLAPSE",
        "SWITCH_OR_JUMP_TABLE_COLLAPSE",
        "TRY_FINALLY_CFG_COLLAPSE",
        "TYPE_EROSION_PLUS_HEAVY_GOTO",
        "DECOMPILER_TYPE_CFG_DAMAGE",
        "SWITCH_STRUCTURAL_DAMAGE",
        "STRUCTURED_CONTROL_SUSPECT",
        "OTHER_CFG"
    };

    /// <summary>
    /// Plans the only currently implemented proof shape: an unconditional
    /// goto whose target label is the immediately following statement in the
    /// same block and has no other incoming goto. The rewrite removes the
    /// redundant goto and label through Roslyn nodes, never text splicing.
    /// </summary>
    public static R3TransformDecision PlanLocalGotoBranch(
        BaseMethodDeclarationSyntax method,
        bool exactIdentity,
        bool exactIsilSelection,
        bool semanticBindingProof,
        bool graphEquivalenceProof)
    {
        const string family = "LOCAL_GOTO_BRANCH_CFG";
        if (!exactIdentity)
            return Reject(family, "EXACT_SOURCE_IDENTITY_REQUIRED");
        if (!exactIsilSelection)
            return Reject(family, "EXACT_ISIL_SELECTION_REQUIRED");

        var candidate = FindCandidate(method);
        if (candidate is null)
            return Reject(family, "NO_STRICT_IMMEDIATE_LABEL_PATTERN");
        if (!semanticBindingProof)
            return Reject(family, "SEMANTIC_BINDING_PROOF_REQUIRED");
        if (!graphEquivalenceProof)
            return Reject(family, "GRAPH_EQUIVALENCE_PROOF_REQUIRED");

        var root = method.SyntaxTree.GetRoot();
        var withoutLabel = root.ReplaceNode(
            candidate.Value.Label,
            candidate.Value.Label.Statement.WithTriviaFrom(candidate.Value.Label));
        var gotoAfterLabelReplacement = withoutLabel.DescendantNodes()
            .OfType<GotoStatementSyntax>()
            .FirstOrDefault(node => node.SpanStart == candidate.Value.Goto.SpanStart);
        var rewritten = gotoAfterLabelReplacement is null
            ? null
            : withoutLabel.RemoveNode(gotoAfterLabelReplacement, SyntaxRemoveOptions.KeepNoTrivia);
        return new R3TransformDecision
        {
            Family = family,
            Eligible = rewritten is not null,
            Reason = rewritten is not null ? "PROVEN_REDUNDANT_IMMEDIATE_LABEL" : "ROSLYN_REWRITE_FAILED",
            RewrittenRoot = rewritten
        };
    }

    public static int SelfTest()
    {
        const string source = "class Fixture { void M() { goto L; L: return; } }";
        var tree = CSharpSyntaxTree.ParseText(source, new CSharpParseOptions(LanguageVersion.Preview));
        var method = tree.GetRoot().DescendantNodes().OfType<MethodDeclarationSyntax>().Single();
        var rejected = PlanLocalGotoBranch(method, true, true, false, false);
        if (rejected.Eligible || rejected.Reason != "SEMANTIC_BINDING_PROOF_REQUIRED")
            return 1;

        var accepted = PlanLocalGotoBranch(method, true, true, true, true);
        var rewritten = accepted.RewrittenRoot?.ToFullString() ?? "";
        if (!accepted.Eligible || rewritten.Contains("goto", StringComparison.Ordinal) ||
            rewritten.Contains("L:", StringComparison.Ordinal))
            return 2;
        Console.WriteLine("r3-selftest PASS");
        return 0;
    }

    private static R3TransformDecision Reject(string family, string reason)
        => new() { Family = family, Eligible = false, Reason = reason };

    private static (GotoStatementSyntax Goto, LabeledStatementSyntax Label)? FindCandidate(
        BaseMethodDeclarationSyntax method)
    {
        var root = method;
        foreach (var block in root.DescendantNodesAndSelf().OfType<BlockSyntax>())
        {
            for (var index = 0; index + 1 < block.Statements.Count; index++)
            {
                if (block.Statements[index] is not GotoStatementSyntax gotoStatement ||
                    gotoStatement.Expression is not IdentifierNameSyntax target ||
                    block.Statements[index + 1] is not LabeledStatementSyntax label ||
                    !string.Equals(target.Identifier.Text, label.Identifier.Text, StringComparison.Ordinal))
                    continue;

                var incoming = root.DescendantNodes()
                    .OfType<GotoStatementSyntax>()
                    .Count(candidate => candidate.Expression is IdentifierNameSyntax name &&
                        string.Equals(name.Identifier.Text, label.Identifier.Text, StringComparison.Ordinal));
                if (incoming == 1)
                    return (gotoStatement, label);
            }
        }
        return null;
    }
}
