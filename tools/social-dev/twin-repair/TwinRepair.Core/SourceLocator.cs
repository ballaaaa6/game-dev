using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.Text;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace TwinRepair.Core;

public sealed class ParsedSource
{
    public string Path { get; init; } = "";
    public string Text { get; init; } = "";
    public SyntaxTree Tree { get; init; } = null!;
    public CompilationUnitSyntax Root { get; init; } = null!;
    public List<LocatedMethod> Methods { get; init; } = new();
    public int ErrorDiagnostics { get; init; }
    public int TotalDiagnostics { get; init; }
}

public static class SourceLocator
{
    public static ParsedSource Parse(string path)
    {
        var text = System.IO.File.ReadAllText(path, Encoding.UTF8);
        return ParseText(text, path);
    }

    public static ParsedSource ParseText(string text, string path)
    {
        var parseOptions = new CSharpParseOptions(LanguageVersion.Preview);
        var tree = CSharpSyntaxTree.ParseText(text, parseOptions, path, Encoding.UTF8);
        var root = (CompilationUnitSyntax)tree.GetRoot();
        var diagnostics = tree.GetDiagnostics().ToList();
        var methods = root.DescendantNodes()
            .OfType<BaseMethodDeclarationSyntax>()
            .Select(node => Describe(tree, node))
            .ToList();

        return new ParsedSource
        {
            Path = path,
            Text = text,
            Tree = tree,
            Root = root,
            Methods = methods,
            ErrorDiagnostics = diagnostics.Count(d => d.Severity == DiagnosticSeverity.Error),
            TotalDiagnostics = diagnostics.Count
        };
    }

    public static List<LocatedMethod> Candidates(ParsedSource source, MethodRow method)
    {
        return source.Methods.Where(candidate =>
            string.Equals(candidate.DeclaringType, method.DeclaringType, StringComparison.Ordinal) &&
            string.Equals(candidate.MethodName, method.MethodName, StringComparison.Ordinal) &&
            candidate.GenericArity == method.GenericArity &&
            candidate.ParameterCount == method.ParameterCount &&
            ParameterTypesMatch(method, candidate)).ToList();
    }

    public static bool ParameterTypesMatch(MethodRow method, LocatedMethod candidate)
    {
        if (method.ParameterTypes.Count != candidate.ParameterTypes.Count)
            return false;
        return method.ParameterTypes.Zip(candidate.ParameterTypes)
            .All(pair => TypeEquivalent(pair.First, pair.Second));
    }

    public static bool ParameterTypeEquivalent(string canonical, string source)
        => TypeEquivalent(canonical, source);

    public static LocatedMethod Describe(SyntaxTree tree, BaseMethodDeclarationSyntax node)
    {
        var lineSpan = tree.GetLineSpan(node.Span);
        var body = BodyText(tree, node);

        var methodName = node is ConstructorDeclarationSyntax
            ? ".ctor"
            : node is DestructorDeclarationSyntax destructor
                ? "~" + destructor.Identifier.Text
                : node is MethodDeclarationSyntax method
                    ? method.Identifier.Text
                    : node.Kind().ToString();
        var genericArity = node is MethodDeclarationSyntax methodNode
            ? methodNode.TypeParameterList?.Parameters.Count ?? 0
            : 0;

        return new LocatedMethod
        {
            DeclaringType = GetDeclaringType(node),
            MethodName = methodName,
            GenericArity = genericArity,
            ParameterCount = node.ParameterList?.Parameters.Count ?? 0,
            ParameterTypes = node.ParameterList?.Parameters
                .Select(parameter => ParameterTypeText(parameter))
                .ToList() ?? new List<string>(),
            StartLine = lineSpan.StartLinePosition.Line + 1,
            EndLine = lineSpan.EndLinePosition.Line + 1,
            BodySha256 = Repository.Sha256Text(body.Replace("\r\n", "\n").Replace("\r", "\n")),
            Node = node
        };
    }

    private static string ParameterTypeText(ParameterSyntax parameter)
    {
        var type = parameter.Type?.ToString() ?? "";
        var byReference = parameter.Modifiers.Any(modifier => modifier.IsKind(SyntaxKind.RefKeyword) ||
                                                              modifier.IsKind(SyntaxKind.OutKeyword) ||
                                                              modifier.IsKind(SyntaxKind.InKeyword));
        return type + (byReference ? "&" : "");
    }

    private static bool TypeEquivalent(string left, string right)
    {
        var normalizedLeft = NormalizeType(left);
        var normalizedRight = NormalizeType(right);
        return string.Equals(normalizedLeft, normalizedRight, StringComparison.Ordinal) ||
               string.Equals(ShortenTypeNames(normalizedLeft), ShortenTypeNames(normalizedRight), StringComparison.Ordinal);
    }

    private static string NormalizeType(string value)
    {
        var text = value.Trim().Replace("global::", "", StringComparison.Ordinal)
            .Replace(" ", "", StringComparison.Ordinal)
            .Replace("\t", "", StringComparison.Ordinal)
            .Replace("\r", "", StringComparison.Ordinal)
            .Replace("\n", "", StringComparison.Ordinal)
            .Replace("?", "", StringComparison.Ordinal);
        foreach (var pair in Aliases)
        {
            text = ReplaceIdentifier(text, pair.Key, pair.Value);
        }
        return text;
    }

    private static string ShortenTypeNames(string value)
    {
        var builder = new StringBuilder(value.Length);
        var token = new StringBuilder();
        void Flush()
        {
            if (token.Length == 0) return;
            builder.Append(token.ToString().Split('.').Last());
            token.Clear();
        }
        foreach (var character in value)
        {
            if (char.IsLetterOrDigit(character) || character == '_' || character == '.')
            {
                token.Append(character);
                continue;
            }
            Flush();
            builder.Append(character);
        }
        Flush();
        return builder.ToString();
    }

    private static string ReplaceIdentifier(string value, string identifier, string replacement)
    {
        var builder = new StringBuilder(value.Length);
        var token = new StringBuilder();
        void Flush()
        {
            if (token.Length == 0) return;
            builder.Append(string.Equals(token.ToString(), identifier, StringComparison.Ordinal) ? replacement : token.ToString());
            token.Clear();
        }
        foreach (var character in value)
        {
            if (char.IsLetterOrDigit(character) || character == '_')
            {
                token.Append(character);
                continue;
            }
            Flush();
            builder.Append(character);
        }
        Flush();
        return builder.ToString();
    }

    private static readonly Dictionary<string, string> Aliases = new(StringComparer.Ordinal)
    {
        ["object"] = "System.Object",
        ["string"] = "System.String",
        ["bool"] = "System.Boolean",
        ["byte"] = "System.Byte",
        ["sbyte"] = "System.SByte",
        ["short"] = "System.Int16",
        ["ushort"] = "System.UInt16",
        ["int"] = "System.Int32",
        ["uint"] = "System.UInt32",
        ["long"] = "System.Int64",
        ["ulong"] = "System.UInt64",
        ["char"] = "System.Char",
        ["float"] = "System.Single",
        ["double"] = "System.Double",
        ["decimal"] = "System.Decimal",
        ["void"] = "System.Void"
    };

    private static string BodyText(SyntaxTree tree, BaseMethodDeclarationSyntax node)
    {
        if (node is MethodDeclarationSyntax method && method.Body != null)
            return tree.GetText().ToString(TextSpan.FromBounds(method.Body.OpenBraceToken.Span.End, method.Body.CloseBraceToken.SpanStart));
        if (node is ConstructorDeclarationSyntax constructor && constructor.Body != null)
            return tree.GetText().ToString(TextSpan.FromBounds(constructor.Body.OpenBraceToken.Span.End, constructor.Body.CloseBraceToken.SpanStart));
        if (node is DestructorDeclarationSyntax destructor && destructor.Body != null)
            return tree.GetText().ToString(TextSpan.FromBounds(destructor.Body.OpenBraceToken.Span.End, destructor.Body.CloseBraceToken.SpanStart));
        if (node is MethodDeclarationSyntax expressionMethod && expressionMethod.ExpressionBody != null)
            return tree.GetText().ToString(TextSpan.FromBounds(expressionMethod.ExpressionBody.ArrowToken.Span.End, expressionMethod.SemicolonToken.SpanStart));
        if (node is ConstructorDeclarationSyntax expressionConstructor && expressionConstructor.ExpressionBody != null)
            return tree.GetText().ToString(TextSpan.FromBounds(expressionConstructor.ExpressionBody.ArrowToken.Span.End, expressionConstructor.SemicolonToken.SpanStart));
        return "";
    }

    public static string GetDeclaringType(SyntaxNode node)
    {
        var namespaceParts = node.Ancestors()
            .OfType<BaseNamespaceDeclarationSyntax>()
            .Reverse()
            .Select(ns => ns.Name.ToString())
            .Where(value => !string.IsNullOrWhiteSpace(value))
            .ToList();
        var typeParts = node.Ancestors()
            .OfType<TypeDeclarationSyntax>()
            .Reverse()
            .Select(TypeName)
            .ToList();
        var all = namespaceParts.Concat(typeParts).ToList();
        return string.Join(".", all);
    }

    public static string TypeName(TypeDeclarationSyntax type)
    {
        var arity = type.TypeParameterList?.Parameters.Count ?? 0;
        return arity == 0 ? type.Identifier.Text : $"{type.Identifier.Text}`{arity}";
    }
}
