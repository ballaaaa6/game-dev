using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

namespace TwinRepair.Core;

public sealed class RepositoryModel
{
    public string ArtifactRoot { get; init; } = "";
    public string SourceRoot { get; init; } = "";
    public List<MethodRow> Methods { get; init; } = new();
    public List<TypeRow> Types { get; init; } = new();
    public List<QueueRow> Queue { get; init; } = new();
    public Dictionary<string, MethodRow> MethodsById { get; init; } = new();
    public Dictionary<string, QueueRow> QueueByMethodId { get; init; } = new();
    public List<SourceFileRow> SourceManifest { get; init; } = new();
}

public static class Repository
{
    public static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNameCaseInsensitive = true,
        WriteIndented = true
    };

    public static RepositoryModel Load(string artifactRoot, string sourceRoot)
    {
        var methods = ReadJsonl<MethodRow>(Path.Combine(artifactRoot, "method-catalog.jsonl"));
        var types = ReadJsonl<TypeRow>(Path.Combine(artifactRoot, "type-catalog.jsonl"));
        var queue = ReadJsonl<QueueRow>(Path.Combine(artifactRoot, "repair-queue.jsonl"));
        var sourceManifestPath = Path.Combine(artifactRoot, "source-file-manifest.json");
        var sourceManifest = File.Exists(sourceManifestPath)
            ? JsonSerializer.Deserialize<List<SourceFileRow>>(File.ReadAllText(sourceManifestPath), JsonOptions) ?? new()
            : new List<SourceFileRow>();

        var methodsById = new Dictionary<string, MethodRow>(StringComparer.Ordinal);
        foreach (var method in methods)
        {
            if (!methodsById.TryAdd(method.MethodId, method))
                throw new InvalidDataException($"Duplicate method_id: {method.MethodId}");
        }

        var queueByMethodId = new Dictionary<string, QueueRow>(StringComparer.Ordinal);
        foreach (var row in queue)
        {
            if (!queueByMethodId.TryAdd(row.MethodId, row))
                throw new InvalidDataException($"Duplicate queue method_id: {row.MethodId}");
            if (!methodsById.ContainsKey(row.MethodId))
                throw new InvalidDataException($"Queue row has no method catalog row: {row.MethodId}");
        }

        return new RepositoryModel
        {
            ArtifactRoot = Path.GetFullPath(artifactRoot),
            SourceRoot = Path.GetFullPath(sourceRoot),
            Methods = methods,
            Types = types,
            Queue = queue,
            MethodsById = methodsById,
            QueueByMethodId = queueByMethodId,
            SourceManifest = sourceManifest
        };
    }

    public static List<T> ReadJsonl<T>(string path)
    {
        if (!File.Exists(path))
            throw new FileNotFoundException("Missing canonical artifact", path);
        var result = new List<T>();
        foreach (var line in File.ReadLines(path))
        {
            if (string.IsNullOrWhiteSpace(line)) continue;
            var value = JsonSerializer.Deserialize<T>(line, JsonOptions);
            if (value == null) throw new InvalidDataException($"Null JSONL row in {path}");
            result.Add(value);
        }
        return result;
    }

    public static List<RepairJob> Jobs(RepositoryModel model)
    {
        return model.Queue.Select(q => new RepairJob
        {
            Queue = q,
            Method = model.MethodsById[q.MethodId]
        }).ToList();
    }

    public static string NormalizeRelative(string path)
        => path.Replace('\\', '/').TrimStart('/');

    public static string SourcePath(RepositoryModel model, string relativePath)
        => Path.GetFullPath(Path.Combine(model.SourceRoot, NormalizeRelative(relativePath).Replace('/', Path.DirectorySeparatorChar)));

    public static string Sha256File(string path)
    {
        using var sha = SHA256.Create();
        using var stream = File.OpenRead(path);
        return Convert.ToHexString(sha.ComputeHash(stream)).ToLowerInvariant();
    }

    public static string Sha256Text(string text)
        => Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(text))).ToLowerInvariant();

    public static void WriteJson(string path, object value)
    {
        Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(path))!);
        File.WriteAllText(path, JsonSerializer.Serialize(value, JsonOptions) + Environment.NewLine, new UTF8Encoding(false));
    }

    public static void WriteJsonl<T>(string path, IEnumerable<T> values)
    {
        Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(path))!);
        var jsonlOptions = new JsonSerializerOptions(JsonOptions) { WriteIndented = false };
        using var writer = new StreamWriter(path, false, new UTF8Encoding(false));
        foreach (var value in values)
            writer.WriteLine(JsonSerializer.Serialize(value, jsonlOptions));
    }
}
