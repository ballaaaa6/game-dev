using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using TwinRepair.Core;

namespace TwinRepair.Cli;

public static class Program
{
    public static int Run(string[] args)
    {
        if (args.Length == 0 || args[0] is "help" or "--help" or "-h")
        {
            PrintUsage();
            return args.Length == 0 ? 2 : 0;
        }

        var command = args[0].ToLowerInvariant();
        var options = ParseOptions(args.Skip(1).ToArray());
        try
        {
            return command switch
            {
                "probe" => RepairFactory.Probe(options.ArtifactRoot, options.SourceRoot, options.OutRoot),
                "mirror" => RepairFactory.Mirror(options.ArtifactRoot, options.SourceRoot, options.OutRoot),
                "plan" => RepairFactory.Plan(options.ArtifactRoot, options.SourceRoot, options.OutRoot),
                "apply" => RepairFactory.Apply(options.ArtifactRoot, options.SourceRoot, options.OutRoot, options.BatchId),
                "verify" => RepairFactory.Verify(options.ArtifactRoot, options.SourceRoot, options.OutRoot, options.BatchId),
                "reindex" => RepairFactory.Reindex(options.ArtifactRoot, options.SourceRoot, options.OutRoot),
                "report" => RepairFactory.Report(options.ArtifactRoot, options.SourceRoot, options.OutRoot),
                "r3-selftest" => R3CfgTransformers.SelfTest(),
                _ => Unknown(command)
            };
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"R2_FACTORY_ERROR: {ex.GetType().Name}: {ex.Message}");
            Console.Error.WriteLine(ex.StackTrace);
            return 1;
        }
    }

    private static FactoryOptions ParseOptions(string[] args)
    {
        var cwd = Directory.GetCurrentDirectory();
        var options = new FactoryOptions
        {
            ArtifactRoot = Path.Combine(cwd, "artifacts", "r1-5-metadata-reconciliation"),
            SourceRoot = Path.Combine(cwd, "knowledge", "sources", "csharp_raw_20260813", "1_Click_CSharp_Code"),
            OutRoot = Path.Combine(cwd, "artifacts", "r2-reference-twin"),
            BatchId = "r2-type-canary-001"
        };
        for (var i = 0; i < args.Length; i++)
        {
            var value = args[i];
            if (value is "--artifact-root" or "--source-root" or "--out" or "--batch")
            {
                if (i + 1 >= args.Length) throw new ArgumentException($"Missing value for {value}");
                var next = value == "--batch" ? args[++i] : Path.GetFullPath(args[++i]);
                if (value == "--artifact-root") options.ArtifactRoot = next;
                else if (value == "--source-root") options.SourceRoot = next;
                else if (value == "--out") options.OutRoot = next;
                else options.BatchId = next;
            }
            else
            {
                throw new ArgumentException($"Unknown option: {value}");
            }
        }
        return options;
    }

    private static int Unknown(string command)
    {
        Console.Error.WriteLine($"Unknown twin-repair command: {command}");
        PrintUsage();
        return 2;
    }

    private static void PrintUsage()
    {
        Console.WriteLine("twin-repair probe|mirror|plan|apply|verify|reindex|report [--artifact-root PATH] [--source-root PATH] [--out PATH] [--batch ID]");
        Console.WriteLine("probe  validates the canonical R1.5 queue and source manifest");
        Console.WriteLine("mirror creates the ignored Reference Twin baseline");
        Console.WriteLine("plan   parses each source file once and emits the exact write-gate status universe");
        Console.WriteLine("apply  applies only REPAIR_ELIGIBLE syntax-node transforms to the ignored Twin");
        Console.WriteLine("verify replays an accepted batch and checks provenance, hashes, and status coverage");
        Console.WriteLine("reindex conservatively reindexes the Twin and reconciles the accepted graph split");
        Console.WriteLine("report  summarizes the R2 local reports");
        Console.WriteLine("r3-selftest  runs the Roslyn-only R3 transformer proof sentinel");
    }
}

public sealed class FactoryOptions
{
    public string ArtifactRoot { get; set; } = "";
    public string SourceRoot { get; set; } = "";
    public string OutRoot { get; set; } = "";
    public string BatchId { get; set; } = "r2-type-canary-001";
}
